"""
Component showcase page.

Displays examples of all reusable components.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QTabWidget,
    QScrollArea,
    QGridLayout,
    QPushButton,
    QLineEdit,
    QComboBox,
    QCheckBox,
    QRadioButton,
    QProgressBar,
    QSlider,
    QSpinBox,
    QTextEdit,
    QGroupBox,
    QButtonGroup,
)
from PySide6.QtCore import Qt

from src.views.base import BasePage
from src.controllers.showcase_controller import ShowcaseController


class ShowcasePage(BasePage):
    """
    Component showcase page.

    Displays:
    - Button variants
    - Card components
    - Form inputs
    - Feedback components
    - And more...
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the showcase page."""
        super().__init__(parent)
        self._controller = ShowcaseController()
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup the UI."""
        # Content container
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(16)

        # Page title
        title = QLabel("Component Showcase")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        content_layout.addWidget(title)

        subtitle = QLabel("Examples of reusable UI components")
        subtitle.setStyleSheet("font-size: 14px; color: #666; margin-bottom: 16px;")
        content_layout.addWidget(subtitle)

        # Tab widget for categories
        tabs = QTabWidget()
        tabs.addTab(self._create_buttons_tab(), "Buttons")
        tabs.addTab(self._create_inputs_tab(), "Inputs")
        tabs.addTab(self._create_cards_tab(), "Cards")
        tabs.addTab(self._create_feedback_tab(), "Feedback")
        tabs.addTab(self._create_layout_tab(), "Layout")

        content_layout.addWidget(tabs)

        self._main_layout.addWidget(content)

    def _create_buttons_tab(self) -> QWidget:
        """Create buttons showcase tab."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(24)

        # Primary buttons
        primary_group = QGroupBox("Primary Buttons")
        primary_layout = QHBoxLayout(primary_group)

        btn_small = QPushButton("Small")
        btn_small.setStyleSheet(self._get_primary_button_style("small"))
        primary_layout.addWidget(btn_small)

        btn_medium = QPushButton("Medium")
        btn_medium.setStyleSheet(self._get_primary_button_style("medium"))
        primary_layout.addWidget(btn_medium)

        btn_large = QPushButton("Large")
        btn_large.setStyleSheet(self._get_primary_button_style("large"))
        primary_layout.addWidget(btn_large)

        btn_disabled = QPushButton("Disabled")
        btn_disabled.setEnabled(False)
        btn_disabled.setStyleSheet(self._get_primary_button_style("medium"))
        primary_layout.addWidget(btn_disabled)

        primary_layout.addStretch()
        layout.addWidget(primary_group)

        # Secondary buttons
        secondary_group = QGroupBox("Secondary Buttons")
        secondary_layout = QHBoxLayout(secondary_group)

        for text in ["Default", "Outline", "Ghost"]:
            btn = QPushButton(text)
            btn.setStyleSheet(self._get_secondary_button_style())
            secondary_layout.addWidget(btn)

        secondary_layout.addStretch()
        layout.addWidget(secondary_group)

        # Danger buttons
        danger_group = QGroupBox("Danger Buttons")
        danger_layout = QHBoxLayout(danger_group)

        btn_danger = QPushButton("Delete")
        btn_danger.setStyleSheet(self._get_danger_button_style())
        danger_layout.addWidget(btn_danger)

        btn_danger_outline = QPushButton("Remove")
        btn_danger_outline.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #dc3545;
                border: 1px solid #dc3545;
                padding: 8px 16px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background: #dc3545;
                color: white;
            }
        """)
        danger_layout.addWidget(btn_danger_outline)

        danger_layout.addStretch()
        layout.addWidget(danger_group)

        layout.addStretch()
        scroll.setWidget(widget)
        return scroll

    def _create_inputs_tab(self) -> QWidget:
        """Create inputs showcase tab."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(24)

        # Text inputs
        text_group = QGroupBox("Text Inputs")
        text_layout = QGridLayout(text_group)

        text_layout.addWidget(QLabel("Default:"), 0, 0)
        text_layout.addWidget(QLineEdit(), 0, 1)

        text_layout.addWidget(QLabel("Placeholder:"), 1, 0)
        placeholder_input = QLineEdit()
        placeholder_input.setPlaceholderText("Enter your name...")
        text_layout.addWidget(placeholder_input, 1, 1)

        text_layout.addWidget(QLabel("Disabled:"), 2, 0)
        disabled_input = QLineEdit("Disabled input")
        disabled_input.setEnabled(False)
        text_layout.addWidget(disabled_input, 2, 1)

        text_layout.addWidget(QLabel("Password:"), 3, 0)
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.Password)
        password_input.setPlaceholderText("Enter password...")
        text_layout.addWidget(password_input, 3, 1)

        layout.addWidget(text_group)

        # Selects
        select_group = QGroupBox("Select Inputs")
        select_layout = QGridLayout(select_group)

        select_layout.addWidget(QLabel("Dropdown:"), 0, 0)
        combo = QComboBox()
        combo.addItems(["Option 1", "Option 2", "Option 3"])
        select_layout.addWidget(combo, 0, 1)

        select_layout.addWidget(QLabel("Editable:"), 1, 0)
        editable_combo = QComboBox()
        editable_combo.setEditable(True)
        editable_combo.addItems(["Apple", "Banana", "Orange"])
        select_layout.addWidget(editable_combo, 1, 1)

        layout.addWidget(select_group)

        # Checkboxes and Radios
        checks_group = QGroupBox("Checkboxes & Radio Buttons")
        checks_layout = QHBoxLayout(checks_group)

        check_layout = QVBoxLayout()
        check_layout.addWidget(QCheckBox("Option A"))
        check_layout.addWidget(QCheckBox("Option B (checked)"))
        checks_layout.widget().findChildren(QCheckBox)[1].setChecked(True) if checks_layout.widget() else None

        cb = QCheckBox("Option B (checked)")
        cb.setChecked(True)
        check_layout.addWidget(cb)

        cb_disabled = QCheckBox("Disabled")
        cb_disabled.setEnabled(False)
        check_layout.addWidget(cb_disabled)
        checks_layout.addLayout(check_layout)

        radio_layout = QVBoxLayout()
        radio_group = QButtonGroup(widget)
        for i, text in enumerate(["Radio 1", "Radio 2", "Radio 3"]):
            radio = QRadioButton(text)
            if i == 0:
                radio.setChecked(True)
            radio_group.addButton(radio)
            radio_layout.addWidget(radio)
        checks_layout.addLayout(radio_layout)

        checks_layout.addStretch()
        layout.addWidget(checks_group)

        # Spinbox and Slider
        numbers_group = QGroupBox("Number Inputs")
        numbers_layout = QGridLayout(numbers_group)

        numbers_layout.addWidget(QLabel("Spin Box:"), 0, 0)
        spin = QSpinBox()
        spin.setRange(0, 100)
        spin.setValue(50)
        numbers_layout.addWidget(spin, 0, 1)

        numbers_layout.addWidget(QLabel("Slider:"), 1, 0)
        slider = QSlider(Qt.Horizontal)
        slider.setRange(0, 100)
        slider.setValue(50)
        numbers_layout.addWidget(slider, 1, 1)

        layout.addWidget(numbers_group)

        # Text area
        textarea_group = QGroupBox("Text Area")
        textarea_layout = QVBoxLayout(textarea_group)

        textarea = QTextEdit()
        textarea.setPlaceholderText("Enter multiple lines of text...")
        textarea.setMaximumHeight(100)
        textarea_layout.addWidget(textarea)

        layout.addWidget(textarea_group)

        layout.addStretch()
        scroll.setWidget(widget)
        return scroll

    def _create_cards_tab(self) -> QWidget:
        """Create cards showcase tab."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(24)

        # Basic cards
        cards_layout = QHBoxLayout()

        for i, (title, content) in enumerate([
            ("Basic Card", "This is a basic card with simple content."),
            ("Card with Shadow", "This card has a higher elevation."),
            ("Bordered Card", "This card uses a border style."),
        ]):
            card = QFrame()
            card.setStyleSheet(f"""
                QFrame {{
                    background: white;
                    border: 1px solid #e0e0e0;
                    border-radius: 8px;
                    padding: 16px;
                    {'box-shadow: 0 4px 6px rgba(0,0,0,0.1);' if i == 1 else ''}
                }}
            """)
            card_layout = QVBoxLayout(card)

            title_label = QLabel(title)
            title_label.setStyleSheet("font-weight: bold; font-size: 16px;")
            card_layout.addWidget(title_label)

            content_label = QLabel(content)
            content_label.setWordWrap(True)
            content_label.setStyleSheet("color: #666;")
            card_layout.addWidget(content_label)

            cards_layout.addWidget(card)

        layout.addLayout(cards_layout)

        # Info cards
        info_group = QGroupBox("Info Cards")
        info_layout = QHBoxLayout(info_group)

        for title, value, color in [
            ("Users", "1,234", "#0078D4"),
            ("Revenue", "$12.5K", "#28A745"),
            ("Orders", "567", "#FFC107"),
            ("Errors", "12", "#DC3545"),
        ]:
            card = QFrame()
            card.setStyleSheet(f"""
                QFrame {{
                    background: white;
                    border-left: 4px solid {color};
                    border-radius: 4px;
                    padding: 16px;
                    min-width: 120px;
                }}
            """)
            card_layout = QVBoxLayout(card)

            value_label = QLabel(value)
            value_label.setStyleSheet("font-size: 24px; font-weight: bold;")
            card_layout.addWidget(value_label)

            title_label = QLabel(title)
            title_label.setStyleSheet("color: #666;")
            card_layout.addWidget(title_label)

            info_layout.addWidget(card)

        info_layout.addStretch()
        layout.addWidget(info_group)

        layout.addStretch()
        scroll.setWidget(widget)
        return scroll

    def _create_feedback_tab(self) -> QWidget:
        """Create feedback components showcase tab."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(24)

        # Progress bars
        progress_group = QGroupBox("Progress Bars")
        progress_layout = QVBoxLayout(progress_group)

        for value in [25, 50, 75, 100]:
            row = QHBoxLayout()
            label = QLabel(f"{value}%")
            label.setMinimumWidth(40)
            row.addWidget(label)

            progress = QProgressBar()
            progress.setValue(value)
            row.addWidget(progress)

            progress_layout.addLayout(row)

        layout.addWidget(progress_group)

        # Badges
        badges_group = QGroupBox("Badges")
        badges_layout = QHBoxLayout(badges_group)

        for text, color, bg in [
            ("Primary", "white", "#0078D4"),
            ("Success", "white", "#28A745"),
            ("Warning", "black", "#FFC107"),
            ("Danger", "white", "#DC3545"),
            ("Info", "white", "#17A2B8"),
        ]:
            badge = QLabel(text)
            badge.setStyleSheet(f"""
                QLabel {{
                    background: {bg};
                    color: {color};
                    padding: 4px 12px;
                    border-radius: 12px;
                    font-size: 12px;
                    font-weight: bold;
                }}
            """)
            badges_layout.addWidget(badge)

        badges_layout.addStretch()
        layout.addWidget(badges_group)

        # Alerts
        alerts_group = QGroupBox("Alerts")
        alerts_layout = QVBoxLayout(alerts_group)

        for alert_type, bg, border, text in [
            ("Info", "#cfe2ff", "#b6d4fe", "This is an informational message."),
            ("Success", "#d1e7dd", "#badbcc", "Operation completed successfully!"),
            ("Warning", "#fff3cd", "#ffecb5", "Please review your changes."),
            ("Error", "#f8d7da", "#f5c2c7", "An error occurred. Please try again."),
        ]:
            alert = QFrame()
            alert.setStyleSheet(f"""
                QFrame {{
                    background: {bg};
                    border: 1px solid {border};
                    border-radius: 6px;
                    padding: 12px;
                }}
            """)
            alert_layout = QHBoxLayout(alert)

            type_label = QLabel(f"<b>{alert_type}:</b>")
            alert_layout.addWidget(type_label)

            text_label = QLabel(text)
            alert_layout.addWidget(text_label)
            alert_layout.addStretch()

            alerts_layout.addWidget(alert)

        layout.addWidget(alerts_group)

        layout.addStretch()
        scroll.setWidget(widget)
        return scroll

    def _create_layout_tab(self) -> QWidget:
        """Create layout components showcase tab."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(24)

        # Grid example
        grid_group = QGroupBox("Grid Layout")
        grid_layout = QGridLayout(grid_group)

        for i in range(3):
            for j in range(4):
                cell = QFrame()
                cell.setStyleSheet("""
                    QFrame {
                        background: #e9ecef;
                        border: 1px solid #dee2e6;
                        border-radius: 4px;
                        min-height: 60px;
                    }
                """)
                cell_layout = QVBoxLayout(cell)
                cell_layout.addWidget(QLabel(f"Cell ({i},{j})"), alignment=Qt.AlignCenter)
                grid_layout.addWidget(cell, i, j)

        layout.addWidget(grid_group)

        # Spacing example
        spacing_group = QGroupBox("Spacing")
        spacing_layout = QVBoxLayout(spacing_group)

        for spacing, label in [(8, "Compact (8px)"), (16, "Normal (16px)"), (24, "Relaxed (24px)")]:
            row = QHBoxLayout()
            row.setSpacing(spacing)

            row_label = QLabel(label)
            row_label.setMinimumWidth(120)
            row.addWidget(row_label)

            for _ in range(4):
                box = QFrame()
                box.setFixedSize(40, 40)
                box.setStyleSheet("background: #0078D4; border-radius: 4px;")
                row.addWidget(box)

            row.addStretch()
            spacing_layout.addLayout(row)

        layout.addWidget(spacing_group)

        layout.addStretch()
        scroll.setWidget(widget)
        return scroll

    def _get_primary_button_style(self, size: str = "medium") -> str:
        """Get primary button style."""
        sizes = {
            "small": "padding: 4px 12px; font-size: 12px;",
            "medium": "padding: 8px 16px; font-size: 14px;",
            "large": "padding: 12px 24px; font-size: 16px;",
        }
        return f"""
            QPushButton {{
                background-color: #0078D4;
                color: white;
                border: none;
                border-radius: 6px;
                {sizes.get(size, sizes['medium'])}
            }}
            QPushButton:hover {{
                background-color: #106EBE;
            }}
            QPushButton:pressed {{
                background-color: #005A9E;
            }}
            QPushButton:disabled {{
                background-color: #cccccc;
            }}
        """

    def _get_secondary_button_style(self) -> str:
        """Get secondary button style."""
        return """
            QPushButton {
                background-color: white;
                color: #333;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
                border-color: #d0d0d0;
            }
        """

    def _get_danger_button_style(self) -> str:
        """Get danger button style."""
        return """
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """

    def on_show(self) -> None:
        """Called when page is shown."""
        self.logger.debug("Showcase page shown")
