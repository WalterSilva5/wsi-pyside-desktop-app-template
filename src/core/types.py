"""
Type definitions and enumerations for the application.

This module contains all custom types, enums, and type aliases
used throughout the application.
"""

from __future__ import annotations

from enum import Enum, auto
from typing import Any, Callable, TypeVar

# Type variables for generics
T = TypeVar("T")
WidgetT = TypeVar("WidgetT")


class PageId(Enum):
    """
    Enumeration of all page identifiers.

    Used for type-safe navigation instead of string-based page names.
    Add new pages here when creating additional screens.
    """
    HOME = auto()
    SETTINGS = auto()
    SHOWCASE = auto()
    RESPONSIVE = auto()


class Theme(Enum):
    """
    Available application themes.

    Attributes:
        LIGHT: Light color scheme
        DARK: Dark color scheme
        SYSTEM: Follow system preference
    """
    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"


class ButtonSize(Enum):
    """Button size variants."""
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class ButtonVariant(Enum):
    """Button style variants."""
    PRIMARY = "primary"
    SECONDARY = "secondary"
    OUTLINE = "outline"
    GHOST = "ghost"
    DANGER = "danger"


class CardElevation(Enum):
    """Card shadow elevation levels."""
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    HIGHEST = 4


class ToastType(Enum):
    """Toast notification types."""
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


class DialogResult(Enum):
    """Dialog result values."""
    ACCEPTED = auto()
    REJECTED = auto()
    CANCELLED = auto()


class InputValidationState(Enum):
    """Input field validation states."""
    VALID = "valid"
    INVALID = "invalid"
    PENDING = "pending"
    NONE = "none"


# Type aliases for common callback signatures
NavigationCallback = Callable[[PageId, dict[str, Any]], None]
EventCallback = Callable[[str, Any], None]
ValidationCallback = Callable[[str], bool]
