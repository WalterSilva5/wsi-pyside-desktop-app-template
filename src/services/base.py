"""
Base service class.

Provides common functionality for all application services.
"""

from __future__ import annotations

from abc import ABC, ABCMeta
from typing import Any

from PySide6.QtCore import QObject


# Resolve metaclass conflict between QObject and ABC
class ServiceMeta(type(QObject), ABCMeta):
    """Combined metaclass for QObject and ABC."""
    pass


class BaseService(QObject, ABC, metaclass=ServiceMeta):
    """
    Abstract base class for all services.

    Provides common functionality:
    - Singleton pattern support
    - QObject inheritance for signals
    - Initialization tracking

    All services should inherit from this class.
    """

    _instances: dict[type, BaseService] = {}

    def __new__(cls) -> BaseService:
        """Ensure singleton instance per service type."""
        if cls not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[cls] = instance
        return cls._instances[cls]

    def __init__(self) -> None:
        """Initialize the service."""
        if hasattr(self, "_initialized"):
            return

        # Only call QObject.__init__ once
        if not hasattr(self, "_qobject_initialized"):
            super().__init__()
            self._qobject_initialized = True

        self._initialized = True
        self._on_init()

    def _on_init(self) -> None:
        """
        Called after initialization.

        Override this method in subclasses to perform
        service-specific initialization.
        """
        pass

    def dispose(self) -> None:
        """
        Cleanup resources.

        Override this method in subclasses to perform
        cleanup when the service is no longer needed.
        """
        pass

    @classmethod
    def reset_instance(cls) -> None:
        """
        Reset the singleton instance.

        Useful for testing.
        """
        if cls in cls._instances:
            del cls._instances[cls]
