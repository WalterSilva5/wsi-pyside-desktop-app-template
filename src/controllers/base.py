"""
Base controller class.

Provides common functionality for all controllers.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from PySide6.QtCore import QObject, Signal

from src.core.container import container
from src.core.signals import event_bus

if TYPE_CHECKING:
    from src.services.logger_service import LoggerService
    from src.services.config_service import ConfigService
    from src.services.navigation_service import NavigationService


class BaseController(QObject):
    """
    Base class for all controllers.

    Provides:
    - Access to common services via DI container
    - Standard error handling
    - Logging integration
    - Signal definitions for view updates

    Controllers handle business logic and coordinate
    between views and services/models.
    """

    # Common signals
    loading_started = Signal()
    loading_finished = Signal()
    error_occurred = Signal(str)  # error message
    data_changed = Signal()

    def __init__(self, parent: QObject | None = None) -> None:
        """Initialize the controller."""
        super().__init__(parent)
        self._is_loading = False
        self._setup_services()

    def _setup_services(self) -> None:
        """Setup references to common services."""
        from src.services.logger_service import LoggerService
        from src.services.config_service import ConfigService
        from src.services.navigation_service import NavigationService

        self._logger = container.resolve(LoggerService)
        self._config = container.resolve(ConfigService)
        self._navigation = container.resolve(NavigationService)

    @property
    def logger(self) -> LoggerService:
        """Get the logger service."""
        return self._logger

    @property
    def config(self) -> ConfigService:
        """Get the config service."""
        return self._config

    @property
    def navigation(self) -> NavigationService:
        """Get the navigation service."""
        return self._navigation

    def set_loading(self, loading: bool) -> None:
        """
        Set loading state.

        Args:
            loading: Whether loading is in progress
        """
        self._is_loading = loading
        if loading:
            self.loading_started.emit()
        else:
            self.loading_finished.emit()

    @property
    def is_loading(self) -> bool:
        """Check if loading is in progress."""
        return self._is_loading

    def handle_error(self, error: Exception, context: str = "") -> None:
        """
        Handle an error.

        Args:
            error: The exception that occurred
            context: Optional context description
        """
        message = str(error)
        if context:
            message = f"{context}: {message}"

        self._logger.error(message, exc_info=True)
        self.error_occurred.emit(message)
        event_bus.error_occurred.emit(type(error).__name__, message)

    def log_action(self, action: str, details: dict[str, Any] | None = None) -> None:
        """
        Log a user action.

        Args:
            action: Action description
            details: Optional action details
        """
        if details:
            self._logger.info(f"{action}: {details}")
        else:
            self._logger.info(action)
