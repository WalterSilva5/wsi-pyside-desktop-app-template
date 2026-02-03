"""Toggle button component."""
from __future__ import annotations
from PySide6.QtWidgets import QPushButton, QWidget, QHBoxLayout
from PySide6.QtCore import Qt, Signal
from src.views.components.base import BaseComponent


class ToggleButton(BaseComponent):
    """Toggle button with on/off states."""

    toggled = Signal(bool)

    def __init__(self, text: str = "", parent: QWidget | None = None, **kwargs) -> None:
        super().__init__(parent, text=text, checked=False, **kwargs)

    def _setup_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self._button = QPushButton(self.get_prop("text", ""))
        self._button.setCheckable(True)
        self._button.setChecked(self.get_prop("checked", False))
        self._button.setCursor(Qt.PointingHandCursor)
        self._apply_styles()
        layout.addWidget(self._button)

    def _setup_connections(self) -> None:
        self._button.toggled.connect(self._on_toggled)

    def _on_toggled(self, checked: bool) -> None:
        self.set_prop("checked", checked)
        self.toggled.emit(checked)

    def _apply_styles(self) -> None:
        self._button.setStyleSheet("""
            QPushButton {
                background: #e9ecef;
                color: #333;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
            }
            QPushButton:hover { background: #dee2e6; }
            QPushButton:checked { background: #0078D4; color: white; }
            QPushButton:checked:hover { background: #106EBE; }
        """)

    def is_checked(self) -> bool:
        return self._button.isChecked()

    def set_checked(self, checked: bool) -> None:
        self._button.setChecked(checked)
