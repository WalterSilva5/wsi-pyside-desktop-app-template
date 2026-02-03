"""
Core infrastructure module.

Contains fundamental components for the application:
- DI Container
- Event Bus (Signals)
- Custom Exceptions
- Type definitions
"""

from src.core.container import Container, container
from src.core.signals import EventBus, event_bus
from src.core.types import PageId, Theme
from src.core.exceptions import (
    AppException,
    ConfigurationError,
    NavigationError,
    ServiceError,
)

__all__ = [
    "Container",
    "container",
    "EventBus",
    "event_bus",
    "PageId",
    "Theme",
    "AppException",
    "ConfigurationError",
    "NavigationError",
    "ServiceError",
]
