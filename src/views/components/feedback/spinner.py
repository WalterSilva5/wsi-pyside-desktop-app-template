"""Spinner component."""
from __future__ import annotations
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import QTimer, Qt
from src.views.components.base import BaseComponent


class Spinner(BaseComponent):
    """Loading spinner."""

    def __init__(self, parent: QWidget | None = None, **kwargs) -> None:
        super().__init__(parent, size=32, **kwargs)
        self._angle = 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._rotate)

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        size = self.get_prop("size", 32)
        self._label = QLabel("⟳")
        self._label.setFixedSize(size, size)
        self._label.setAlignment(Qt.AlignCenter)
        self._label.setStyleSheet(f"font-size: {size}px; color: #0078D4;")
        layout.addWidget(self._label, alignment=Qt.AlignCenter)

    def _rotate(self) -> None:
        self._angle = (self._angle + 30) % 360
        self._label.setStyleSheet(f"""
            font-size: {self.get_prop('size', 32)}px; color: #0078D4;
            qproperty-text: '⟳';
        """)

    def start(self) -> None:
        self._timer.start(100)

    def stop(self) -> None:
        self._timer.stop()

    def is_spinning(self) -> bool:
        return self._timer.isActive()
