"""Basic card component."""
from __future__ import annotations
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from src.views.components.base import BaseComponent


class BasicCard(BaseComponent):
    """Basic card container for content grouping."""

    def __init__(self, title: str = "", parent: QWidget | None = None, **kwargs) -> None:
        super().__init__(parent, title=title, subtitle="", elevation=1, **kwargs)

    def _setup_ui(self) -> None:
        self._frame = QFrame(self)
        self._frame.setFrameShape(QFrame.StyledPanel)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self._frame)
        self._content_layout = QVBoxLayout(self._frame)
        self._content_layout.setContentsMargins(16, 16, 16, 16)
        self._content_layout.setSpacing(8)
        self._title_label = QLabel(self.get_prop("title", ""))
        self._title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self._title_label.setVisible(bool(self.get_prop("title")))
        self._content_layout.addWidget(self._title_label)
        self._subtitle_label = QLabel(self.get_prop("subtitle", ""))
        self._subtitle_label.setStyleSheet("font-size: 14px; color: #666;")
        self._subtitle_label.setVisible(bool(self.get_prop("subtitle")))
        self._content_layout.addWidget(self._subtitle_label)
        self._apply_styles()

    def _apply_styles(self) -> None:
        self._frame.setStyleSheet("""
            QFrame { background: white; border: 1px solid #e0e0e0; border-radius: 8px; }
        """)

    def add_content(self, widget: QWidget) -> None:
        """Add widget to card content."""
        self._content_layout.addWidget(widget)

    def set_title(self, title: str) -> None:
        self.set_prop("title", title)
        self._title_label.setText(title)
        self._title_label.setVisible(bool(title))
