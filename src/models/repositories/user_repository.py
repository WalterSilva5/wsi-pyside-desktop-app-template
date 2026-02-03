"""
User repository implementation.

Provides data access for User entities.
"""

from __future__ import annotations

import sys
from pathlib import Path

from src.models.user import User
from src.models.repositories.base import JsonFileRepository


class UserRepository(JsonFileRepository[User]):
    """
    Repository for User entities.

    Provides CRUD operations and specialized queries for users.

    Usage:
        repo = UserRepository()
        user = repo.add(User(name="John", email="john@test.com"))
        user = repo.find_by_email("john@test.com")
    """

    def __init__(self, file_path: Path | None = None) -> None:
        """
        Initialize the user repository.

        Args:
            file_path: Optional custom path. Uses default if not provided.
        """
        if file_path is None:
            file_path = self._get_default_path()
        super().__init__(file_path, User)

    def _get_default_path(self) -> Path:
        """Get the default storage path."""
        if sys.platform == "win32":
            base = Path.home() / "AppData" / "Local"
        elif sys.platform == "darwin":
            base = Path.home() / "Library" / "Application Support"
        else:
            base = Path.home() / ".local" / "share"

        return base / "PySide6AppTemplate" / "data" / "users.json"

    def find_by_email(self, email: str) -> User | None:
        """
        Find user by email address.

        Args:
            email: Email to search for

        Returns:
            User if found, None otherwise
        """
        return self.find_one(email=email)

    def find_by_username(self, username: str) -> User | None:
        """
        Find user by username.

        Args:
            username: Username to search for

        Returns:
            User if found, None otherwise
        """
        return self.find_one(username=username)

    def get_active_users(self) -> list[User]:
        """
        Get all active users.

        Returns:
            List of active users
        """
        return self.find(is_active=True)

    def get_inactive_users(self) -> list[User]:
        """
        Get all inactive users.

        Returns:
            List of inactive users
        """
        return self.find(is_active=False)

    def search(self, query: str) -> list[User]:
        """
        Search users by name or email.

        Args:
            query: Search query string

        Returns:
            List of matching users
        """
        query_lower = query.lower()
        return [
            user for user in self.get_all()
            if query_lower in user.name.lower()
            or query_lower in user.email.lower()
            or query_lower in user.username.lower()
        ]

    def email_exists(self, email: str, exclude_id: str | None = None) -> bool:
        """
        Check if email is already in use.

        Args:
            email: Email to check
            exclude_id: Optional user ID to exclude from check

        Returns:
            True if email exists, False otherwise
        """
        user = self.find_by_email(email)
        if user is None:
            return False
        if exclude_id and user.id == exclude_id:
            return False
        return True

    def username_exists(self, username: str, exclude_id: str | None = None) -> bool:
        """
        Check if username is already in use.

        Args:
            username: Username to check
            exclude_id: Optional user ID to exclude from check

        Returns:
            True if username exists, False otherwise
        """
        user = self.find_by_username(username)
        if user is None:
            return False
        if exclude_id and user.id == exclude_id:
            return False
        return True
