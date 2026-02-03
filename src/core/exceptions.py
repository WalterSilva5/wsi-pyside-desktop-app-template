"""
Custom exception classes for the application.

This module defines a hierarchy of custom exceptions
for better error handling and debugging.
"""

from __future__ import annotations

from typing import Any


class AppException(Exception):
    """
    Base exception for all application-specific errors.

    Attributes:
        message: Human-readable error message
        code: Optional error code for programmatic handling
        details: Optional dictionary with additional error details
    """

    def __init__(
        self,
        message: str,
        code: str | None = None,
        details: dict[str, Any] | None = None
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}

    def __str__(self) -> str:
        if self.code:
            return f"[{self.code}] {self.message}"
        return self.message

    def to_dict(self) -> dict[str, Any]:
        """Convert exception to dictionary for serialization."""
        return {
            "type": self.__class__.__name__,
            "message": self.message,
            "code": self.code,
            "details": self.details,
        }


class ConfigurationError(AppException):
    """
    Raised when there's an error in configuration.

    Examples:
        - Missing required configuration key
        - Invalid configuration value
        - Configuration file not found
    """

    def __init__(
        self,
        message: str,
        key: str | None = None,
        details: dict[str, Any] | None = None
    ) -> None:
        super().__init__(message, code="CONFIG_ERROR", details=details)
        self.key = key


class NavigationError(AppException):
    """
    Raised when navigation fails.

    Examples:
        - Page not registered
        - Invalid navigation parameters
        - Navigation blocked by guard
    """

    def __init__(
        self,
        message: str,
        page_id: Any | None = None,
        details: dict[str, Any] | None = None
    ) -> None:
        super().__init__(message, code="NAV_ERROR", details=details)
        self.page_id = page_id


class ServiceError(AppException):
    """
    Raised when a service operation fails.

    Examples:
        - Service not initialized
        - Service dependency missing
        - Service operation timeout
    """

    def __init__(
        self,
        message: str,
        service_name: str | None = None,
        details: dict[str, Any] | None = None
    ) -> None:
        super().__init__(message, code="SERVICE_ERROR", details=details)
        self.service_name = service_name


class ValidationError(AppException):
    """
    Raised when validation fails.

    Examples:
        - Required field missing
        - Invalid field format
        - Value out of range
    """

    def __init__(
        self,
        message: str,
        field: str | None = None,
        value: Any = None,
        details: dict[str, Any] | None = None
    ) -> None:
        super().__init__(message, code="VALIDATION_ERROR", details=details)
        self.field = field
        self.value = value


class RepositoryError(AppException):
    """
    Raised when a repository operation fails.

    Examples:
        - Entity not found
        - Duplicate entity
        - Storage access error
    """

    def __init__(
        self,
        message: str,
        entity_type: str | None = None,
        entity_id: str | None = None,
        details: dict[str, Any] | None = None
    ) -> None:
        super().__init__(message, code="REPO_ERROR", details=details)
        self.entity_type = entity_type
        self.entity_id = entity_id


class ComponentError(AppException):
    """
    Raised when a UI component encounters an error.

    Examples:
        - Component not found
        - Invalid component props
        - Component rendering error
    """

    def __init__(
        self,
        message: str,
        component_name: str | None = None,
        details: dict[str, Any] | None = None
    ) -> None:
        super().__init__(message, code="COMPONENT_ERROR", details=details)
        self.component_name = component_name
