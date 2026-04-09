"""
Componente Sidebar.

Barra lateral de navegação data-driven: o conjunto de itens é
injetado pelo chamador via `set_items(...)`. O próprio componente
não conhece nenhuma feature específica — por isso pode ficar em
`src/components/`, sem criar dependência circular para
`src/features/`.
"""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.components.base import BaseComponent
from src.core.container import container
from src.core.types import PageId


@dataclass(frozen=True)
class SidebarMenuItem:
    """Descreve uma entrada na sidebar."""

    page_id: PageId
    label: str
    icon: str = ""


class _SidebarButton(QPushButton):
    """Botão de item da sidebar com estado de seleção."""

    def __init__(
        self,
        label: str,
        icon: str = "",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._label = label
        self._icon = icon
        self.setText(f"{icon}  {label}" if icon else label)
        self.setCursor(Qt.PointingHandCursor)
        self.setCheckable(True)
        self._apply_style()

    @property
    def label(self) -> str:
        return self._label

    @property
    def icon_text(self) -> str:
        return self._icon

    def set_collapsed(self, collapsed: bool) -> None:
        """Mostra apenas ícone quando a sidebar está recolhida."""
        if collapsed and self._icon:
            self.setText(self._icon)
        else:
            self.setText(f"{self._icon}  {self._label}" if self._icon else self._label)

    def _apply_style(self) -> None:
        self.setStyleSheet(
            """
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 8px;
                padding: 12px 16px;
                text-align: left;
                font-size: 14px;
            }
            QPushButton:hover {
                background: rgba(128, 128, 128, 0.15);
            }
            QPushButton:checked {
                background: #0078D4;
                color: white;
            }
            """
        )


class Sidebar(BaseComponent):
    """
    Componente de navegação lateral data-driven.

    Fluxo de uso:

        sidebar = Sidebar(parent)
        sidebar.set_items([
            SidebarMenuItem(PageId.HOME, "Início", "🏠"),
            SidebarMenuItem(PageId.SETTINGS, "Configurações", "⚙️"),
        ])

    Props:
        collapsed: Se inicia recolhida.
        width: Largura quando expandida.
    """

    item_clicked = Signal(object)  # PageId
    collapse_toggled = Signal(bool)

    def __init__(self, parent: QWidget | None = None, **kwargs) -> None:
        kwargs.setdefault("collapsed", False)

        kwargs.setdefault("width", 250)

        super().__init__(parent, **kwargs)
        self._active_page: PageId | None = None
        self._items: dict[PageId, _SidebarButton] = {}
        self._setup_navigation_listener()

    # -------------------------------------------------------- construção

    def _setup_ui(self) -> None:
        self.setProperty("class", "sidebar")
        self.setFixedWidth(self.get_prop("width", 250))

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(12, 16, 12, 16)
        self._layout.setSpacing(8)

        # Branding
        brand_frame = QFrame()
        brand_layout = QVBoxLayout(brand_frame)
        brand_layout.setContentsMargins(8, 0, 8, 16)

        app_name = QLabel("PySide6 App")
        app_name.setStyleSheet("font-size: 16px; font-weight: bold;")
        app_name.setProperty("class", "sidebar-title")
        brand_layout.addWidget(app_name)

        version = QLabel("v1.0.0")
        version.setStyleSheet("font-size: 11px;")
        version.setProperty("class", "sidebar-subtitle")
        brand_layout.addWidget(version)

        self._layout.addWidget(brand_frame)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setProperty("class", "sidebar-separator")
        separator.setFixedHeight(1)
        self._layout.addWidget(separator)

        self._nav_label = QLabel("Navegação")
        self._nav_label.setStyleSheet("font-size: 11px; margin-top: 8px;")
        self._nav_label.setProperty("class", "sidebar-section")
        self._layout.addWidget(self._nav_label)

        # Placeholder onde os itens serão inseridos (antes do stretch)
        self._items_container = QWidget()
        self._items_layout = QVBoxLayout(self._items_container)
        self._items_layout.setContentsMargins(0, 0, 0, 0)
        self._items_layout.setSpacing(4)
        self._layout.addWidget(self._items_container)

        self._layout.addStretch()

        # Botão de collapse
        self._collapse_btn = QPushButton("«")
        self._collapse_btn.setFixedHeight(32)
        self._collapse_btn.setCursor(Qt.PointingHandCursor)
        self._collapse_btn.setToolTip("Recolher sidebar")
        self._collapse_btn.setProperty("class", "sidebar-collapse")
        self._collapse_btn.setStyleSheet(
            """
            QPushButton {
                background: transparent;
                border: 1px solid rgba(128, 128, 128, 0.3);
                border-radius: 4px;
            }
            QPushButton:hover {
                background: rgba(128, 128, 128, 0.15);
            }
            """
        )
        self._collapse_btn.clicked.connect(self._toggle_collapse)
        self._layout.addWidget(self._collapse_btn)

    # ---------------------------------------------------------- API pública

    def set_items(self, items: list[SidebarMenuItem]) -> None:
        """
        Substitui os itens da sidebar.

        Chame este método do `MainWindow` após criar a sidebar,
        passando a lista derivada de `FEATURE_METADATA`.
        """
        # Remove itens atuais
        while self._items_layout.count():
            widget = self._items_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()
        self._items.clear()

        for item in items:
            button = _SidebarButton(item.label, item.icon)
            button.clicked.connect(
                lambda _checked=False, pid=item.page_id: self._on_item_clicked(pid)
            )
            self._items[item.page_id] = button
            self._items_layout.addWidget(button)

        self._update_active_item()

    def set_active(self, page_id: PageId) -> None:
        """Define externamente qual item está ativo."""
        self._active_page = page_id
        self._update_active_item()

    # ------------------------------------------------------------- eventos

    def _setup_navigation_listener(self) -> None:
        from src.services.navigation_service import NavigationService

        nav = container.resolve(NavigationService)
        nav.page_changed.connect(self._on_page_changed)

    def _on_item_clicked(self, page_id: PageId) -> None:
        self.item_clicked.emit(page_id)
        from src.services.navigation_service import NavigationService

        nav = container.resolve(NavigationService)
        nav.navigate_to(page_id)

    def _on_page_changed(self, page_id: PageId, params: dict) -> None:
        self._active_page = page_id
        self._update_active_item()

    def _update_active_item(self) -> None:
        for pid, button in self._items.items():
            button.setChecked(pid == self._active_page)

    def _toggle_collapse(self) -> None:
        collapsed = not self.get_prop("collapsed", False)
        self.set_prop("collapsed", collapsed)

        if collapsed:
            self.setFixedWidth(60)
            self._collapse_btn.setText("»")
            self._collapse_btn.setToolTip("Expandir sidebar")
            self._nav_label.setVisible(False)
        else:
            self.setFixedWidth(self.get_prop("width", 250))
            self._collapse_btn.setText("«")
            self._collapse_btn.setToolTip("Recolher sidebar")
            self._nav_label.setVisible(True)

        for button in self._items.values():
            button.set_collapsed(collapsed)

        self.collapse_toggled.emit(collapsed)
