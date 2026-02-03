"""
Application services module.

Contains singleton services for:
- Configuration management
- Navigation/Routing
- Theme management
- Logging
- Local storage
"""

from src.services.base import BaseService
from src.services.config_service import ConfigService
from src.services.navigation_service import NavigationService
from src.services.theme_service import ThemeService
from src.services.logger_service import LoggerService
from src.services.storage_service import StorageService

__all__ = [
    "BaseService",
    "ConfigService",
    "NavigationService",
    "ThemeService",
    "LoggerService",
    "StorageService",
]
