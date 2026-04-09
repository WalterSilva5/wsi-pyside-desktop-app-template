"""Base dialog component."""
from __future__ import annotations
from PySide6.QtWidgets import QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt


class BaseDialog(QDialog):
    """Base class for all dialogs."""

    def __init__(self, title: str = "", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setMinimumWidth(400)
        self._setup_ui()

    def _setup_ui(self) -> None:
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(24, 24, 24, 24)
        self._layout.setSpacing(16)
        self._content_layout = QVBoxLayout()
        self._layout.addLayout(self._content_layout)
        self._button_layout = QHBoxLayout()
        self._button_layout.addStretch()
        self._layout.addLayout(self._button_layout)

    def add_content(self, widget: QWidget) -> None:
        self._content_layout.addWidget(widget)

    def add_button(self, text: str, callback=None, primary: bool = False) -> QPushButton:
        btn = QPushButton(text)
        btn.setCursor(Qt.PointingHandCursor)
        if primary:
            btn.setStyleSheet("QPushButton { background: #0078D4; color: white; border: none; border-radius: 6px; padding: 10px 20px; }")
        else:
            btn.setStyleSheet("QPushButton { background: white; border: 1px solid #e0e0e0; border-radius: 6px; padding: 10px 20px; }")
        if callback:
            btn.clicked.connect(callback)
        self._button_layout.addWidget(btn)
        return btn
