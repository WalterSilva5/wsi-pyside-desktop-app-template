"""Checkbox component."""
from __future__ import annotations
from PySide6.QtWidgets import QWidget, QHBoxLayout, QCheckBox as QCB
from PySide6.QtCore import Signal, Qt
from src.views.components.base import BaseComponent


class Checkbox(BaseComponent):
    """Checkbox input with label."""

    checked_changed = Signal(bool)

    def __init__(self, label: str = "", parent: QWidget | None = None, **kwargs) -> None:
        super().__init__(parent, label=label, checked=False, **kwargs)

    def _setup_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self._checkbox = QCB(self.get_prop("label", ""))
        self._checkbox.setChecked(self.get_prop("checked", False))
        layout.addWidget(self._checkbox)
        layout.addStretch()

    def _setup_connections(self) -> None:
        self._checkbox.stateChanged.connect(self._on_state_changed)

    def _on_state_changed(self, state: int) -> None:
        checked = state == Qt.Checked
        self.set_prop("checked", checked)
        self.checked_changed.emit(checked)
        self.value_changed.emit(checked)

    def is_checked(self) -> bool:
        return self._checkbox.isChecked()

    def set_checked(self, checked: bool) -> None:
        self._checkbox.setChecked(checked)
