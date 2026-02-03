"""
Base repository implementations.

Provides abstract repository interface and JSON file-based implementation.
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Generic, TypeVar, Type

from src.models.base import BaseModel
from src.core.exceptions import RepositoryError

T = TypeVar("T", bound=BaseModel)


class BaseRepository(ABC, Generic[T]):
    """
    Abstract base repository.

    Defines the interface for data access operations (CRUD).
    Implements the Repository Pattern for data abstraction.

    Type Parameters:
        T: The model type this repository manages
    """

    @abstractmethod
    def get_all(self) -> list[T]:
        """Get all entities."""
        pass

    @abstractmethod
    def get_by_id(self, entity_id: str) -> T | None:
        """Get entity by ID."""
        pass

    @abstractmethod
    def add(self, entity: T) -> T:
        """Add a new entity."""
        pass

    @abstractmethod
    def update(self, entity: T) -> T:
        """Update an existing entity."""
        pass

    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """Delete an entity by ID."""
        pass

    @abstractmethod
    def exists(self, entity_id: str) -> bool:
        """Check if entity exists."""
        pass

    @abstractmethod
    def count(self) -> int:
        """Get total count of entities."""
        pass


class JsonFileRepository(BaseRepository[T]):
    """
    JSON file-based repository implementation.

    Stores entities in a JSON file on disk.
    Suitable for small datasets and local storage.

    Usage:
        repo = JsonFileRepository(Path("users.json"), User)
        user = repo.add(User(name="John", email="john@test.com"))
        all_users = repo.get_all()
    """

    def __init__(self, file_path: Path, model_class: Type[T]) -> None:
        """
        Initialize the repository.

        Args:
            file_path: Path to the JSON file
            model_class: The model class for deserialization
        """
        self._file_path = file_path
        self._model_class = model_class
        self._data: list[dict[str, Any]] = []
        self._ensure_file()
        self._load()

    def _ensure_file(self) -> None:
        """Ensure the storage file and directory exist."""
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self._file_path.exists():
            self._save()

    def _load(self) -> None:
        """Load data from file."""
        try:
            if self._file_path.exists():
                with open(self._file_path, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            else:
                self._data = []
        except (json.JSONDecodeError, IOError) as e:
            raise RepositoryError(
                f"Failed to load data: {e}",
                entity_type=self._model_class.__name__
            )

    def _save(self) -> None:
        """Save data to file."""
        try:
            with open(self._file_path, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            raise RepositoryError(
                f"Failed to save data: {e}",
                entity_type=self._model_class.__name__
            )

    def get_all(self) -> list[T]:
        """Get all entities."""
        return [self._model_class.from_dict(item) for item in self._data]

    def get_by_id(self, entity_id: str) -> T | None:
        """Get entity by ID."""
        for item in self._data:
            if item.get("id") == entity_id:
                return self._model_class.from_dict(item)
        return None

    def add(self, entity: T) -> T:
        """Add a new entity."""
        # Check for duplicate ID
        if self.exists(entity.id):
            raise RepositoryError(
                f"Entity with ID {entity.id} already exists",
                entity_type=self._model_class.__name__,
                entity_id=entity.id
            )

        self._data.append(entity.to_dict())
        self._save()
        return entity

    def update(self, entity: T) -> T:
        """Update an existing entity."""
        for i, item in enumerate(self._data):
            if item.get("id") == entity.id:
                self._data[i] = entity.to_dict()
                self._save()
                return entity

        raise RepositoryError(
            f"Entity with ID {entity.id} not found",
            entity_type=self._model_class.__name__,
            entity_id=entity.id
        )

    def delete(self, entity_id: str) -> bool:
        """Delete an entity by ID."""
        for i, item in enumerate(self._data):
            if item.get("id") == entity_id:
                del self._data[i]
                self._save()
                return True
        return False

    def exists(self, entity_id: str) -> bool:
        """Check if entity exists."""
        return any(item.get("id") == entity_id for item in self._data)

    def count(self) -> int:
        """Get total count of entities."""
        return len(self._data)

    def clear(self) -> None:
        """Delete all entities."""
        self._data = []
        self._save()

    def find(self, **criteria: Any) -> list[T]:
        """
        Find entities matching criteria.

        Args:
            **criteria: Field-value pairs to match

        Returns:
            List of matching entities
        """
        results = []
        for item in self._data:
            match = all(
                item.get(key) == value
                for key, value in criteria.items()
            )
            if match:
                results.append(self._model_class.from_dict(item))
        return results

    def find_one(self, **criteria: Any) -> T | None:
        """
        Find first entity matching criteria.

        Args:
            **criteria: Field-value pairs to match

        Returns:
            First matching entity or None
        """
        results = self.find(**criteria)
        return results[0] if results else None

    @property
    def file_path(self) -> Path:
        """Get the file path."""
        return self._file_path
