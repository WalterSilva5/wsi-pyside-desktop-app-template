"""
Home page view.

The main landing page of the application.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGridLayout,
    QFrame,
)
from PySide6.QtCore import Qt

from src.views.base import BasePage
from src.core.types import PageId
from src.controllers.home_controller import HomeController


class HomePage(BasePage):
    """
    Home page.

    Displays:
    - Welcome message
    - Quick stats cards
    - Navigation shortcuts
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the home page."""
        super().__init__(parent)
        self._controller = HomeController()
        self._setup_ui()
        self._setup_connections()

    def _setup_ui(self) -> None:
        """Setup the UI."""
        # Content container
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(24)

        # Welcome section
        welcome_section = self._create_welcome_section()
        content_layout.addWidget(welcome_section)

        # Stats section
        stats_section = self._create_stats_section()
        content_layout.addWidget(stats_section)

        # Quick actions section
        actions_section = self._create_actions_section()
        content_layout.addWidget(actions_section)

        # Stretch to fill
        content_layout.addStretch()

        self._main_layout.addWidget(content)

    def _create_welcome_section(self) -> QWidget:
        """Create the welcome section."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # Title
        self._title_label = QLabel("Welcome to PySide6 App Template")
        self._title_label.setProperty("class", "heading")
        self._title_label.setStyleSheet("font-size: 28px; font-weight: bold;")
        layout.addWidget(self._title_label)

        # Subtitle
        subtitle = QLabel("A scalable template with design patterns and reusable components")
        subtitle.setProperty("class", "subheading")
        subtitle.setStyleSheet("font-size: 16px;")
        layout.addWidget(subtitle)

        return widget

    def _create_stats_section(self) -> QWidget:
        """Create the stats cards section."""
        widget = QWidget()
        layout = QGridLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        stats = [
            {"title": "Pages", "value": "3", "color": "#0078D4"},
            {"title": "Components", "value": "20+", "color": "#28A745"},
            {"title": "Services", "value": "5", "color": "#FFC107"},
            {"title": "Design Patterns", "value": "5", "color": "#DC3545"},
        ]

        for i, stat in enumerate(stats):
            card = self._create_stat_card(stat["title"], stat["value"], stat["color"])
            layout.addWidget(card, 0, i)

        return widget

    def _create_stat_card(self, title: str, value: str, color: str) -> QFrame:
        """Create a stat card."""
        card = QFrame()
        card.setProperty("class", "card")
        card.setStyleSheet(f"""
            QFrame {{
                border-radius: 8px;
                padding: 16px;
                border-left: 4px solid {color};
            }}
        """)

        layout = QVBoxLayout(card)

        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 32px; font-weight: bold;")
        layout.addWidget(value_label)

        title_label = QLabel(title)
        title_label.setProperty("class", "subheading")
        title_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(title_label)

        return card

    def _create_actions_section(self) -> QWidget:
        """Create quick actions section."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # Section title
        section_title = QLabel("Quick Actions")
        section_title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 16px;")
        layout.addWidget(section_title)

        # Actions row
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(16)

        actions = [
            {"title": "Settings", "description": "Configure application", "action": self._go_to_settings},
            {"title": "Components", "description": "View component showcase", "action": self._go_to_showcase},
            {"title": "Toggle Theme", "description": "Switch light/dark mode", "action": self._toggle_theme},
        ]

        for action in actions:
            card = self._create_action_card(
                action["title"],
                action["description"],
                action["action"]
            )
            actions_layout.addWidget(card)

        actions_layout.addStretch()
        layout.addLayout(actions_layout)

        return widget

    def _create_action_card(self, title: str, description: str, callback) -> QFrame:
        """Create an action card."""
        card = QFrame()
        card.setProperty("class", "card")
        card.setCursor(Qt.PointingHandCursor)
        card.setStyleSheet("""
            QFrame {
                border-radius: 8px;
                padding: 16px;
                min-width: 200px;
            }
            QFrame:hover {
                border-color: #0078D4;
            }
        """)

        layout = QVBoxLayout(card)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)

        desc_label = QLabel(description)
        desc_label.setProperty("class", "subheading")
        desc_label.setStyleSheet("font-size: 13px;")
        layout.addWidget(desc_label)

        # Make card clickable
        card.mousePressEvent = lambda e: callback()

        return card

    def _setup_connections(self) -> None:
        """Setup signal connections."""
        self._controller.dashboard_data_loaded.connect(self._on_dashboard_loaded)
        self._controller.welcome_message_changed.connect(self._on_welcome_message_changed)

    def _on_dashboard_loaded(self, data: dict) -> None:
        """Handle dashboard data loaded."""
        app_name = data.get("app_name", "PySide6 App")
        self._title_label.setText(f"Welcome to {app_name}")

    def _on_welcome_message_changed(self, message: str) -> None:
        """Handle welcome message changed."""
        self._title_label.setText(message)

    def _go_to_settings(self) -> None:
        """Navigate to settings page."""
        self.navigate_to(PageId.SETTINGS)

    def _go_to_showcase(self) -> None:
        """Navigate to showcase page."""
        self.navigate_to(PageId.SHOWCASE)

    def _toggle_theme(self) -> None:
        """Toggle the application theme."""
        from src.core.container import container
        from src.services.theme_service import ThemeService
        theme_service = container.resolve(ThemeService)
        theme_service.toggle_theme()

    def on_first_show(self) -> None:
        """Load data on first show."""
        self._controller.load_dashboard_data()

    def on_show(self) -> None:
        """Called when page is shown."""
        self.logger.debug("Home page shown")

    def refresh(self) -> None:
        """Refresh the page."""
        self._controller.refresh()
