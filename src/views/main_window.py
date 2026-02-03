"""
Main application window.

The root window that contains the navigation stack and layout.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QStackedWidget,
)
from PySide6.QtCore import Qt

from src.core.container import container
from src.core.signals import event_bus
from src.core.types import PageId
from src.services.navigation_service import NavigationService
from src.services.config_service import ConfigService
from src.services.theme_service import ThemeService


class MainWindow(QMainWindow):
    """
    Main application window.

    Features:
    - Navigation stack for page management
    - Sidebar for navigation
    - Header with common actions
    - Theme support

    The window uses the NavigationService for page management
    instead of direct page switching.
    """

    def __init__(self) -> None:
        """Initialize the main window."""
        super().__init__()

        self._setup_services()
        self._setup_window()
        self._setup_ui()
        self._setup_pages()
        self._setup_connections()

        # Navigate to default page
        self._navigation.navigate_to(PageId.HOME)

    def _setup_services(self) -> None:
        """Setup service references."""
        self._navigation = container.resolve(NavigationService)
        self._config = container.resolve(ConfigService)
        self._theme_service = container.resolve(ThemeService)

    def _setup_window(self) -> None:
        """Setup window properties."""
        self.setWindowTitle(self._config.get("app.name", "PySide6 App Template"))

        # Window size
        width = self._config.get("window.width", 1200)
        height = self._config.get("window.height", 800)
        min_width = self._config.get("window.min_width", 800)
        min_height = self._config.get("window.min_height", 600)

        self.resize(width, height)
        self.setMinimumSize(min_width, min_height)

        # Center on screen
        self._center_on_screen()

    def _center_on_screen(self) -> None:
        """Center the window on the screen."""
        screen = self.screen()
        if screen:
            screen_geometry = screen.availableGeometry()
            x = (screen_geometry.width() - self.width()) // 2
            y = (screen_geometry.height() - self.height()) // 2
            self.move(x, y)

    def _setup_ui(self) -> None:
        """Setup the main UI structure."""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self._sidebar = self._create_sidebar()
        main_layout.addWidget(self._sidebar)

        # Content area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Header
        self._header = self._create_header()
        content_layout.addWidget(self._header)

        # Page stack
        self._stack = QStackedWidget()
        content_layout.addWidget(self._stack, 1)

        main_layout.addWidget(content_widget, 1)

        # Set stack widget for navigation service
        self._navigation.set_stack_widget(self._stack)

    def _create_sidebar(self) -> QWidget:
        """Create the sidebar widget."""
        from src.views.components.layout.sidebar import Sidebar
        return Sidebar(self)

    def _create_header(self) -> QWidget:
        """Create the header widget."""
        from src.views.components.layout.header import Header
        return Header(
            title=self._config.get("app.name", "PySide6 App"),
            parent=self
        )

    def _setup_pages(self) -> None:
        """Setup and register all pages."""
        from src.views.pages.home_page import HomePage
        from src.views.pages.settings_page import SettingsPage
        from src.views.pages.showcase_page import ShowcasePage
        from src.views.pages.responsive_page import ResponsivePage

        # Create pages
        self._home_page = HomePage(self)
        self._settings_page = SettingsPage(self)
        self._showcase_page = ShowcasePage(self)
        self._responsive_page = ResponsivePage(self)

        # Register with navigation service
        self._navigation.register_page(PageId.HOME, self._home_page, is_default=True)
        self._navigation.register_page(PageId.SETTINGS, self._settings_page)
        self._navigation.register_page(PageId.SHOWCASE, self._showcase_page)
        self._navigation.register_page(PageId.RESPONSIVE, self._responsive_page)

    def _setup_connections(self) -> None:
        """Setup signal connections."""
        # Navigation events
        self._navigation.page_changed.connect(self._on_page_changed)

        # Theme events
        event_bus.theme_change_requested.connect(self._on_theme_change_requested)

        # App events
        event_bus.app_closing.connect(self._on_app_closing)

    def _on_page_changed(self, page_id: PageId, params: dict) -> None:
        """Handle page change."""
        # Update header title based on page
        titles = {
            PageId.HOME: "Home",
            PageId.SETTINGS: "Settings",
            PageId.SHOWCASE: "Component Showcase",
            PageId.RESPONSIVE: "Responsive Grid",
        }
        if hasattr(self, '_header') and hasattr(self._header, 'set_title'):
            self._header.set_title(titles.get(page_id, ""))

    def _on_theme_change_requested(self, theme) -> None:
        """Handle theme change request."""
        self._theme_service.set_theme(theme)

    def _on_app_closing(self) -> None:
        """Handle app closing event."""
        # Save window state
        if self._config.get("window.remember_size", True):
            self._config.set("window.width", self.width())
            self._config.set("window.height", self.height())

        if self._config.get("window.remember_position", True):
            pos = self.pos()
            self._config.set("window.x", pos.x())
            self._config.set("window.y", pos.y())

    def closeEvent(self, event) -> None:
        """Handle window close event."""
        event_bus.app_closing.emit()
        super().closeEvent(event)

    # Public API for compatibility
    def change_page(self, page: str) -> None:
        """
        Change to a page by name.

        Deprecated: Use navigation service directly.

        Args:
            page: Page name (home, settings, showcase, responsive)
        """
        page_map = {
            "home": PageId.HOME,
            "settings": PageId.SETTINGS,
            "showcase": PageId.SHOWCASE,
            "responsive": PageId.RESPONSIVE,
        }
        page_id = page_map.get(page, PageId.HOME)
        self._navigation.navigate_to(page_id)
