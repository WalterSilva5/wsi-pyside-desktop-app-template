"""Badge component."""
from __future__ import annotations
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from src.views.components.base import BaseComponent


class Badge(BaseComponent):
    """Badge for status indicators."""

    def __init__(self, text: str = "", parent: QWidget | None = None, **kwargs) -> None:
        super().__init__(parent, text=text, variant="primary", **kwargs)

    def _setup_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self._label = QLabel(self.get_prop("text", ""))
        self._apply_styles()
        layout.addWidget(self._label)

    def _apply_styles(self) -> None:
        colors = {
            "primary": ("#0078D4", "white"),
            "success": ("#28A745", "white"),
            "warning": ("#FFC107", "black"),
            "danger": ("#DC3545", "white"),
            "info": ("#17A2B8", "white"),
        }
        variant = self.get_prop("variant", "primary")
        bg, fg = colors.get(variant, colors["primary"])
        self._label.setStyleSheet(f"""
            QLabel {{ background: {bg}; color: {fg}; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: bold; }}
        """)

    def set_text(self, text: str) -> None:
        self.set_prop("text", text)
        self._label.setText(text)

    def set_variant(self, variant: str) -> None:
        self.set_prop("variant", variant)
        self._apply_styles()
