"""
Base view/page class.

Provides common functionality for all pages.
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Signal

from src.core.container import container
from src.core.signals import event_bus

if TYPE_CHECKING:
    from src.services.navigation_service import NavigationService
    from src.services.config_service import ConfigService
    from src.services.logger_service import LoggerService


class BasePage(QWidget):
    """
    Base class for all application pages.

    Provides:
    - Access to common services
    - Navigation helpers
    - Page lifecycle hooks
    - Common layout setup

    All pages should inherit from this class.
    """

    # Lifecycle signals
    page_shown = Signal()
    page_hidden = Signal()
    page_refreshed = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the page."""
        super().__init__(parent)
        self._params: dict[str, Any] = {}
        self._is_initialized = False
        self._setup_services()
        self._setup_base_layout()

    def _setup_services(self) -> None:
        """Setup references to common services."""
        from src.services.navigation_service import NavigationService
        from src.services.config_service import ConfigService
        from src.services.logger_service import LoggerService

        self._navigation = container.resolve(NavigationService)
        self._config = container.resolve(ConfigService)
        self._logger = container.resolve(LoggerService)

    def _setup_base_layout(self) -> None:
        """Setup the base layout structure."""
        self._main_layout = QVBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)

    @property
    def navigation(self) -> NavigationService:
        """Get the navigation service."""
        return self._navigation

    @property
    def config(self) -> ConfigService:
        """Get the config service."""
        return self._config

    @property
    def logger(self) -> LoggerService:
        """Get the logger service."""
        return self._logger

    @property
    def params(self) -> dict[str, Any]:
        """Get current navigation parameters."""
        return self._params

    def on_navigate(self, params: dict[str, Any]) -> None:
        """
        Called when navigating to this page.

        Override to handle navigation parameters.

        Args:
            params: Navigation parameters
        """
        self._params = params
        self._logger.debug(f"Navigated to {self.__class__.__name__} with params: {params}")

        if not self._is_initialized:
            self._is_initialized = True
            self.on_first_show()

        self.on_show()
        self.page_shown.emit()

    def on_first_show(self) -> None:
        """
        Called only on the first time the page is shown.

        Override to perform one-time initialization.
        """
        pass

    def on_show(self) -> None:
        """
        Called every time the page is shown.

        Override to refresh data or update UI.
        """
        pass

    def on_hide(self) -> None:
        """
        Called when leaving this page.

        Override to cleanup or save state.
        """
        self.page_hidden.emit()

    def refresh(self) -> None:
        """
        Refresh the page content.

        Override to implement refresh logic.
        """
        self.page_refreshed.emit()

    def navigate_to(self, page_id: Any, params: dict[str, Any] | None = None) -> None:
        """
        Navigate to another page.

        Args:
            page_id: Target page identifier
            params: Optional navigation parameters
        """
        self._navigation.navigate_to(page_id, params)

    def go_back(self) -> bool:
        """
        Navigate back.

        Returns:
            True if navigation successful
        """
        return self._navigation.go_back()

    def show_loading(self, show: bool = True) -> None:
        """
        Show or hide loading indicator.

        Override to implement custom loading UI.

        Args:
            show: Whether to show loading
        """
        if show:
            event_bus.loading_started.emit(self.__class__.__name__)
        else:
            event_bus.loading_finished.emit(self.__class__.__name__)

    def show_error(self, message: str) -> None:
        """
        Show an error message.

        Args:
            message: Error message
        """
        event_bus.error_occurred.emit("PageError", message)

    def show_toast(self, message: str, toast_type: str = "info") -> None:
        """
        Show a toast notification.

        Args:
            message: Toast message
            toast_type: Type (info, success, warning, error)
        """
        event_bus.toast_requested.emit(message, toast_type, 3000)
