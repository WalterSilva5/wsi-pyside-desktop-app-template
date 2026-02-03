"""Select input component."""
from __future__ import annotations
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox
from PySide6.QtCore import Signal
from src.views.components.base import BaseComponent


class SelectInput(BaseComponent):
    """Dropdown select input."""

    selection_changed = Signal(str)

    def __init__(self, label: str = "", parent: QWidget | None = None, **kwargs) -> None:
        super().__init__(parent, label=label, options=[], value="", **kwargs)

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        self._label = QLabel(self.get_prop("label", ""))
        self._label.setStyleSheet("font-weight: 500;")
        self._label.setVisible(bool(self.get_prop("label")))
        layout.addWidget(self._label)
        self._combo = QComboBox()
        self._combo.setStyleSheet("""
            QComboBox { border: 1px solid #e0e0e0; border-radius: 6px; padding: 10px 12px; }
            QComboBox:focus { border-color: #0078D4; }
        """)
        for option in self.get_prop("options", []):
            self._combo.addItem(option.get("label", ""), option.get("value", ""))
        layout.addWidget(self._combo)

    def _setup_connections(self) -> None:
        self._combo.currentIndexChanged.connect(self._on_selection_changed)

    def _on_selection_changed(self, index: int) -> None:
        value = self._combo.currentData()
        self.set_prop("value", value)
        self.selection_changed.emit(value)
        self.value_changed.emit(value)

    def get_value(self) -> str:
        return self._combo.currentData()

    def set_options(self, options: list) -> None:
        self._combo.clear()
        for option in options:
            self._combo.addItem(option.get("label", ""), option.get("value", ""))
