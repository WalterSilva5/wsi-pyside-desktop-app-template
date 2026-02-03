"""Helper utilities."""
from __future__ import annotations
import sys
from pathlib import Path


def get_app_data_dir(app_name: str = "PySide6AppTemplate") -> Path:
    """Get the application data directory."""
    if sys.platform == "win32":
        base = Path.home() / "AppData" / "Local"
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path.home() / ".local" / "share"
    return base / app_name


def ensure_dir_exists(path: Path) -> Path:
    """Ensure a directory exists, create if not."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_resource_path(relative_path: str) -> Path:
    """Get absolute path to resource."""
    base_path = Path(__file__).parent.parent.parent
    return base_path / "resources" / relative_path


def format_file_size(size_bytes: int) -> str:
    """Format file size to human readable."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to max length."""
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def safe_int(value: str, default: int = 0) -> int:
    """Safely convert to int."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def safe_float(value: str, default: float = 0.0) -> float:
    """Safely convert to float."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default
