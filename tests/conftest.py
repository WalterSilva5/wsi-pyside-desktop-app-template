"""Pytest configuration and fixtures."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING, Generator
from unittest.mock import MagicMock

import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

if TYPE_CHECKING:
    from src.core.container import Container


@pytest.fixture(scope="session")
def qapp():
    """Create QApplication for the test session."""
    from PySide6.QtWidgets import QApplication

    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


@pytest.fixture
def container() -> Generator["Container", None, None]:
    """Create a fresh DI container for each test."""
    from src.core.container import Container

    test_container = Container()
    yield test_container
    test_container.clear()


@pytest.fixture
def mock_logger() -> MagicMock:
    """Create a mock logger service."""
    logger = MagicMock()
    logger.debug = MagicMock()
    logger.info = MagicMock()
    logger.warning = MagicMock()
    logger.error = MagicMock()
    return logger


@pytest.fixture
def temp_config_file(tmp_path: Path) -> Path:
    """Create a temporary config file."""
    import json

    config_file = tmp_path / "config.json"
    config_data = {
        "app": {
            "name": "TestApp",
            "version": "1.0.0"
        },
        "theme": "light",
        "window": {
            "width": 800,
            "height": 600
        }
    }
    config_file.write_text(json.dumps(config_data, indent=2))
    return config_file


@pytest.fixture
def temp_storage_dir(tmp_path: Path) -> Path:
    """Create a temporary storage directory."""
    storage_dir = tmp_path / "storage"
    storage_dir.mkdir(parents=True, exist_ok=True)
    return storage_dir


@pytest.fixture
def sample_user_data() -> dict:
    """Sample user data for testing."""
    return {
        "id": "user-123",
        "username": "testuser",
        "email": "test@example.com",
        "display_name": "Test User",
        "is_active": True
    }


@pytest.fixture
def sample_settings_data() -> dict:
    """Sample settings data for testing."""
    return {
        "theme": "dark",
        "language": "en",
        "window": {
            "width": 1024,
            "height": 768,
            "maximized": False,
            "x": 100,
            "y": 100
        },
        "sidebar": {
            "visible": True,
            "width": 250
        },
        "recent_files": ["/path/to/file1", "/path/to/file2"],
        "notifications_enabled": True
    }


class MockEventBus:
    """Mock EventBus for testing."""

    def __init__(self):
        self.emitted_signals = []

    def emit_navigate(self, page_id):
        self.emitted_signals.append(("navigate", page_id))

    def emit_theme_changed(self, theme):
        self.emitted_signals.append(("theme_changed", theme))

    def emit_error(self, error):
        self.emitted_signals.append(("error", error))


@pytest.fixture
def mock_event_bus() -> MockEventBus:
    """Create a mock event bus."""
    return MockEventBus()
