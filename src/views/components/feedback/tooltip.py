"""Tooltip helper."""
from __future__ import annotations
from PySide6.QtWidgets import QWidget


class Tooltip:
    """Helper class for tooltips."""

    @staticmethod
    def set(widget: QWidget, text: str) -> None:
        """Set tooltip on a widget."""
        widget.setToolTip(text)

    @staticmethod
    def clear(widget: QWidget) -> None:
        """Clear tooltip from a widget."""
        widget.setToolTip("")
