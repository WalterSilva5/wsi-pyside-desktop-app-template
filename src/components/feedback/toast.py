"""Toast notification component."""
from __future__ import annotations
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication
from PySide6.QtCore import QTimer, Qt, QPropertyAnimation, QPoint
from PySide6.QtGui import QGuiApplication


class Toast(QWidget):
    """Toast notification."""

    _instances: list[Toast] = []

    def __init__(self, message: str, toast_type: str = "info", duration: int = 3000, parent: QWidget | None = None) -> None:
        super().__init__(parent, Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self._message = message
        self._toast_type = toast_type
        self._duration = duration
        self._setup_ui()
        Toast._instances.append(self)

    def _setup_ui(self) -> None:
        colors = {"info": "#0078D4", "success": "#28A745", "warning": "#FFC107", "error": "#DC3545"}
        bg = colors.get(self._toast_type, colors["info"])
        fg = "black" if self._toast_type == "warning" else "white"
        self.setStyleSheet(f"background: {bg}; border-radius: 8px;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        label = QLabel(self._message)
        label.setStyleSheet(f"color: {fg}; font-size: 14px;")
        layout.addWidget(label)
        self.adjustSize()

    def show_toast(self) -> None:
        screen = QGuiApplication.primaryScreen()
        if screen:
            geo = screen.availableGeometry()
            x = geo.right() - self.width() - 20
            y = geo.bottom() - self.height() - 20 - (len(Toast._instances) - 1) * 60
            self.move(x, y)
        self.show()
        QTimer.singleShot(self._duration, self._hide)

    def _hide(self) -> None:
        if self in Toast._instances:
            Toast._instances.remove(self)
        self.close()
        self.deleteLater()

    @classmethod
    def show(cls, message: str, toast_type: str = "info", duration: int = 3000) -> Toast:
        toast = cls(message, toast_type, duration)
        toast.show_toast()
        return toast
