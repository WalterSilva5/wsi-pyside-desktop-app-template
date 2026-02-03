"""Radio group component."""
from __future__ import annotations
from PySide6.QtWidgets import QWidget, QVBoxLayout, QRadioButton, QButtonGroup
from PySide6.QtCore import Signal
from src.views.components.base import BaseComponent


class RadioGroup(BaseComponent):
    """Group of radio buttons."""

    selection_changed = Signal(str)

    def __init__(self, parent: QWidget | None = None, **kwargs) -> None:
        super().__init__(parent, options=[], value="", **kwargs)

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        self._button_group = QButtonGroup(self)
        self._buttons: dict[str, QRadioButton] = {}
        for option in self.get_prop("options", []):
            radio = QRadioButton(option.get("label", ""))
            value = option.get("value", "")
            self._buttons[value] = radio
            self._button_group.addButton(radio)
            if value == self.get_prop("value"):
                radio.setChecked(True)
            layout.addWidget(radio)

    def _setup_connections(self) -> None:
        self._button_group.buttonClicked.connect(self._on_button_clicked)

    def _on_button_clicked(self, button: QRadioButton) -> None:
        for value, btn in self._buttons.items():
            if btn == button:
                self.set_prop("value", value)
                self.selection_changed.emit(value)
                self.value_changed.emit(value)
                break

    def get_value(self) -> str:
        for value, btn in self._buttons.items():
            if btn.isChecked():
                return value
        return ""

    def set_options(self, options: list) -> None:
        # Clear existing
        for btn in self._buttons.values():
            self._button_group.removeButton(btn)
            btn.deleteLater()
        self._buttons.clear()
        self.set_prop("options", options)
        # Rebuild
        layout = self.layout()
        for option in options:
            radio = QRadioButton(option.get("label", ""))
            value = option.get("value", "")
            self._buttons[value] = radio
            self._button_group.addButton(radio)
            layout.addWidget(radio)
