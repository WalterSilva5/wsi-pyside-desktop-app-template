"""Secondary button component."""
from __future__ import annotations
from PySide6.QtWidgets import QPushButton, QWidget, QHBoxLayout
from PySide6.QtCore import Qt
from src.views.components.base import BaseComponent
from src.core.types import ButtonSize


class SecondaryButton(BaseComponent):
    """Secondary button for less prominent actions."""

    def __init__(self, text: str = "", parent: QWidget | None = None, **kwargs) -> None:
        super().__init__(parent, text=text, size=ButtonSize.MEDIUM, **kwargs)

    def _setup_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self._button = QPushButton(self.get_prop("text", ""))
        self._button.setCursor(Qt.PointingHandCursor)
        self._apply_styles()
        layout.addWidget(self._button)

    def _setup_connections(self) -> None:
        self._button.clicked.connect(self.clicked.emit)

    def _apply_styles(self) -> None:
        self._button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #333;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: 500;
            }
            QPushButton:hover { background-color: #f5f5f5; border-color: #d0d0d0; }
            QPushButton:pressed { background-color: #e8e8e8; }
        """)

    def _update_ui(self) -> None:
        self._button.setText(self.get_prop("text", ""))
