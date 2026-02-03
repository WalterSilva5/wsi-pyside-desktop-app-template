"""
User model.

Represents a user in the application.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from src.models.base import BaseModel
from src.core.exceptions import ValidationError


@dataclass
class User(BaseModel):
    """
    User model.

    Attributes:
        name: User's full name
        email: User's email address
        username: User's username (optional)
        avatar_url: URL to user's avatar (optional)
        preferences: User-specific preferences
        is_active: Whether user is active

    Usage:
        user = User(name="John Doe", email="john@example.com")
    """

    name: str = ""
    email: str = ""
    username: str = ""
    avatar_url: str = ""
    preferences: dict[str, Any] = field(default_factory=dict)
    is_active: bool = True

    def validate(self) -> None:
        """Validate user data."""
        super().validate()

        if not self.name:
            raise ValidationError("Name is required", field="name")

        if not self.email:
            raise ValidationError("Email is required", field="email")

        if "@" not in self.email:
            raise ValidationError("Invalid email format", field="email", value=self.email)

    def get_preference(self, key: str, default: Any = None) -> Any:
        """
        Get a user preference.

        Args:
            key: Preference key
            default: Default value if not found

        Returns:
            Preference value
        """
        return self.preferences.get(key, default)

    def set_preference(self, key: str, value: Any) -> None:
        """
        Set a user preference.

        Args:
            key: Preference key
            value: Preference value
        """
        self.preferences[key] = value
        self.touch()

    def touch(self) -> None:
        """Update the updated_at timestamp."""
        from datetime import datetime
        self.updated_at = datetime.now()

    @property
    def display_name(self) -> str:
        """Get display name (username or name)."""
        return self.username or self.name

    @property
    def initials(self) -> str:
        """Get user initials."""
        parts = self.name.split()
        if len(parts) >= 2:
            return f"{parts[0][0]}{parts[-1][0]}".upper()
        elif parts:
            return parts[0][0].upper()
        return "?"

    def deactivate(self) -> None:
        """Deactivate the user."""
        self.is_active = False
        self.touch()

    def activate(self) -> None:
        """Activate the user."""
        self.is_active = True
        self.touch()
