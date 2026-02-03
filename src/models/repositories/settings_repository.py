"""
Settings repository implementation.

Provides data access for AppSettings.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from src.models.settings import AppSettings
from src.core.exceptions import RepositoryError


class SettingsRepository:
    """
    Repository for AppSettings.

    Unlike other repositories, this manages a single settings instance
    rather than a collection of entities.

    Usage:
        repo = SettingsRepository()
        settings = repo.get()
        settings.theme.current = "dark"
        repo.save(settings)
    """

    def __init__(self, file_path: Path | None = None) -> None:
        """
        Initialize the settings repository.

        Args:
            file_path: Optional custom path. Uses default if not provided.
        """
        if file_path is None:
            file_path = self._get_default_path()
        self._file_path = file_path
        self._settings: AppSettings | None = None
        self._ensure_file()

    def _get_default_path(self) -> Path:
        """Get the default storage path."""
        if sys.platform == "win32":
            base = Path.home() / "AppData" / "Local"
        elif sys.platform == "darwin":
            base = Path.home() / "Library" / "Application Support"
        else:
            base = Path.home() / ".config"

        return base / "PySide6AppTemplate" / "settings.json"

    def _ensure_file(self) -> None:
        """Ensure the storage file and directory exist."""
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self._file_path.exists():
            self._settings = AppSettings()
            self.save(self._settings)

    def get(self) -> AppSettings:
        """
        Get the current settings.

        Returns:
            AppSettings instance
        """
        if self._settings is None:
            self._load()
        return self._settings or AppSettings()

    def save(self, settings: AppSettings) -> None:
        """
        Save settings to file.

        Args:
            settings: Settings to save
        """
        try:
            self._file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self._file_path, "w", encoding="utf-8") as f:
                json.dump(settings.to_dict(), f, indent=2, ensure_ascii=False)
            self._settings = settings
        except IOError as e:
            raise RepositoryError(
                f"Failed to save settings: {e}",
                entity_type="AppSettings"
            )

    def _load(self) -> None:
        """Load settings from file."""
        try:
            if self._file_path.exists():
                with open(self._file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._settings = AppSettings.from_dict(data)
            else:
                self._settings = AppSettings()
        except (json.JSONDecodeError, IOError) as e:
            # If loading fails, use defaults
            self._settings = AppSettings()

    def reset(self) -> AppSettings:
        """
        Reset settings to defaults.

        Returns:
            New default settings
        """
        self._settings = AppSettings()
        self.save(self._settings)
        return self._settings

    def update(self, **kwargs: Any) -> AppSettings:
        """
        Update specific settings.

        Args:
            **kwargs: Settings to update (dot notation supported)

        Returns:
            Updated settings
        """
        settings = self.get()

        for key, value in kwargs.items():
            parts = key.split(".")
            target = settings

            # Navigate to the target attribute
            for part in parts[:-1]:
                target = getattr(target, part)

            # Set the value
            setattr(target, parts[-1], value)

        settings.touch()
        self.save(settings)
        return settings

    def get_value(self, key: str, default: Any = None) -> Any:
        """
        Get a specific setting value using dot notation.

        Args:
            key: Setting key (e.g., "theme.current")
            default: Default value if not found

        Returns:
            Setting value or default
        """
        settings = self.get()
        parts = key.split(".")

        try:
            value = settings
            for part in parts:
                value = getattr(value, part)
            return value
        except AttributeError:
            return default

    def set_value(self, key: str, value: Any) -> None:
        """
        Set a specific setting value using dot notation.

        Args:
            key: Setting key (e.g., "theme.current")
            value: Value to set
        """
        self.update(**{key: value})

    @property
    def file_path(self) -> Path:
        """Get the file path."""
        return self._file_path
