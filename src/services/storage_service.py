"""
Storage Service.

Provides local storage functionality for persisting data.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from PySide6.QtCore import Signal

from src.services.base import BaseService


class StorageService(BaseService):
    """
    Local Storage Service.

    Provides key-value storage with JSON persistence.
    Useful for caching, user preferences, and temporary data.

    Usage:
        storage = StorageService()

        # Store data
        storage.set("user_preferences", {"theme": "dark"})

        # Retrieve data
        prefs = storage.get("user_preferences", {})

        # Remove data
        storage.remove("user_preferences")
    """

    # Signals
    data_changed = Signal(str, object)  # key, value
    data_removed = Signal(str)  # key

    def _on_init(self) -> None:
        """Initialize the storage service."""
        self._storage_dir = self._get_storage_directory()
        self._storage_dir.mkdir(parents=True, exist_ok=True)
        self._cache: dict[str, Any] = {}
        self._load_cache()

    def _get_storage_directory(self) -> Path:
        """Get the storage directory path."""
        if sys.platform == "win32":
            base = Path.home() / "AppData" / "Local"
        elif sys.platform == "darwin":
            base = Path.home() / "Library" / "Application Support"
        else:
            base = Path.home() / ".local" / "share"

        return base / "PySide6AppTemplate" / "storage"

    def _get_storage_file(self, namespace: str = "default") -> Path:
        """Get storage file path for a namespace."""
        return self._storage_dir / f"{namespace}.json"

    def _load_cache(self, namespace: str = "default") -> None:
        """Load data from storage file into cache."""
        storage_file = self._get_storage_file(namespace)
        if storage_file.exists():
            try:
                with open(storage_file, "r", encoding="utf-8") as f:
                    self._cache = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._cache = {}
        else:
            self._cache = {}

    def _save_cache(self, namespace: str = "default") -> None:
        """Save cache to storage file."""
        storage_file = self._get_storage_file(namespace)
        try:
            with open(storage_file, "w", encoding="utf-8") as f:
                json.dump(self._cache, f, indent=2, ensure_ascii=False)
        except IOError:
            pass

    def get(self, key: str, default: Any = None, namespace: str = "default") -> Any:
        """
        Get a value from storage.

        Args:
            key: Storage key
            default: Default value if not found
            namespace: Storage namespace

        Returns:
            Stored value or default
        """
        if namespace != "default":
            self._load_cache(namespace)
        return self._cache.get(key, default)

    def set(self, key: str, value: Any, namespace: str = "default") -> None:
        """
        Set a value in storage.

        Args:
            key: Storage key
            value: Value to store (must be JSON serializable)
            namespace: Storage namespace
        """
        if namespace != "default":
            self._load_cache(namespace)

        self._cache[key] = value
        self._save_cache(namespace)
        self.data_changed.emit(key, value)

    def remove(self, key: str, namespace: str = "default") -> bool:
        """
        Remove a value from storage.

        Args:
            key: Storage key
            namespace: Storage namespace

        Returns:
            True if removed, False if not found
        """
        if namespace != "default":
            self._load_cache(namespace)

        if key in self._cache:
            del self._cache[key]
            self._save_cache(namespace)
            self.data_removed.emit(key)
            return True
        return False

    def has(self, key: str, namespace: str = "default") -> bool:
        """
        Check if a key exists in storage.

        Args:
            key: Storage key
            namespace: Storage namespace

        Returns:
            True if exists, False otherwise
        """
        if namespace != "default":
            self._load_cache(namespace)
        return key in self._cache

    def clear(self, namespace: str = "default") -> None:
        """
        Clear all data in a namespace.

        Args:
            namespace: Storage namespace to clear
        """
        self._cache = {}
        self._save_cache(namespace)

    def get_all(self, namespace: str = "default") -> dict[str, Any]:
        """
        Get all data in a namespace.

        Args:
            namespace: Storage namespace

        Returns:
            Copy of all stored data
        """
        if namespace != "default":
            self._load_cache(namespace)
        return self._cache.copy()

    def get_keys(self, namespace: str = "default") -> list[str]:
        """
        Get all keys in a namespace.

        Args:
            namespace: Storage namespace

        Returns:
            List of keys
        """
        if namespace != "default":
            self._load_cache(namespace)
        return list(self._cache.keys())

    def get_namespaces(self) -> list[str]:
        """
        Get all available namespaces.

        Returns:
            List of namespace names
        """
        namespaces = []
        for file in self._storage_dir.glob("*.json"):
            namespaces.append(file.stem)
        return namespaces

    def delete_namespace(self, namespace: str) -> bool:
        """
        Delete an entire namespace.

        Args:
            namespace: Namespace to delete

        Returns:
            True if deleted, False otherwise
        """
        storage_file = self._get_storage_file(namespace)
        if storage_file.exists():
            storage_file.unlink()
            if namespace == "default":
                self._cache = {}
            return True
        return False

    @property
    def storage_directory(self) -> Path:
        """Get the storage directory path."""
        return self._storage_dir
