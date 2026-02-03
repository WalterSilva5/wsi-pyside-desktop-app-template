"""
Home page controller.

Handles business logic for the home page.
"""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import Signal

from src.controllers.base import BaseController
from src.core.types import PageId


class HomeController(BaseController):
    """
    Controller for the home page.

    Handles:
    - Dashboard data loading
    - Quick actions
    - Navigation to other pages

    Usage:
        controller = HomeController()
        controller.load_dashboard_data()
    """

    # Signals
    dashboard_data_loaded = Signal(dict)
    welcome_message_changed = Signal(str)

    def __init__(self) -> None:
        """Initialize the home controller."""
        super().__init__()
        self._dashboard_data: dict[str, Any] = {}
        self._welcome_message = "Welcome to PySide6 App Template"

    def load_dashboard_data(self) -> None:
        """Load dashboard data."""
        try:
            self.set_loading(True)
            self.log_action("Loading dashboard data")

            # Simulate loading dashboard data
            self._dashboard_data = {
                "app_name": self.config.get("app.name", "PySide6 App"),
                "version": self.config.get("app.version", "1.0.0"),
                "theme": self.config.get("theme.current", "light"),
                "quick_stats": {
                    "pages": 3,
                    "components": 20,
                    "services": 5,
                },
                "recent_activities": [
                    "Application started",
                    "Theme loaded",
                    "Configuration initialized",
                ],
            }

            self.dashboard_data_loaded.emit(self._dashboard_data)
            self.data_changed.emit()

        except Exception as e:
            self.handle_error(e, "Failed to load dashboard data")
        finally:
            self.set_loading(False)

    def get_dashboard_data(self) -> dict[str, Any]:
        """Get the current dashboard data."""
        return self._dashboard_data

    def get_welcome_message(self) -> str:
        """Get the welcome message."""
        return self._welcome_message

    def set_welcome_message(self, message: str) -> None:
        """Set the welcome message."""
        self._welcome_message = message
        self.welcome_message_changed.emit(message)

    def navigate_to_settings(self) -> None:
        """Navigate to settings page."""
        self.log_action("Navigating to settings")
        self.navigation.navigate_to(PageId.SETTINGS)

    def navigate_to_showcase(self) -> None:
        """Navigate to component showcase page."""
        self.log_action("Navigating to showcase")
        self.navigation.navigate_to(PageId.SHOWCASE)

    def refresh(self) -> None:
        """Refresh home page data."""
        self.log_action("Refreshing home page")
        self.load_dashboard_data()
