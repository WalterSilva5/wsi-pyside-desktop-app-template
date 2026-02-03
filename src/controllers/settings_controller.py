"""
Settings page controller.

Handles business logic for the settings page.
"""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import Signal

from src.controllers.base import BaseController
from src.core.container import container
from src.core.types import Theme
from src.services.theme_service import ThemeService


class SettingsController(BaseController):
    """
    Controller for the settings page.

    Handles:
    - Settings loading and saving
    - Theme changes
    - Application preferences
    """

    # Signals
    settings_loaded = Signal(dict)
    settings_saved = Signal()
    theme_changed = Signal(str)

    def __init__(self) -> None:
        """Initialize the settings controller."""
        super().__init__()
        self._theme_service = container.resolve(ThemeService)
        self._current_settings: dict[str, Any] = {}

    def load_settings(self) -> dict[str, Any]:
        """Load all settings."""
        try:
            self.set_loading(True)
            self.log_action("Loading settings")

            self._current_settings = {
                "app": {
                    "name": self.config.get("app.name", "PySide6 App"),
                    "version": self.config.get("app.version", "1.0.0"),
                    "language": self.config.get("app.language", "en"),
                },
                "theme": {
                    "current": self.config.get("theme.current", "light"),
                    "follow_system": self.config.get("theme.follow_system", False),
                },
                "window": {
                    "width": self.config.get("window.width", 1200),
                    "height": self.config.get("window.height", 800),
                    "remember_size": self.config.get("window.remember_size", True),
                },
                "sidebar": {
                    "collapsed": self.config.get("sidebar.collapsed", False),
                    "width": self.config.get("sidebar.width", 250),
                },
            }

            self.settings_loaded.emit(self._current_settings)
            return self._current_settings

        except Exception as e:
            self.handle_error(e, "Failed to load settings")
            return {}
        finally:
            self.set_loading(False)

    def get_current_settings(self) -> dict[str, Any]:
        """Get the current settings."""
        return self._current_settings

    def save_settings(self, settings: dict[str, Any]) -> bool:
        """Save settings."""
        try:
            self.set_loading(True)
            self.log_action("Saving settings", settings)

            for section, values in settings.items():
                if isinstance(values, dict):
                    for key, value in values.items():
                        self.config.set(f"{section}.{key}", value)
                else:
                    self.config.set(section, values)

            self._current_settings = settings
            self.settings_saved.emit()
            return True

        except Exception as e:
            self.handle_error(e, "Failed to save settings")
            return False
        finally:
            self.set_loading(False)

    def get_theme(self) -> str:
        """Get current theme name."""
        return self._theme_service.get_current_theme().value

    def set_theme(self, theme_name: str) -> None:
        """Set application theme."""
        try:
            self.log_action("Changing theme", {"theme": theme_name})
            theme = Theme(theme_name)
            self._theme_service.set_theme(theme)
            self.config.set("theme.current", theme_name)
            self.theme_changed.emit(theme_name)
        except ValueError as e:
            self.handle_error(e, f"Invalid theme: {theme_name}")

    def toggle_theme(self) -> str:
        """Toggle between light and dark themes."""
        new_theme = self._theme_service.toggle_theme()
        theme_name = new_theme.value
        self.config.set("theme.current", theme_name)
        self.theme_changed.emit(theme_name)
        return theme_name

    def get_available_themes(self) -> list[dict[str, str]]:
        """Get list of available themes."""
        return [
            {"id": "light", "name": "Light", "description": "Light color scheme"},
            {"id": "dark", "name": "Dark", "description": "Dark color scheme"},
            {"id": "system", "name": "System", "description": "Follow system preference"},
        ]

    def reset_to_defaults(self) -> None:
        """Reset all settings to defaults."""
        try:
            self.log_action("Resetting settings to defaults")
            self.config.reset_to_defaults()
            self.load_settings()
        except Exception as e:
            self.handle_error(e, "Failed to reset settings")

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a specific setting."""
        return self.config.get(key, default)

    def set_setting(self, key: str, value: Any) -> None:
        """Set a specific setting."""
        self.config.set(key, value)
        self.data_changed.emit()
