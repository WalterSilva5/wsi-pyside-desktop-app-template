"""
Configuration Service.

Manages application settings with JSON persistence.
Implements the Singleton pattern.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from PySide6.QtCore import Signal

from src.services.base import BaseService


class ConfigService(BaseService):
    """
    Singleton Configuration Service.

    Manages application settings with:
    - JSON file persistence
    - Dot notation for nested keys
    - Change notifications via signals
    - Default values support

    Usage:
        config = ConfigService()

        # Get a value
        theme = config.get("app.theme", "light")

        # Set a value
        config.set("app.theme", "dark")

        # Listen to changes
        config.settings_changed.connect(my_handler)
    """

    # Signals
    settings_changed = Signal(str, object)  # key, value
    settings_loaded = Signal()
    settings_saved = Signal()

    def _on_init(self) -> None:
        """Initialize the configuration service."""
        self._settings: dict[str, Any] = {}
        self._config_dir = self._get_config_directory()
        self._config_path = self._config_dir / "settings.json"
        self._load_settings()

    def _get_config_directory(self) -> Path:
        """Get the configuration directory path."""
        if sys.platform == "win32":
            base = Path.home() / "AppData" / "Local"
        elif sys.platform == "darwin":
            base = Path.home() / "Library" / "Application Support"
        else:
            base = Path.home() / ".config"

        return base / "PySide6AppTemplate"

    def _load_settings(self) -> None:
        """Load settings from JSON file."""
        if self._config_path.exists():
            try:
                with open(self._config_path, "r", encoding="utf-8") as f:
                    self._settings = json.load(f)
                self.settings_loaded.emit()
            except (json.JSONDecodeError, IOError):
                self._load_defaults()
        else:
            self._load_defaults()

    def _load_defaults(self) -> None:
        """Load default settings from resources."""
        # Try to load from resources
        default_path = Path(__file__).parent.parent.parent / "resources" / "config" / "default_settings.json"

        if default_path.exists():
            try:
                with open(default_path, "r", encoding="utf-8") as f:
                    self._settings = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._settings = self._get_hardcoded_defaults()
        else:
            self._settings = self._get_hardcoded_defaults()

        # Save defaults to user config
        self.save()

    def _get_hardcoded_defaults(self) -> dict[str, Any]:
        """Get hardcoded default settings."""
        return {
            "app": {
                "name": "PySide6 App Template",
                "version": "1.0.0",
                "language": "en",
            },
            "window": {
                "width": 1200,
                "height": 800,
                "min_width": 800,
                "min_height": 600,
                "remember_size": True,
                "remember_position": True,
            },
            "theme": {
                "current": "light",
                "follow_system": False,
            },
            "sidebar": {
                "collapsed": False,
                "width": 250,
            },
        }

    def save(self) -> None:
        """Persist settings to JSON file."""
        self._config_dir.mkdir(parents=True, exist_ok=True)
        try:
            with open(self._config_path, "w", encoding="utf-8") as f:
                json.dump(self._settings, f, indent=2, ensure_ascii=False)
            self.settings_saved.emit()
        except IOError as e:
            raise IOError(f"Failed to save settings: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a setting value using dot notation.

        Args:
            key: Setting key (e.g., "app.theme" or "window.width")
            default: Default value if key not found

        Returns:
            The setting value or default
        """
        keys = key.split(".")
        value = self._settings

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any, save: bool = True) -> None:
        """
        Set a setting value using dot notation.

        Args:
            key: Setting key (e.g., "app.theme")
            value: Value to set
            save: Whether to persist immediately
        """
        keys = key.split(".")
        target = self._settings

        # Navigate to parent
        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            target = target[k]

        # Set value
        target[keys[-1]] = value

        # Emit change signal
        self.settings_changed.emit(key, value)

        # Save if requested
        if save:
            self.save()

    def has(self, key: str) -> bool:
        """
        Check if a setting key exists.

        Args:
            key: Setting key to check

        Returns:
            True if key exists, False otherwise
        """
        return self.get(key) is not None

    def remove(self, key: str, save: bool = True) -> bool:
        """
        Remove a setting.

        Args:
            key: Setting key to remove
            save: Whether to persist immediately

        Returns:
            True if removed, False if not found
        """
        keys = key.split(".")
        target = self._settings

        # Navigate to parent
        for k in keys[:-1]:
            if k not in target:
                return False
            target = target[k]

        # Remove key
        if keys[-1] in target:
            del target[keys[-1]]
            if save:
                self.save()
            return True

        return False

    def get_all(self) -> dict[str, Any]:
        """
        Get all settings.

        Returns:
            Copy of all settings
        """
        return self._settings.copy()

    def reset_to_defaults(self) -> None:
        """Reset all settings to defaults."""
        self._settings = self._get_hardcoded_defaults()
        self.save()
        self.settings_loaded.emit()

    @property
    def config_path(self) -> Path:
        """Get the configuration file path."""
        return self._config_path
