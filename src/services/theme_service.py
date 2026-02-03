"""
Theme Service.

Manages application themes and stylesheets.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QApplication

from src.core.types import Theme
from src.services.base import BaseService


class ThemeService(BaseService):
    """
    Theme/Styling Service.

    Manages application themes with:
    - Light/Dark theme support
    - QSS stylesheet loading
    - System theme detection
    - Change notifications

    Usage:
        theme_service = ThemeService()
        theme_service.set_theme(Theme.DARK)
        theme_service.theme_changed.connect(my_handler)
    """

    # Signals
    theme_changed = Signal(object)  # Theme

    def _on_init(self) -> None:
        """Initialize the theme service."""
        self._current_theme = Theme.LIGHT
        self._styles_path = self._find_styles_path()

    def _find_styles_path(self) -> Path:
        """Find the styles directory with fallback options."""
        # Try relative to this file (src/services/theme_service.py -> resources/styles)
        path1 = Path(__file__).parent.parent.parent / "resources" / "styles"
        if path1.exists():
            return path1

        # Try relative to CWD
        path2 = Path.cwd() / "resources" / "styles"
        if path2.exists():
            return path2

        # Try using __file__ of the main module
        import sys
        if hasattr(sys.modules.get('__main__'), '__file__') and sys.modules['__main__'].__file__:
            main_file = Path(sys.modules['__main__'].__file__).resolve()
            path3 = main_file.parent / "resources" / "styles"
            if path3.exists():
                return path3

        # Fallback to first option even if it doesn't exist
        return path1

    def set_theme(self, theme: Theme) -> None:
        """
        Set the application theme.

        Args:
            theme: Theme to apply
        """
        if theme == Theme.SYSTEM:
            theme = self._detect_system_theme()

        self._current_theme = theme
        self._apply_theme()
        self.theme_changed.emit(theme)

    def get_current_theme(self) -> Theme:
        """Get the current theme."""
        return self._current_theme

    def toggle_theme(self) -> Theme:
        """
        Toggle between light and dark themes.

        Returns:
            The new theme
        """
        new_theme = Theme.DARK if self._current_theme == Theme.LIGHT else Theme.LIGHT
        self.set_theme(new_theme)
        return new_theme

    def apply_current_theme(self) -> None:
        """Apply the current theme to the application."""
        self._apply_theme()

    def _apply_theme(self) -> None:
        """Apply the current theme stylesheet."""
        app = QApplication.instance()
        if not app:
            return

        # Load base stylesheet
        base_qss = self._load_stylesheet("base.qss")

        # Load theme-specific stylesheet
        theme_file = f"{self._current_theme.value}.qss"
        theme_qss = self._load_stylesheet(theme_file)

        # Combine and apply
        full_stylesheet = base_qss + "\n" + theme_qss
        app.setStyleSheet(full_stylesheet)

        # Also set palette for native widgets
        self._apply_palette()

    def _load_stylesheet(self, filename: str) -> str:
        """Load a stylesheet file."""
        file_path = self._styles_path / filename
        if file_path.exists():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    return f.read()
            except IOError:
                return ""
        return ""

    def _apply_palette(self) -> None:
        """Apply color palette for native widgets."""
        app = QApplication.instance()
        if not app:
            return

        palette = QPalette()

        if self._current_theme == Theme.DARK:
            # Dark theme colors
            palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.Base, QColor(45, 45, 45))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(55, 55, 55))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.Button, QColor(55, 55, 55))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
            palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))
        else:
            # Light theme colors (matching light.qss: #F5F5F5 = 245,245,245)
            palette.setColor(QPalette.ColorRole.Window, QColor(245, 245, 245))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(26, 26, 26))  # #1A1A1A
            palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(245, 245, 245))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(26, 26, 26))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.Text, QColor(26, 26, 26))  # #1A1A1A
            palette.setColor(QPalette.ColorRole.Button, QColor(245, 245, 245))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(26, 26, 26))
            palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
            palette.setColor(QPalette.ColorRole.Link, QColor(0, 120, 212))  # #0078D4
            palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 120, 212))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(102, 102, 102))  # #666666

        app.setPalette(palette)

    def _detect_system_theme(self) -> Theme:
        """
        Detect the system theme preference.

        Returns:
            Theme.DARK or Theme.LIGHT based on system settings
        """
        app = QApplication.instance()
        if app:
            palette = app.palette()
            bg_color = palette.color(QPalette.ColorRole.Window)
            # If background is dark, system is using dark theme
            if bg_color.lightness() < 128:
                return Theme.DARK
        return Theme.LIGHT

    def get_color(self, color_name: str) -> QColor:
        """
        Get a theme color by name.

        Args:
            color_name: Name of the color (primary, secondary, etc.)

        Returns:
            QColor for the requested color
        """
        colors = {
            "primary": QColor(0, 120, 215) if self._current_theme == Theme.LIGHT else QColor(42, 130, 218),
            "secondary": QColor(108, 117, 125),
            "success": QColor(40, 167, 69),
            "danger": QColor(220, 53, 69),
            "warning": QColor(255, 193, 7),
            "info": QColor(23, 162, 184),
            "light": QColor(248, 249, 250),
            "dark": QColor(52, 58, 64),
            "background": QColor(255, 255, 255) if self._current_theme == Theme.LIGHT else QColor(30, 30, 30),
            "surface": QColor(255, 255, 255) if self._current_theme == Theme.LIGHT else QColor(45, 45, 45),
            "text": QColor(33, 37, 41) if self._current_theme == Theme.LIGHT else QColor(255, 255, 255),
            "text_secondary": QColor(108, 117, 125) if self._current_theme == Theme.LIGHT else QColor(170, 170, 170),
            "border": QColor(222, 226, 230) if self._current_theme == Theme.LIGHT else QColor(68, 68, 68),
        }
        return colors.get(color_name, QColor(0, 0, 0))

    @property
    def is_dark(self) -> bool:
        """Check if current theme is dark."""
        return self._current_theme == Theme.DARK

    @property
    def styles_path(self) -> Path:
        """Get the styles directory path."""
        return self._styles_path
