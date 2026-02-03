"""
Centralized Logging Service.

Provides file and console logging with rotation support.
"""

from __future__ import annotations

import logging
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

from src.services.base import BaseService


class LoggerService(BaseService):
    """
    Centralized logging service.

    Features:
    - Console and file logging
    - Log rotation (5 files, 5MB each)
    - Configurable log levels
    - Structured log format

    Usage:
        logger = LoggerService()
        logger.info("Application started")
        logger.error("An error occurred", exc_info=True)
    """

    def _on_init(self) -> None:
        """Initialize the logger."""
        self._log_dir = self._get_log_directory()
        self._log_dir.mkdir(parents=True, exist_ok=True)
        self._logger = self._setup_logger()

    def _get_log_directory(self) -> Path:
        """Get the log directory path."""
        # Use platform-appropriate app data directory
        if sys.platform == "win32":
            base = Path.home() / "AppData" / "Local"
        elif sys.platform == "darwin":
            base = Path.home() / "Library" / "Application Support"
        else:
            base = Path.home() / ".local" / "share"

        return base / "PySide6AppTemplate" / "logs"

    def _setup_logger(self) -> logging.Logger:
        """Configure and return the logger."""
        logger = logging.getLogger("PySide6AppTemplate")
        logger.setLevel(logging.DEBUG)

        # Remove existing handlers
        logger.handlers.clear()

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%H:%M:%S"
        )
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)

        # File handler with rotation
        log_file = self._log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=5 * 1024 * 1024,  # 5MB
            backupCount=5,
            encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

        return logger

    def debug(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log a debug message."""
        self._logger.debug(message, *args, **kwargs)

    def info(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log an info message."""
        self._logger.info(message, *args, **kwargs)

    def warning(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log a warning message."""
        self._logger.warning(message, *args, **kwargs)

    def error(self, message: str, *args: Any, exc_info: bool = False, **kwargs: Any) -> None:
        """Log an error message."""
        self._logger.error(message, *args, exc_info=exc_info, **kwargs)

    def critical(self, message: str, *args: Any, exc_info: bool = False, **kwargs: Any) -> None:
        """Log a critical message."""
        self._logger.critical(message, *args, exc_info=exc_info, **kwargs)

    def exception(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log an exception with traceback."""
        self._logger.exception(message, *args, **kwargs)

    def set_level(self, level: int | str) -> None:
        """
        Set the logging level.

        Args:
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        if isinstance(level, str):
            level = getattr(logging, level.upper(), logging.INFO)
        self._logger.setLevel(level)

    @property
    def log_directory(self) -> Path:
        """Get the log directory path."""
        return self._log_dir
