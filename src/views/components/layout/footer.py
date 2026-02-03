"""
Footer component.

Application footer with status and information.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
)
from PySide6.QtCore import Qt

from src.views.components.base import BaseComponent


class Footer(BaseComponent):
    """
    Application footer component.

    Features:
    - Status text
    - Version info
    - Copyright notice

    Props:
        text: Footer text
        show_version: Show version info
    """

    def __init__(
        self,
        text: str = "",
        parent: QWidget | None = None,
        **kwargs
    ) -> None:
        """Initialize the footer."""
        super().__init__(parent, text=text, **kwargs)

    def _setup_ui(self) -> None:
        """Setup the footer UI."""
        self.setFixedHeight(32)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)

        # Status text
        self._status_label = QLabel(self.get_prop("text", "Ready"))
        self._status_label.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(self._status_label)

        # Stretch
        layout.addStretch()

        # Version
        if self.get_prop("show_version", True):
            version_label = QLabel("v1.0.0")
            version_label.setStyleSheet("color: #888; font-size: 11px;")
            layout.addWidget(version_label)

    def set_status(self, text: str) -> None:
        """Set the status text."""
        self.set_prop("text", text)
        self._status_label.setText(text)
