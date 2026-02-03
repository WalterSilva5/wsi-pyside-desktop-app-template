"""Tests for ConfigService."""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


class TestConfigService:
    """Test cases for ConfigService."""

    def test_get_default_value(self, temp_config_file: Path):
        """Test getting a config value with default."""
        from src.services.config_service import ConfigService

        service = ConfigService(config_path=temp_config_file)

        # Existing value
        assert service.get("theme") == "light"

        # Non-existing with default
        assert service.get("nonexistent", "default") == "default"

    def test_get_nested_value(self, temp_config_file: Path):
        """Test getting nested config values with dot notation."""
        from src.services.config_service import ConfigService

        service = ConfigService(config_path=temp_config_file)

        assert service.get("app.name") == "TestApp"
        assert service.get("app.version") == "1.0.0"
        assert service.get("window.width") == 800

    def test_set_value(self, temp_config_file: Path):
        """Test setting a config value."""
        from src.services.config_service import ConfigService

        service = ConfigService(config_path=temp_config_file)

        service.set("theme", "dark")
        assert service.get("theme") == "dark"

    def test_set_nested_value(self, temp_config_file: Path):
        """Test setting nested config values."""
        from src.services.config_service import ConfigService

        service = ConfigService(config_path=temp_config_file)

        service.set("window.width", 1024)
        assert service.get("window.width") == 1024

        # Set new nested path
        service.set("user.preferences.theme", "dark")
        assert service.get("user.preferences.theme") == "dark"

    def test_save_and_load(self, temp_config_file: Path):
        """Test saving and loading config."""
        from src.services.config_service import ConfigService

        service = ConfigService(config_path=temp_config_file)
        service.set("new_key", "new_value")
        service.save()

        # Create new instance to verify persistence
        service2 = ConfigService(config_path=temp_config_file)
        assert service2.get("new_key") == "new_value"

    def test_load_nonexistent_file(self, tmp_path: Path):
        """Test loading from nonexistent file uses defaults."""
        from src.services.config_service import ConfigService

        config_path = tmp_path / "nonexistent.json"
        service = ConfigService(config_path=config_path)

        # Should have empty config or defaults
        assert service.get("anything", "default") == "default"

    def test_delete_key(self, temp_config_file: Path):
        """Test deleting a config key."""
        from src.services.config_service import ConfigService

        service = ConfigService(config_path=temp_config_file)

        assert service.get("theme") == "light"
        service.delete("theme")
        assert service.get("theme", "default") == "default"

    def test_has_key(self, temp_config_file: Path):
        """Test checking if key exists."""
        from src.services.config_service import ConfigService

        service = ConfigService(config_path=temp_config_file)

        assert service.has("theme") is True
        assert service.has("nonexistent") is False
        assert service.has("app.name") is True

    def test_get_all(self, temp_config_file: Path):
        """Test getting all config as dict."""
        from src.services.config_service import ConfigService

        service = ConfigService(config_path=temp_config_file)

        config = service.get_all()
        assert isinstance(config, dict)
        assert "theme" in config
        assert "app" in config


class TestConfigServiceEdgeCases:
    """Edge case tests for ConfigService."""

    def test_empty_key(self, temp_config_file: Path):
        """Test handling empty key."""
        from src.services.config_service import ConfigService

        service = ConfigService(config_path=temp_config_file)

        assert service.get("", "default") == "default"

    def test_special_characters_in_key(self, temp_config_file: Path):
        """Test keys with special characters."""
        from src.services.config_service import ConfigService

        service = ConfigService(config_path=temp_config_file)

        service.set("special-key_123", "value")
        assert service.get("special-key_123") == "value"

    def test_none_value(self, temp_config_file: Path):
        """Test setting None as value."""
        from src.services.config_service import ConfigService

        service = ConfigService(config_path=temp_config_file)

        service.set("nullable", None)
        assert service.get("nullable") is None
        assert service.has("nullable") is True

    def test_complex_value_types(self, temp_config_file: Path):
        """Test setting complex value types."""
        from src.services.config_service import ConfigService

        service = ConfigService(config_path=temp_config_file)

        # List
        service.set("list_val", [1, 2, 3])
        assert service.get("list_val") == [1, 2, 3]

        # Dict
        service.set("dict_val", {"nested": True})
        assert service.get("dict_val") == {"nested": True}

        # Bool
        service.set("bool_val", False)
        assert service.get("bool_val") is False
