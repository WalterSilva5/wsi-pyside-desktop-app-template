"""Icon component."""
from __future__ import annotations
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QStyle
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QSize
from src.views.components.base import BaseComponent


class Icon(BaseComponent):
    """Icon display component."""

    def __init__(self, icon: QIcon | None = None, parent: QWidget | None = None, **kwargs) -> None:
        super().__init__(parent, icon=icon, size=24, color="", **kwargs)

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self._label = QLabel()
        size = self.get_prop("size", 24)
        self._label.setFixedSize(size, size)
        self._label.setAlignment(Qt.AlignCenter)
        icon = self.get_prop("icon")
        if icon:
            pixmap = icon.pixmap(QSize(size, size))
            self._label.setPixmap(pixmap)
        layout.addWidget(self._label)

    def set_icon(self, icon: QIcon) -> None:
        self.set_prop("icon", icon)
        size = self.get_prop("size", 24)
        pixmap = icon.pixmap(QSize(size, size))
        self._label.setPixmap(pixmap)

    def set_size(self, size: int) -> None:
        self.set_prop("size", size)
        self._label.setFixedSize(size, size)
        icon = self.get_prop("icon")
        if icon:
            pixmap = icon.pixmap(QSize(size, size))
            self._label.setPixmap(pixmap)

    @staticmethod
    def from_standard(style_icon: QStyle.StandardPixmap, size: int = 24) -> Icon:
        """Create icon from Qt standard icon."""
        from PySide6.QtWidgets import QApplication
        app = QApplication.instance()
        if app:
            icon = app.style().standardIcon(style_icon)
            return Icon(icon=icon, size=size)
        return Icon(size=size)
