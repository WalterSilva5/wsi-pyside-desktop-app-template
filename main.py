#!/usr/bin/env python3
"""
PySide6 Desktop Application Template

A scalable, well-structured template for building desktop applications
with PySide6, implementing design patterns and best practices.

Usage:
    python main.py

Or using the module:
    python -m src.app
"""

from __future__ import annotations

import sys


def main() -> int:
    """
    Application entry point.

    Returns:
        Application exit code
    """
    from src.core.application import Application

    app = Application()
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
