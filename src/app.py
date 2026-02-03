"""
Application entry point.

This module provides the main entry point for the application.
"""

from __future__ import annotations

import sys

from src.core.application import Application, main as app_main


def main() -> int:
    """
    Application entry point.

    Returns:
        Application exit code
    """
    return app_main()


if __name__ == "__main__":
    sys.exit(main())
