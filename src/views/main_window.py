"""
Janela principal da aplicação.

Responsável por criar o shell da UI (sidebar, header, stack de
páginas) e registrar todas as features via `features.registry`.
Esta classe deve ser mantida enxuta — a lógica de cada tela vive
em `src/features/<nome>/`.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from src.core.container import container
from src.core.signals import event_bus
from src.core.types import PageId
from src.features.registry import FEATURE_METADATA, get_metadata, register_all_features
from src.services.config_service import ConfigService
from src.services.navigation_service import NavigationService
from src.services.theme_service import ThemeService


class MainWindow(QMainWindow):
    """
    Janela principal.

    Layout:
        ┌────────────────────────────────────────────┐
        │         │ Header                           │
        │ Sidebar ├──────────────────────────────────┤
        │         │                                  │
        │         │      QStackedWidget              │
        │         │      (páginas das features)      │
        │         │                                  │
        └────────────────────────────────────────────┘

    A troca de páginas deve ser feita via `NavigationService`, nunca
    chamando `QStackedWidget.setCurrentWidget` diretamente.
    """

    def __init__(self) -> None:
        super().__init__()

        self._setup_services()
        self._setup_window()
        self._setup_ui()
        self._register_features()
        self._setup_connections()

        default_page_id = next(
            (meta.page_id for meta in FEATURE_METADATA if meta.is_default),
            PageId.HOME,
        )
        self._navigation.navigate_to(default_page_id)

    # --------------------------------------------------------------- setup

    def _setup_services(self) -> None:
        self._navigation = container.resolve(NavigationService)
        self._config = container.resolve(ConfigService)
        self._theme_service = container.resolve(ThemeService)

    def _setup_window(self) -> None:
        self.setWindowTitle(self._config.get("app.name", "PySide6 App Template"))

        width = self._config.get("window.width", 1200)
        height = self._config.get("window.height", 800)
        min_width = self._config.get("window.min_width", 800)
        min_height = self._config.get("window.min_height", 600)

        self.resize(width, height)
        self.setMinimumSize(min_width, min_height)
        self._center_on_screen()

    def _center_on_screen(self) -> None:
        screen = self.screen()
        if screen:
            rect = screen.availableGeometry()
            x = (rect.width() - self.width()) // 2
            y = (rect.height() - self.height()) // 2
            self.move(x, y)

    def _setup_ui(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self._sidebar = self._create_sidebar()
        main_layout.addWidget(self._sidebar)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self._header = self._create_header()
        content_layout.addWidget(self._header)

        self._stack = QStackedWidget()
        content_layout.addWidget(self._stack, 1)

        main_layout.addWidget(content_widget, 1)
        self._navigation.set_stack_widget(self._stack)

    def _create_sidebar(self) -> QWidget:
        from src.components.layout.sidebar import Sidebar, SidebarMenuItem

        sidebar = Sidebar(self)
        sidebar.set_items(
            [
                SidebarMenuItem(meta.page_id, meta.title, meta.icon)
                for meta in FEATURE_METADATA
            ]
        )
        return sidebar

    def _create_header(self) -> QWidget:
        from src.components.layout.header import Header

        return Header(
            title=self._config.get("app.name", "PySide6 App"),
            parent=self,
        )

    def _register_features(self) -> None:
        """Delega criação e registro das páginas para `features.registry`."""
        register_all_features(self._navigation, parent=self)

    def _setup_connections(self) -> None:
        self._navigation.page_changed.connect(self._on_page_changed)
        event_bus.theme_change_requested.connect(self._on_theme_change_requested)
        event_bus.app_closing.connect(self._on_app_closing)

    # -------------------------------------------------------------- events

    def _on_page_changed(self, page_id: PageId, params: dict) -> None:
        meta = get_metadata(page_id)
        if meta and hasattr(self, "_header") and hasattr(self._header, "set_title"):
            self._header.set_title(meta.title)

    def _on_theme_change_requested(self, theme) -> None:
        self._theme_service.set_theme(theme)

    def _on_app_closing(self) -> None:
        if self._config.get("window.remember_size", True):
            self._config.set("window.width", self.width())
            self._config.set("window.height", self.height())

        if self._config.get("window.remember_position", True):
            pos = self.pos()
            self._config.set("window.x", pos.x())
            self._config.set("window.y", pos.y())

    def closeEvent(self, event) -> None:
        event_bus.app_closing.emit()
        super().closeEvent(event)
