"""Primary button component."""
from __future__ import annotations
from PySide6.QtWidgets import QPushButton, QWidget
from PySide6.QtCore import Qt
from src.views.components.base import BaseComponent
from src.core.types import ButtonSize


class PrimaryButton(BaseComponent):
    """Primary action button for main actions."""

    def __init__(self, text: str = "", parent: QWidget | None = None, **kwargs) -> None:
        super().__init__(parent, text=text, size=ButtonSize.MEDIUM, disabled=False, **kwargs)

    def _setup_ui(self) -> None:
        from PySide6.QtWidgets import QHBoxLayout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self._button = QPushButton(self.get_prop("text", ""))
        self._button.setCursor(Qt.PointingHandCursor)
        self._apply_styles()
        layout.addWidget(self._button)

    def _setup_connections(self) -> None:
        self._button.clicked.connect(self.clicked.emit)

    def _apply_styles(self) -> None:
        size = self.get_prop("size", ButtonSize.MEDIUM)
        sizes = {
            ButtonSize.SMALL: "padding: 6px 12px; font-size: 12px;",
            ButtonSize.MEDIUM: "padding: 10px 20px; font-size: 14px;",
            ButtonSize.LARGE: "padding: 14px 28px; font-size: 16px;",
        }
        self._button.setStyleSheet(f"""
            QPushButton {{
                background-color: #0078D4;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 500;
                {sizes.get(size, sizes[ButtonSize.MEDIUM])}
            }}
            QPushButton:hover {{ background-color: #106EBE; }}
            QPushButton:pressed {{ background-color: #005A9E; }}
            QPushButton:disabled {{ background-color: #ccc; color: #888; }}
        """)
        self._button.setEnabled(not self.get_prop("disabled", False))

    def _update_ui(self) -> None:
        self._button.setText(self.get_prop("text", ""))
        self._apply_styles()

    def set_text(self, text: str) -> None:
        self.set_prop("text", text)
