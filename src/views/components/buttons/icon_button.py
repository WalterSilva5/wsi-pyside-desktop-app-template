"""Icon button component."""
from __future__ import annotations
from PySide6.QtWidgets import QPushButton, QWidget, QHBoxLayout
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from src.views.components.base import BaseComponent


class IconButton(BaseComponent):
    """Button with icon only."""

    def __init__(self, icon: QIcon | None = None, parent: QWidget | None = None, **kwargs) -> None:
        super().__init__(parent, icon=icon, size=32, tooltip="", **kwargs)

    def _setup_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        size = self.get_prop("size", 32)
        self._button = QPushButton()
        self._button.setFixedSize(size, size)
        self._button.setCursor(Qt.PointingHandCursor)
        icon = self.get_prop("icon")
        if icon:
            self._button.setIcon(icon)
            self._button.setIconSize(QSize(size - 8, size - 8))
        tooltip = self.get_prop("tooltip", "")
        if tooltip:
            self._button.setToolTip(tooltip)
        self._apply_styles()
        layout.addWidget(self._button)

    def _setup_connections(self) -> None:
        self._button.clicked.connect(self.clicked.emit)

    def _apply_styles(self) -> None:
        size = self.get_prop("size", 32)
        self._button.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: 1px solid #e0e0e0;
                border-radius: {size // 2}px;
            }}
            QPushButton:hover {{ background: #f0f0f0; }}
            QPushButton:pressed {{ background: #e0e0e0; }}
        """)

    def set_icon(self, icon: QIcon) -> None:
        self.set_prop("icon", icon)
        self._button.setIcon(icon)
