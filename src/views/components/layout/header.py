"""
Header component.

Application header with title, navigation controls, and actions.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QPushButton,
)
from PySide6.QtCore import Qt, Signal

from src.views.components.base import BaseComponent
from src.core.container import container
from src.core.types import Theme


class Header(BaseComponent):
    """
    Application header component.

    Features:
    - Dynamic title
    - Back navigation button
    - Theme toggle
    - Custom actions

    Props:
        title: Header title text
        show_back: Show back button
        show_theme_toggle: Show theme toggle button
    """

    # Signals
    back_clicked = Signal()
    theme_toggled = Signal()

    def __init__(
        self,
        title: str = "",
        parent: QWidget | None = None,
        **kwargs
    ) -> None:
        """Initialize the header."""
        super().__init__(parent, title=title, **kwargs)

    def _setup_ui(self) -> None:
        """Setup the header UI."""
        self.setProperty("class", "header")
        self.setFixedHeight(56)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(12)

        # Back button (hidden by default)
        self._back_btn = QPushButton("<")
        self._back_btn.setFixedSize(32, 32)
        self._back_btn.setCursor(Qt.PointingHandCursor)
        self._back_btn.setVisible(self.get_prop("show_back", False))
        self._back_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: 1px solid rgba(128, 128, 128, 0.3);
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(128, 128, 128, 0.15);
            }
        """)
        layout.addWidget(self._back_btn)

        # Title
        self._title_label = QLabel(self.get_prop("title", ""))
        self._title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self._title_label.setProperty("class", "header-title")
        layout.addWidget(self._title_label)

        # Stretch
        layout.addStretch()

        # Theme toggle
        self._theme_btn = QPushButton("🌙")
        self._theme_btn.setFixedSize(36, 36)
        self._theme_btn.setCursor(Qt.PointingHandCursor)
        self._theme_btn.setToolTip("Toggle theme")
        self._theme_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: 1px solid #e0e0e0;
                border-radius: 18px;
                font-size: 16px;
            }
            QPushButton:hover {
                background: #f0f0f0;
            }
        """)
        layout.addWidget(self._theme_btn)

    def _setup_connections(self) -> None:
        """Setup signal connections."""
        self._back_btn.clicked.connect(self._on_back_clicked)
        self._theme_btn.clicked.connect(self._on_theme_toggled)

    def _on_back_clicked(self) -> None:
        """Handle back button click."""
        self.back_clicked.emit()
        from src.services.navigation_service import NavigationService
        nav = container.resolve(NavigationService)
        nav.go_back()

    def _on_theme_toggled(self) -> None:
        """Handle theme toggle click."""
        self.theme_toggled.emit()
        from src.services.theme_service import ThemeService
        theme_service = container.resolve(ThemeService)
        new_theme = theme_service.toggle_theme()
        self._update_theme_icon(new_theme)

    def _update_theme_icon(self, theme: Theme) -> None:
        """Update theme button icon."""
        icon = "☀️" if theme == Theme.DARK else "🌙"
        self._theme_btn.setText(icon)

    def set_title(self, title: str) -> None:
        """Set the header title."""
        self.set_prop("title", title)
        self._title_label.setText(title)

    def show_back_button(self, show: bool = True) -> None:
        """Show or hide the back button."""
        self.set_prop("show_back", show)
        self._back_btn.setVisible(show)

    def _update_ui(self) -> None:
        """Update UI based on props."""
        self._title_label.setText(self.get_prop("title", ""))
        self._back_btn.setVisible(self.get_prop("show_back", False))
