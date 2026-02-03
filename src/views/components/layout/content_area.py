"""
Content area component.

Main content container with optional padding and scrolling.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QFrame,
)

from src.views.components.base import BaseComponent


class ContentArea(BaseComponent):
    """
    Content area component.

    Features:
    - Optional scrolling
    - Configurable padding
    - Content container

    Props:
        scrollable: Enable scrolling
        padding: Content padding (default 24)
    """

    def __init__(self, parent: QWidget | None = None, **kwargs) -> None:
        """Initialize the content area."""
        super().__init__(parent, scrollable=True, padding=24, **kwargs)

    def _setup_ui(self) -> None:
        """Setup the content area UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        if self.get_prop("scrollable", True):
            # Scroll area
            self._scroll = QScrollArea()
            self._scroll.setWidgetResizable(True)
            self._scroll.setFrameShape(QFrame.NoFrame)

            # Content widget
            self._content = QWidget()
            self._content_layout = QVBoxLayout(self._content)
            padding = self.get_prop("padding", 24)
            self._content_layout.setContentsMargins(padding, padding, padding, padding)
            self._content_layout.setSpacing(16)

            self._scroll.setWidget(self._content)
            layout.addWidget(self._scroll)
        else:
            # Direct content widget
            self._content = QWidget()
            self._content_layout = QVBoxLayout(self._content)
            padding = self.get_prop("padding", 24)
            self._content_layout.setContentsMargins(padding, padding, padding, padding)
            self._content_layout.setSpacing(16)

            layout.addWidget(self._content)

    def add_widget(self, widget: QWidget) -> None:
        """Add a widget to the content area."""
        self._content_layout.addWidget(widget)

    def add_layout(self, layout) -> None:
        """Add a layout to the content area."""
        self._content_layout.addLayout(layout)

    def add_stretch(self) -> None:
        """Add stretch to content."""
        self._content_layout.addStretch()

    def clear(self) -> None:
        """Clear all content."""
        while self._content_layout.count():
            item = self._content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    @property
    def content_layout(self) -> QVBoxLayout:
        """Get the content layout."""
        return self._content_layout
