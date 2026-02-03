"""
Main Application class.

Handles application initialization, service registration,
and lifecycle management.
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from PySide6.QtWidgets import QApplication

from src.core.container import container
from src.core.signals import event_bus

if TYPE_CHECKING:
    from src.views.main_window import MainWindow


class Application:
    """
    Main application class.

    Responsible for:
    - Initializing the Qt application
    - Registering services in the DI container
    - Setting up the main window
    - Managing application lifecycle

    Usage:
        app = Application()
        app.run()
    """

    _instance: Application | None = None

    def __new__(cls) -> Application:
        """Ensure singleton instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initialize the application."""
        if hasattr(self, "_initialized"):
            return

        self._initialized = True
        self._qt_app: QApplication | None = None
        self._main_window: MainWindow | None = None

    def _create_qt_app(self) -> QApplication:
        """Create and configure the Qt application instance."""
        app = QApplication(sys.argv)
        app.setApplicationName("PySide6 App Template")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("WSI")
        app.setOrganizationDomain("wsi.dev")

        # Use Fusion style for consistent cross-platform appearance
        app.setStyle("Fusion")

        return app

    def _register_services(self) -> None:
        """Register all services in the DI container."""
        from src.services.logger_service import LoggerService
        from src.services.config_service import ConfigService
        from src.services.theme_service import ThemeService
        from src.services.navigation_service import NavigationService
        from src.services.storage_service import StorageService

        # Register services as singletons
        container.register_singleton(LoggerService)
        container.register_singleton(ConfigService)
        container.register_singleton(ThemeService)
        container.register_singleton(NavigationService)
        container.register_singleton(StorageService)

        # Initialize logger first
        logger = container.resolve(LoggerService)
        logger.info("Services registered successfully")

    def _initialize_services(self) -> None:
        """Initialize all registered services."""
        from src.services.logger_service import LoggerService
        from src.services.config_service import ConfigService
        from src.services.theme_service import ThemeService
        from src.core.types import Theme

        logger = container.resolve(LoggerService)

        # Initialize config
        config = container.resolve(ConfigService)
        logger.info("Configuration loaded")

        # Initialize theme from config
        theme_service = container.resolve(ThemeService)
        theme_name = config.get("theme.current", "light")
        follow_system = config.get("theme.follow_system", False)

        if follow_system:
            theme_service.set_theme(Theme.SYSTEM)
        else:
            theme = Theme.DARK if theme_name == "dark" else Theme.LIGHT
            theme_service.set_theme(theme)

        logger.info(f"Theme applied: {theme_service.get_current_theme().value}")

    def _create_main_window(self) -> MainWindow:
        """Create and configure the main window."""
        from src.views.main_window import MainWindow
        from src.services.logger_service import LoggerService

        logger = container.resolve(LoggerService)

        window = MainWindow()
        logger.info("Main window created")

        return window

    def _setup_signal_handlers(self) -> None:
        """Setup global signal handlers."""
        from src.services.logger_service import LoggerService

        logger = container.resolve(LoggerService)

        # Log errors
        event_bus.error_occurred.connect(
            lambda error_type, message: logger.error(f"{error_type}: {message}")
        )

        # Log warnings
        event_bus.warning_occurred.connect(
            lambda warning_type, message: logger.warning(f"{warning_type}: {message}")
        )

    def initialize(self) -> None:
        """
        Initialize the application.

        This method sets up all necessary components before running.
        """
        # Create Qt application
        self._qt_app = self._create_qt_app()

        # Register and initialize services
        self._register_services()
        self._initialize_services()

        # Setup signal handlers
        self._setup_signal_handlers()

        # Create main window
        self._main_window = self._create_main_window()

        # Emit app ready signal
        event_bus.app_ready.emit()

    def run(self) -> int:
        """
        Run the application.

        Returns:
            Application exit code
        """
        if self._qt_app is None or self._main_window is None:
            self.initialize()

        # Show main window
        if self._main_window:
            self._main_window.show()

        # Run event loop
        if self._qt_app:
            return self._qt_app.exec()

        return 1

    def quit(self) -> None:
        """Quit the application gracefully."""
        event_bus.app_closing.emit()

        if self._qt_app:
            self._qt_app.quit()

    @property
    def qt_app(self) -> QApplication | None:
        """Get the Qt application instance."""
        return self._qt_app

    @property
    def main_window(self) -> MainWindow | None:
        """Get the main window instance."""
        return self._main_window


def main() -> int:
    """
    Application entry point.

    Returns:
        Application exit code
    """
    app = Application()
    return app.run()
