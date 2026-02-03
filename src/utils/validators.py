"""Validation utilities."""
from __future__ import annotations
import re


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_not_empty(value: str) -> bool:
    """Validate that value is not empty."""
    return bool(value and value.strip())


def validate_min_length(value: str, min_length: int) -> bool:
    """Validate minimum length."""
    return len(value) >= min_length


def validate_max_length(value: str, max_length: int) -> bool:
    """Validate maximum length."""
    return len(value) <= max_length


def validate_numeric(value: str) -> bool:
    """Validate that value is numeric."""
    try:
        float(value)
        return True
    except ValueError:
        return False


def validate_integer(value: str) -> bool:
    """Validate that value is an integer."""
    try:
        int(value)
        return True
    except ValueError:
        return False


def validate_range(value: float, min_val: float, max_val: float) -> bool:
    """Validate that value is within range."""
    return min_val <= value <= max_val


def validate_url(url: str) -> bool:
    """Validate URL format."""
    pattern = r"^https?://[^\s/$.?#].[^\s]*$"
    return bool(re.match(pattern, url, re.IGNORECASE))


def validate_phone(phone: str) -> bool:
    """Validate phone number (basic)."""
    pattern = r"^[\d\s\-\+\(\)]{7,20}$"
    return bool(re.match(pattern, phone))
