"""Confirm dialog component."""
from __future__ import annotations
from PySide6.QtWidgets import QWidget, QLabel
from src.views.components.dialogs.base_dialog import BaseDialog


class ConfirmDialog(BaseDialog):
    """Confirmation dialog for important actions."""

    def __init__(self, title: str = "Confirm", message: str = "", parent: QWidget | None = None, **kwargs) -> None:
        super().__init__(title, parent)
        self._message = message
        self._confirm_text = kwargs.get("confirm_text", "Confirm")
        self._cancel_text = kwargs.get("cancel_text", "Cancel")
        self._build_ui()

    def _build_ui(self) -> None:
        msg_label = QLabel(self._message)
        msg_label.setWordWrap(True)
        self.add_content(msg_label)
        self.add_button(self._cancel_text, self.reject)
        self.add_button(self._confirm_text, self.accept, primary=True)

    @classmethod
    def confirm(cls, title: str, message: str, parent: QWidget | None = None) -> bool:
        dialog = cls(title, message, parent)
        return dialog.exec() == cls.Accepted
