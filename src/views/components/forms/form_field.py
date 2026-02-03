"""Form field wrapper component."""
from __future__ import annotations
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from src.views.components.base import BaseComponent


class FormField(BaseComponent):
    """Wrapper for form fields with label and error display."""

    def __init__(self, label: str = "", parent: QWidget | None = None, **kwargs) -> None:
        super().__init__(parent, label=label, error="", required=False, **kwargs)

    def _setup_ui(self) -> None:
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(4)
        label_text = self.get_prop("label", "")
        if self.get_prop("required"):
            label_text += " *"
        self._label = QLabel(label_text)
        self._label.setStyleSheet("font-weight: 500;")
        self._label.setVisible(bool(self.get_prop("label")))
        self._layout.addWidget(self._label)
        self._content_layout = QVBoxLayout()
        self._content_layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addLayout(self._content_layout)
        self._error_label = QLabel(self.get_prop("error", ""))
        self._error_label.setStyleSheet("color: #dc3545; font-size: 12px;")
        self._error_label.setVisible(bool(self.get_prop("error")))
        self._layout.addWidget(self._error_label)

    def set_content(self, widget: QWidget) -> None:
        """Set the form field content widget."""
        while self._content_layout.count():
            item = self._content_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
        self._content_layout.addWidget(widget)

    def set_error(self, error: str) -> None:
        self.set_prop("error", error)
        self._error_label.setText(error)
        self._error_label.setVisible(bool(error))
