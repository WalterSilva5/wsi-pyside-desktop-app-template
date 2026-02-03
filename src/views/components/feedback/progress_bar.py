"""Progress bar component."""
from __future__ import annotations
from PySide6.QtWidgets import QWidget, QVBoxLayout, QProgressBar as QPB
from src.views.components.base import BaseComponent


class ProgressBar(BaseComponent):
    """Progress indicator."""

    def __init__(self, parent: QWidget | None = None, **kwargs) -> None:
        super().__init__(parent, value=0, show_text=True, **kwargs)

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self._progress = QPB()
        self._progress.setValue(self.get_prop("value", 0))
        self._progress.setTextVisible(self.get_prop("show_text", True))
        self._progress.setStyleSheet("""
            QProgressBar { border: none; border-radius: 8px; background: #e9ecef; text-align: center; min-height: 20px; }
            QProgressBar::chunk { background: #0078D4; border-radius: 8px; }
        """)
        layout.addWidget(self._progress)

    def set_value(self, value: int) -> None:
        self.set_prop("value", value)
        self._progress.setValue(value)
        self.value_changed.emit(value)

    def get_value(self) -> int:
        return self._progress.value()
