"""Form dialog component."""
from __future__ import annotations
from typing import Any
from PySide6.QtWidgets import QWidget
from src.views.components.dialogs.base_dialog import BaseDialog


class FormDialog(BaseDialog):
    """Dialog with form fields."""

    def __init__(self, title: str = "Form", parent: QWidget | None = None) -> None:
        super().__init__(title, parent)
        self._form_data: dict[str, Any] = {}
        self._fields: dict[str, QWidget] = {}
        self._build_buttons()

    def _build_buttons(self) -> None:
        self.add_button("Cancel", self.reject)
        self.add_button("Submit", self._on_submit, primary=True)

    def add_field(self, name: str, widget: QWidget) -> None:
        self._fields[name] = widget
        self.add_content(widget)

    def _on_submit(self) -> None:
        for name, widget in self._fields.items():
            if hasattr(widget, "get_value"):
                self._form_data[name] = widget.get_value()
            elif hasattr(widget, "text"):
                self._form_data[name] = widget.text()
        self.accept()

    def get_data(self) -> dict[str, Any]:
        return self._form_data
