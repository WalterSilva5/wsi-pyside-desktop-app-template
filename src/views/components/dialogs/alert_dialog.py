"""Alert dialog component."""
from __future__ import annotations
from PySide6.QtWidgets import QWidget, QLabel, QFrame, QVBoxLayout
from src.views.components.dialogs.base_dialog import BaseDialog


class AlertDialog(BaseDialog):
    """Alert dialog for notifications."""

    def __init__(self, title: str = "Alert", message: str = "", alert_type: str = "info", parent: QWidget | None = None) -> None:
        super().__init__(title, parent)
        self._message = message
        self._alert_type = alert_type
        self._build_ui()

    def _build_ui(self) -> None:
        colors = {"info": "#cfe2ff", "success": "#d1e7dd", "warning": "#fff3cd", "error": "#f8d7da"}
        bg_color = colors.get(self._alert_type, colors["info"])
        alert_frame = QFrame()
        alert_frame.setStyleSheet(f"QFrame {{ background: {bg_color}; border-radius: 6px; padding: 16px; }}")
        layout = QVBoxLayout(alert_frame)
        msg_label = QLabel(self._message)
        msg_label.setWordWrap(True)
        layout.addWidget(msg_label)
        self.add_content(alert_frame)
        self.add_button("OK", self.accept, primary=True)

    @classmethod
    def show_info(cls, title: str, message: str, parent: QWidget | None = None) -> None:
        cls(title, message, "info", parent).exec()

    @classmethod
    def show_success(cls, title: str, message: str, parent: QWidget | None = None) -> None:
        cls(title, message, "success", parent).exec()

    @classmethod
    def show_warning(cls, title: str, message: str, parent: QWidget | None = None) -> None:
        cls(title, message, "warning", parent).exec()

    @classmethod
    def show_error(cls, title: str, message: str, parent: QWidget | None = None) -> None:
        cls(title, message, "error", parent).exec()
