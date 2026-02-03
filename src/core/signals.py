"""
Global Event Bus using Qt Signals.

Implements the Observer pattern for decoupled communication
between application components.
"""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import QObject, Signal

from src.core.types import PageId, Theme


class EventBus(QObject):
    """
    Global Event Bus for application-wide communication.

    Uses Qt Signals to implement the Observer pattern,
    allowing components to communicate without direct coupling.

    Usage:
        # Subscribe to an event
        event_bus.navigate_to.connect(my_handler)

        # Emit an event
        event_bus.navigate_to.emit(PageId.HOME, {})
    """

    _instance: EventBus | None = None

    # Navigation events
    navigate_to = Signal(object, dict)  # page_id: PageId, params: dict
    navigation_completed = Signal(object)  # page_id: PageId
    navigation_failed = Signal(object, str)  # page_id: PageId, error: str
    go_back_requested = Signal()

    # Theme events
    theme_changed = Signal(object)  # theme: Theme
    theme_change_requested = Signal(object)  # theme: Theme

    # User events
    user_logged_in = Signal(object)  # user data
    user_logged_out = Signal()
    user_updated = Signal(object)  # user data

    # Application lifecycle events
    app_ready = Signal()
    app_closing = Signal()
    app_minimized = Signal()
    app_restored = Signal()

    # Settings events
    settings_changed = Signal(str, object)  # key, value
    settings_saved = Signal()
    settings_loaded = Signal()

    # Error events
    error_occurred = Signal(str, str)  # error_type, message
    warning_occurred = Signal(str, str)  # warning_type, message

    # UI events
    loading_started = Signal(str)  # context
    loading_finished = Signal(str)  # context
    toast_requested = Signal(str, str, int)  # message, type, duration_ms
    dialog_requested = Signal(str, dict)  # dialog_type, params

    # Generic custom events
    custom_event = Signal(str, object)  # event_name, data

    def __new__(cls) -> EventBus:
        """Ensure singleton instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initialize the event bus."""
        if hasattr(self, "_initialized"):
            return
        super().__init__()
        self._initialized = True

    def emit_navigation(self, page_id: PageId, params: dict[str, Any] | None = None) -> None:
        """
        Convenience method to emit navigation event.

        Args:
            page_id: Target page identifier
            params: Optional navigation parameters
        """
        self.navigate_to.emit(page_id, params or {})

    def emit_theme_change(self, theme: Theme) -> None:
        """
        Convenience method to request theme change.

        Args:
            theme: Target theme
        """
        self.theme_change_requested.emit(theme)

    def emit_toast(
        self,
        message: str,
        toast_type: str = "info",
        duration_ms: int = 3000
    ) -> None:
        """
        Convenience method to show a toast notification.

        Args:
            message: Toast message
            toast_type: Type of toast (info, success, warning, error)
            duration_ms: Display duration in milliseconds
        """
        self.toast_requested.emit(message, toast_type, duration_ms)

    def emit_error(self, error_type: str, message: str) -> None:
        """
        Convenience method to emit an error event.

        Args:
            error_type: Type/category of error
            message: Error message
        """
        self.error_occurred.emit(error_type, message)

    def emit_custom(self, event_name: str, data: Any = None) -> None:
        """
        Emit a custom event.

        Args:
            event_name: Name of the custom event
            data: Event data
        """
        self.custom_event.emit(event_name, data)


# Global event bus instance
event_bus = EventBus()
