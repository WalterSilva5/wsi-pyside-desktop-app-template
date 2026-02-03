"""
Application settings model.

Represents application settings as a structured model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from src.models.base import BaseModel
from src.core.types import Theme


@dataclass
class WindowSettings:
    """Window configuration settings."""
    width: int = 1200
    height: int = 800
    min_width: int = 800
    min_height: int = 600
    x: int | None = None
    y: int | None = None
    is_maximized: bool = False
    remember_size: bool = True
    remember_position: bool = True


@dataclass
class ThemeSettings:
    """Theme configuration settings."""
    current: str = "light"
    follow_system: bool = False

    @property
    def theme(self) -> Theme:
        """Get current theme as enum."""
        try:
            return Theme(self.current)
        except ValueError:
            return Theme.LIGHT


@dataclass
class SidebarSettings:
    """Sidebar configuration settings."""
    collapsed: bool = False
    width: int = 250


@dataclass
class LoggingSettings:
    """Logging configuration settings."""
    level: str = "INFO"
    file_enabled: bool = True
    console_enabled: bool = True


@dataclass
class NavigationSettings:
    """Navigation configuration settings."""
    default_page: str = "home"
    remember_last_page: bool = True
    last_page: str | None = None


@dataclass
class AppSettings(BaseModel):
    """
    Application settings model.

    Structured representation of all application settings.

    Usage:
        settings = AppSettings()
        settings.theme.current = "dark"
        settings.window.width = 1400
    """

    app_name: str = "PySide6 App Template"
    app_version: str = "1.0.0"
    language: str = "en"

    window: WindowSettings = field(default_factory=WindowSettings)
    theme: ThemeSettings = field(default_factory=ThemeSettings)
    sidebar: SidebarSettings = field(default_factory=SidebarSettings)
    logging: LoggingSettings = field(default_factory=LoggingSettings)
    navigation: NavigationSettings = field(default_factory=NavigationSettings)

    # Custom user settings
    custom: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "app": {
                "name": self.app_name,
                "version": self.app_version,
                "language": self.language,
            },
            "window": {
                "width": self.window.width,
                "height": self.window.height,
                "min_width": self.window.min_width,
                "min_height": self.window.min_height,
                "x": self.window.x,
                "y": self.window.y,
                "is_maximized": self.window.is_maximized,
                "remember_size": self.window.remember_size,
                "remember_position": self.window.remember_position,
            },
            "theme": {
                "current": self.theme.current,
                "follow_system": self.theme.follow_system,
            },
            "sidebar": {
                "collapsed": self.sidebar.collapsed,
                "width": self.sidebar.width,
            },
            "logging": {
                "level": self.logging.level,
                "file_enabled": self.logging.file_enabled,
                "console_enabled": self.logging.console_enabled,
            },
            "navigation": {
                "default_page": self.navigation.default_page,
                "remember_last_page": self.navigation.remember_last_page,
                "last_page": self.navigation.last_page,
            },
            "custom": self.custom,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AppSettings:
        """Create from dictionary."""
        from datetime import datetime

        settings = cls()

        # Base fields
        if "id" in data:
            settings.id = data["id"]
        if "created_at" in data:
            settings.created_at = datetime.fromisoformat(data["created_at"])
        if "updated_at" in data:
            settings.updated_at = datetime.fromisoformat(data["updated_at"])

        # App section
        app = data.get("app", {})
        settings.app_name = app.get("name", settings.app_name)
        settings.app_version = app.get("version", settings.app_version)
        settings.language = app.get("language", settings.language)

        # Window section
        window = data.get("window", {})
        settings.window = WindowSettings(
            width=window.get("width", 1200),
            height=window.get("height", 800),
            min_width=window.get("min_width", 800),
            min_height=window.get("min_height", 600),
            x=window.get("x"),
            y=window.get("y"),
            is_maximized=window.get("is_maximized", False),
            remember_size=window.get("remember_size", True),
            remember_position=window.get("remember_position", True),
        )

        # Theme section
        theme = data.get("theme", {})
        settings.theme = ThemeSettings(
            current=theme.get("current", "light"),
            follow_system=theme.get("follow_system", False),
        )

        # Sidebar section
        sidebar = data.get("sidebar", {})
        settings.sidebar = SidebarSettings(
            collapsed=sidebar.get("collapsed", False),
            width=sidebar.get("width", 250),
        )

        # Logging section
        logging_data = data.get("logging", {})
        settings.logging = LoggingSettings(
            level=logging_data.get("level", "INFO"),
            file_enabled=logging_data.get("file_enabled", True),
            console_enabled=logging_data.get("console_enabled", True),
        )

        # Navigation section
        navigation = data.get("navigation", {})
        settings.navigation = NavigationSettings(
            default_page=navigation.get("default_page", "home"),
            remember_last_page=navigation.get("remember_last_page", True),
            last_page=navigation.get("last_page"),
        )

        # Custom section
        settings.custom = data.get("custom", {})

        return settings

    def get_custom(self, key: str, default: Any = None) -> Any:
        """Get a custom setting."""
        return self.custom.get(key, default)

    def set_custom(self, key: str, value: Any) -> None:
        """Set a custom setting."""
        self.custom[key] = value
        self.touch()

    def touch(self) -> None:
        """Update the updated_at timestamp."""
        from datetime import datetime
        self.updated_at = datetime.now()
