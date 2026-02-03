"""Text input component."""
from __future__ import annotations
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit
from PySide6.QtCore import Signal
from src.views.components.base import BaseComponent


class TextInput(BaseComponent):
    """Text input field with label and validation."""

    text_changed = Signal(str)

    def __init__(self, label: str = "", parent: QWidget | None = None, **kwargs) -> None:
        super().__init__(parent, label=label, placeholder="", value="", required=False, error="", **kwargs)

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        self._label = QLabel(self.get_prop("label", ""))
        self._label.setStyleSheet("font-weight: 500;")
        self._label.setVisible(bool(self.get_prop("label")))
        layout.addWidget(self._label)
        self._input = QLineEdit()
        self._input.setPlaceholderText(self.get_prop("placeholder", ""))
        self._input.setText(self.get_prop("value", ""))
        self._input.setStyleSheet("""
            QLineEdit { border: 1px solid #e0e0e0; border-radius: 6px; padding: 10px 12px; }
            QLineEdit:focus { border-color: #0078D4; }
        """)
        layout.addWidget(self._input)
        self._error_label = QLabel(self.get_prop("error", ""))
        self._error_label.setStyleSheet("color: #dc3545; font-size: 12px;")
        self._error_label.setVisible(bool(self.get_prop("error")))
        layout.addWidget(self._error_label)

    def _setup_connections(self) -> None:
        self._input.textChanged.connect(self._on_text_changed)

    def _on_text_changed(self, text: str) -> None:
        self.set_prop("value", text)
        self.text_changed.emit(text)
        self.value_changed.emit(text)

    def get_value(self) -> str:
        return self._input.text()

    def set_value(self, value: str) -> None:
        self._input.setText(value)

    def set_error(self, error: str) -> None:
        self.set_prop("error", error)
        self._error_label.setText(error)
        self._error_label.setVisible(bool(error))
        border_color = "#dc3545" if error else "#e0e0e0"
        self._input.setStyleSheet(f"QLineEdit {{ border: 1px solid {border_color}; border-radius: 6px; padding: 10px 12px; }}")
