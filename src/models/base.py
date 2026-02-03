"""
Base model class.

Provides common functionality for all data models.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, TypeVar
from uuid import uuid4

T = TypeVar("T", bound="BaseModel")


@dataclass
class BaseModel:
    """
    Base class for all data models.

    Provides common functionality:
    - Unique ID generation
    - Timestamps
    - Serialization/deserialization
    - Validation hooks

    Usage:
        @dataclass
        class User(BaseModel):
            name: str
            email: str
    """

    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """Called after dataclass initialization."""
        self.validate()

    def validate(self) -> None:
        """
        Validate the model.

        Override in subclasses to add validation logic.
        Raise ValidationError if validation fails.
        """
        pass

    def to_dict(self) -> dict[str, Any]:
        """
        Convert model to dictionary.

        Returns:
            Dictionary representation of the model
        """
        data = asdict(self)
        # Convert datetime to ISO format
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
        return data

    @classmethod
    def from_dict(cls: type[T], data: dict[str, Any]) -> T:
        """
        Create model from dictionary.

        Args:
            data: Dictionary with model data

        Returns:
            New model instance
        """
        # Convert ISO strings back to datetime
        for key in ["created_at", "updated_at"]:
            if key in data and isinstance(data[key], str):
                data[key] = datetime.fromisoformat(data[key])
        return cls(**data)

    def update(self, **kwargs: Any) -> None:
        """
        Update model fields.

        Args:
            **kwargs: Fields to update
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()
        self.validate()

    def copy(self: T, **changes: Any) -> T:
        """
        Create a copy with optional changes.

        Args:
            **changes: Fields to change in the copy

        Returns:
            New model instance
        """
        data = self.to_dict()
        data.update(changes)
        # Generate new ID for copy
        data["id"] = str(uuid4())
        data["created_at"] = datetime.now()
        data["updated_at"] = datetime.now()
        return self.__class__.from_dict(data)

    def __eq__(self, other: object) -> bool:
        """Check equality based on ID."""
        if isinstance(other, BaseModel):
            return self.id == other.id
        return False

    def __hash__(self) -> int:
        """Hash based on ID."""
        return hash(self.id)
