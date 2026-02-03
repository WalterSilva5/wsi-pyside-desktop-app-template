"""
Settings page view.

Application settings and preferences.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QComboBox,
    QCheckBox,
    QPushButton,
    QScrollArea,
    QGroupBox,
)
from PySide6.QtCore import Qt

from src.views.base import BasePage
from src.core.types import PageId
from src.controllers.settings_controller import SettingsController


class SettingsPage(BasePage):
    """
    Settings page.

    Displays:
    - Theme settings
    - Window settings
    - Application preferences
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the settings page."""
        super().__init__(parent)
        self._controller = SettingsController()
        self._setup_ui()
        self._setup_connections()

    def _setup_ui(self) -> None:
        """Setup the UI."""
        # Scroll area for settings
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        # Content container
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(24)

        # Page title
        title = QLabel("Settings")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #1A1A1A;")
        content_layout.addWidget(title)

        # Theme settings
        theme_group = self._create_theme_settings()
        content_layout.addWidget(theme_group)

        # Window settings
        window_group = self._create_window_settings()
        content_layout.addWidget(window_group)

        # About section
        about_group = self._create_about_section()
        content_layout.addWidget(about_group)

        # Actions
        actions_layout = QHBoxLayout()
        actions_layout.addStretch()

        reset_btn = QPushButton("Reset to Defaults")
        reset_btn.setProperty("class", "secondary")
        reset_btn.clicked.connect(self._on_reset_clicked)
        actions_layout.addWidget(reset_btn)

        content_layout.addLayout(actions_layout)

        # Stretch
        content_layout.addStretch()

        scroll.setWidget(content)
        self._main_layout.addWidget(scroll)

    def _create_theme_settings(self) -> QGroupBox:
        """Create theme settings group."""
        group = QGroupBox("Appearance")
        layout = QVBoxLayout(group)

        # Theme selector
        theme_row = QHBoxLayout()
        theme_label = QLabel("Theme:")
        theme_label.setMinimumWidth(120)
        theme_row.addWidget(theme_label)

        self._theme_combo = QComboBox()
        self._theme_combo.addItem("Light", "light")
        self._theme_combo.addItem("Dark", "dark")
        self._theme_combo.addItem("System", "system")
        self._theme_combo.currentIndexChanged.connect(self._on_theme_changed)
        theme_row.addWidget(self._theme_combo)
        theme_row.addStretch()

        layout.addLayout(theme_row)

        return group

    def _create_window_settings(self) -> QGroupBox:
        """Create window settings group."""
        group = QGroupBox("Window")
        layout = QVBoxLayout(group)

        # Remember size
        self._remember_size_check = QCheckBox("Remember window size")
        self._remember_size_check.stateChanged.connect(
            lambda state: self._controller.set_setting(
                "window.remember_size", state == Qt.Checked
            )
        )
        layout.addWidget(self._remember_size_check)

        # Remember position
        self._remember_pos_check = QCheckBox("Remember window position")
        self._remember_pos_check.stateChanged.connect(
            lambda state: self._controller.set_setting(
                "window.remember_position", state == Qt.Checked
            )
        )
        layout.addWidget(self._remember_pos_check)

        return group

    def _create_about_section(self) -> QGroupBox:
        """Create about section."""
        group = QGroupBox("About")
        layout = QVBoxLayout(group)

        # App info
        app_name = self.config.get("app.name", "PySide6 App Template")
        version = self.config.get("app.version", "1.0.0")

        name_label = QLabel(f"<b>{app_name}</b>")
        name_label.setStyleSheet("color: #1A1A1A;")
        layout.addWidget(name_label)

        version_label = QLabel(f"Version: {version}")
        version_label.setStyleSheet("color: #666666;")
        layout.addWidget(version_label)

        desc_label = QLabel(
            "A scalable PySide6 desktop application template "
            "with design patterns and reusable components."
        )
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #666666; margin-top: 8px;")
        layout.addWidget(desc_label)

        return group

    def _setup_connections(self) -> None:
        """Setup signal connections."""
        self._controller.settings_loaded.connect(self._on_settings_loaded)
        self._controller.theme_changed.connect(self._on_theme_updated)

    def _on_settings_loaded(self, settings: dict) -> None:
        """Handle settings loaded."""
        # Update theme combo
        theme = settings.get("theme", {}).get("current", "light")
        index = self._theme_combo.findData(theme)
        if index >= 0:
            self._theme_combo.setCurrentIndex(index)

        # Update checkboxes
        window = settings.get("window", {})
        self._remember_size_check.setChecked(window.get("remember_size", True))
        self._remember_pos_check.setChecked(window.get("remember_position", True))

    def _on_theme_changed(self, index: int) -> None:
        """Handle theme selection changed."""
        theme = self._theme_combo.currentData()
        if theme:
            self._controller.set_theme(theme)

    def _on_theme_updated(self, theme: str) -> None:
        """Handle theme updated externally."""
        index = self._theme_combo.findData(theme)
        if index >= 0 and self._theme_combo.currentIndex() != index:
            self._theme_combo.blockSignals(True)
            self._theme_combo.setCurrentIndex(index)
            self._theme_combo.blockSignals(False)

    def _on_reset_clicked(self) -> None:
        """Handle reset button clicked."""
        self._controller.reset_to_defaults()
        self.show_toast("Settings reset to defaults", "success")

    def on_first_show(self) -> None:
        """Load settings on first show."""
        self._controller.load_settings()

    def on_show(self) -> None:
        """Called when page is shown."""
        self.logger.debug("Settings page shown")

    def refresh(self) -> None:
        """Refresh the page."""
        self._controller.load_settings()
