"""Utility decorators."""
from __future__ import annotations
import functools
import time
from typing import Any, Callable, TypeVar

T = TypeVar("T")


def singleton(cls: type[T]) -> type[T]:
    """Singleton decorator."""
    instances: dict[type, Any] = {}

    @functools.wraps(cls)
    def get_instance(*args: Any, **kwargs: Any) -> T:
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance  # type: ignore


def debounce(wait_ms: int) -> Callable:
    """Debounce decorator - delays function execution."""
    def decorator(func: Callable) -> Callable:
        last_call = [0.0]

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            now = time.time() * 1000
            if now - last_call[0] >= wait_ms:
                last_call[0] = now
                return func(*args, **kwargs)
            return None

        return wrapper
    return decorator


def throttle(limit_ms: int) -> Callable:
    """Throttle decorator - limits function calls."""
    def decorator(func: Callable) -> Callable:
        last_call = [0.0]

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            now = time.time() * 1000
            if now - last_call[0] >= limit_ms:
                last_call[0] = now
                return func(*args, **kwargs)
            return None

        return wrapper
    return decorator


def log_call(func: Callable) -> Callable:
    """Log function calls decorator."""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        from src.core.container import container
        from src.services.logger_service import LoggerService
        try:
            logger = container.resolve(LoggerService)
            logger.debug(f"Calling {func.__name__}")
        except Exception:
            pass
        return func(*args, **kwargs)
    return wrapper
