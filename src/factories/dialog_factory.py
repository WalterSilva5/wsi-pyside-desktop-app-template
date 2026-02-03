"""Dialog Factory."""
from __future__ import annotations
from typing import Type, Any
from PySide6.QtWidgets import QDialog, QWidget


class DialogFactory:
    """Factory for creating dialogs."""

    _dialogs: dict[str, Type[QDialog]] = {}

    @classmethod
    def register(cls, name: str, dialog_class: Type[QDialog]) -> None:
        """Register a dialog class."""
        cls._dialogs[name] = dialog_class

    @classmethod
    def create(cls, name: str, parent: QWidget | None = None, **kwargs: Any) -> QDialog:
        """Create a dialog by name."""
        if name not in cls._dialogs:
            raise ValueError(f"Dialog '{name}' not registered")
        return cls._dialogs[name](parent=parent, **kwargs)

    @classmethod
    def get_registered(cls) -> list[str]:
        """Get list of registered dialogs."""
        return list(cls._dialogs.keys())


def register_default_dialogs() -> None:
    """Register all default dialogs."""
    from src.views.components.dialogs.confirm_dialog import ConfirmDialog
    from src.views.components.dialogs.alert_dialog import AlertDialog
    from src.views.components.dialogs.form_dialog import FormDialog

    DialogFactory.register("confirm", ConfirmDialog)
    DialogFactory.register("alert", AlertDialog)
    DialogFactory.register("form", FormDialog)
