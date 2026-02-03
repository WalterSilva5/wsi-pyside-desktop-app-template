"""Info card component."""
from __future__ import annotations
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from src.views.components.base import BaseComponent


class InfoCard(BaseComponent):
    """Card for displaying information with accent color."""

    def __init__(self, title: str = "", value: str = "", parent: QWidget | None = None, **kwargs) -> None:
        super().__init__(parent, title=title, value=value, color="#0078D4", **kwargs)

    def _setup_ui(self) -> None:
        color = self.get_prop("color", "#0078D4")
        self._frame = QFrame(self)
        self._frame.setStyleSheet(f"""
            QFrame {{ background: white; border: 1px solid #e0e0e0; border-left: 4px solid {color}; border-radius: 4px; padding: 16px; }}
        """)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self._frame)
        content_layout = QVBoxLayout(self._frame)
        self._value_label = QLabel(self.get_prop("value", ""))
        self._value_label.setStyleSheet("font-size: 28px; font-weight: bold;")
        content_layout.addWidget(self._value_label)
        self._title_label = QLabel(self.get_prop("title", ""))
        self._title_label.setStyleSheet("font-size: 14px; color: #666;")
        content_layout.addWidget(self._title_label)

    def set_value(self, value: str) -> None:
        self.set_prop("value", value)
        self._value_label.setText(value)
