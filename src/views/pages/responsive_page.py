"""
Responsive Layout Demo Page.

Demonstrates the 12-column responsive grid system.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QScrollArea,
    QSizePolicy,
)
from PySide6.QtCore import Qt

from src.views.base import BasePage
from src.views.components.layout.grid import Grid, GridRow, GridColumn
from src.views.components.layout.flow_layout import FlowLayout


class DemoCard(QFrame):
    """A demo card for showcasing grid columns."""

    def __init__(
        self,
        title: str,
        span_info: str,
        color: str = "#0078D4",
        parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)

        self.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 8px;
            }}
        """)
        self.setMinimumHeight(80)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        title_label = QLabel(title)
        title_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        span_label = QLabel(span_info)
        span_label.setStyleSheet("color: rgba(255,255,255,0.8); font-size: 12px;")
        span_label.setAlignment(Qt.AlignCenter)
        span_label.setWordWrap(True)
        layout.addWidget(span_label)


class SimpleFlowCard(QFrame):
    """A simple card for FlowLayout demo."""

    def __init__(
        self,
        title: str,
        color: str = "#0078D4",
        width: int = 200,
        parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)

        self.setFixedWidth(width)
        self.setMinimumHeight(100)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 8px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        title_label = QLabel(title)
        title_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        size_label = QLabel(f"{width}px wide")
        size_label.setStyleSheet("color: rgba(255,255,255,0.7); font-size: 11px;")
        size_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(size_label)


class ResponsivePage(BasePage):
    """
    Responsive Layout Demo Page.

    Demonstrates:
    - FlowLayout for automatic wrapping
    - 12-column grid system
    - Responsive breakpoints (xs, sm, md, lg, xl)
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the responsive demo page."""
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup the UI."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(32)

        # Page title
        title = QLabel("Responsive Grid System")
        title.setProperty("class", "heading")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")
        content_layout.addWidget(title)

        subtitle = QLabel(
            "Resize the window to see cards wrap automatically. "
            "The FlowLayout handles wrapping, while the Grid system "
            "provides Bootstrap-like 12-column behavior."
        )
        subtitle.setProperty("class", "subheading")
        subtitle.setStyleSheet("font-size: 14px; margin-bottom: 16px;")
        subtitle.setWordWrap(True)
        content_layout.addWidget(subtitle)

        # Section 1: Simple FlowLayout Demo
        content_layout.addWidget(self._create_section_title("FlowLayout Demo (Fixed Width Cards)"))
        content_layout.addWidget(self._create_flow_demo())

        # Section 2: Grid with Responsive Columns
        content_layout.addWidget(self._create_section_title("Responsive Grid (12-Column System)"))
        content_layout.addWidget(self._create_responsive_grid_demo())

        # Section 3: Mixed Column Widths
        content_layout.addWidget(self._create_section_title("Mixed Column Widths"))
        content_layout.addWidget(self._create_mixed_columns_demo())

        # Section 4: Real-world Layout
        content_layout.addWidget(self._create_section_title("Real-world Layout Example"))
        content_layout.addWidget(self._create_real_world_demo())

        # Breakpoint info
        content_layout.addWidget(self._create_breakpoint_info())

        content_layout.addStretch()

        scroll.setWidget(content)
        self._main_layout.addWidget(scroll)

    def _create_section_title(self, text: str) -> QLabel:
        """Create a section title."""
        label = QLabel(text)
        label.setStyleSheet(
            "font-size: 18px; font-weight: bold; "
            "margin-top: 16px; padding-bottom: 8px; "
            "border-bottom: 2px solid rgba(128, 128, 128, 0.3);"
        )
        return label

    def _create_flow_demo(self) -> QWidget:
        """Create a simple FlowLayout demo with fixed-width cards."""
        container = QFrame()
        container.setProperty("class", "card")
        container.setStyleSheet("""
            QFrame {
                border: 1px dashed rgba(128, 128, 128, 0.5);
                border-radius: 8px;
            }
        """)

        flow_layout = FlowLayout(container, h_spacing=16, v_spacing=16)
        flow_layout.setContentsMargins(16, 16, 16, 16)

        colors = ["#0078D4", "#28A745", "#FFC107", "#DC3545", "#6F42C1", "#17A2B8"]
        widths = [200, 150, 180, 220, 160, 190, 170, 200]

        for i, (color, width) in enumerate(zip(colors * 2, widths)):
            card = SimpleFlowCard(f"Card {i + 1}", color, width)
            flow_layout.addWidget(card)

        return container

    def _create_responsive_grid_demo(self) -> Grid:
        """Create demo with responsive breakpoints."""
        grid = Grid()

        # Row 1: 4 cards that stack on small screens
        row1 = grid.add_row()
        colors = ["#0078D4", "#28A745", "#FFC107", "#DC3545"]
        for i, color in enumerate(colors):
            col = row1.create_column(
                span=3,      # 4 per row on xl
                lg=3,        # 4 per row on lg
                md=6,        # 2 per row on md
                sm=12,       # 1 per row on sm/xs
            )
            col.add_widget(DemoCard(
                f"Card {i + 1}",
                "xl:3 | md:6 | sm:12",
                color
            ))

        # Row 2: 3 cards
        row2 = grid.add_row()
        colors2 = ["#6F42C1", "#E83E8C", "#20C997"]
        for i, color in enumerate(colors2):
            col = row2.create_column(
                span=4,      # 3 per row on xl/lg
                md=6,        # 2 per row on md (last one wraps)
                sm=12,       # 1 per row on sm/xs
            )
            col.add_widget(DemoCard(
                f"Item {i + 1}",
                "xl:4 | md:6 | sm:12",
                color
            ))

        return grid

    def _create_mixed_columns_demo(self) -> Grid:
        """Create demo with mixed width columns."""
        grid = Grid()

        # Row: 8 + 4 -> becomes 12 + 12 on small screens
        row1 = grid.add_row()
        col1 = row1.create_column(span=8, md=12, sm=12)
        col1.add_widget(DemoCard("Main Content", "xl:8 | md:12 | sm:12", "#6C757D"))
        col2 = row1.create_column(span=4, md=12, sm=12)
        col2.add_widget(DemoCard("Sidebar", "xl:4 | md:12 | sm:12", "#17A2B8"))

        # Row: 3 + 6 + 3
        row2 = grid.add_row()
        col1 = row2.create_column(span=3, md=4, sm=12)
        col1.add_widget(DemoCard("Left", "xl:3 | md:4 | sm:12", "#6F42C1"))
        col2 = row2.create_column(span=6, md=4, sm=12)
        col2.add_widget(DemoCard("Center", "xl:6 | md:4 | sm:12", "#6F42C1"))
        col3 = row2.create_column(span=3, md=4, sm=12)
        col3.add_widget(DemoCard("Right", "xl:3 | md:4 | sm:12", "#6F42C1"))

        return grid

    def _create_real_world_demo(self) -> Grid:
        """Create a real-world layout example."""
        grid = Grid()

        # Header row
        header_row = grid.add_row()
        header_col = header_row.create_column(span=12)
        header_col.add_widget(self._create_content_card(
            "Header / Navigation",
            "Full width header - span=12",
            "#343A40",
            60
        ))

        # Main content row
        main_row = grid.add_row()

        # Sidebar - hides on small screens
        sidebar_col = main_row.create_column(span=3, md=4, sm=12)
        sidebar_col.add_widget(self._create_content_card(
            "Sidebar",
            "xl:3 | md:4 | sm:12\n\nNavigation\nLinks\nFilters",
            "#6C757D",
            180
        ))

        # Main content area
        main_col = main_row.create_column(span=6, md=8, sm=12)
        main_col.add_widget(self._create_content_card(
            "Main Content",
            "xl:6 | md:8 | sm:12\n\nArticles, posts, or main content",
            "#0078D4",
            180
        ))

        # Right sidebar - moves below on medium
        right_col = main_row.create_column(span=3, md=12, sm=12)
        right_col.add_widget(self._create_content_card(
            "Right Panel",
            "xl:3 | md:12 | sm:12\n\nAds or widgets",
            "#28A745",
            180
        ))

        # Footer row
        footer_row = grid.add_row()
        footer_col = footer_row.create_column(span=12)
        footer_col.add_widget(self._create_content_card(
            "Footer",
            "Full width footer - span=12",
            "#343A40",
            60
        ))

        return grid

    def _create_content_card(
        self,
        title: str,
        content: str,
        color: str,
        min_height: int = 80
    ) -> QFrame:
        """Create a content card with title and description."""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 8px;
            }}
        """)
        card.setMinimumHeight(min_height)
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 12, 16, 12)

        title_label = QLabel(title)
        title_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        layout.addWidget(title_label)

        content_label = QLabel(content)
        content_label.setStyleSheet("color: rgba(255,255,255,0.8); font-size: 11px;")
        content_label.setWordWrap(True)
        layout.addWidget(content_label)

        layout.addStretch()

        return card

    def _create_breakpoint_info(self) -> QFrame:
        """Create breakpoint information card."""
        card = QFrame()
        card.setProperty("class", "card")
        card.setStyleSheet("""
            QFrame {
                border-radius: 8px;
            }
        """)
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 16, 16, 16)

        title = QLabel("Breakpoints Reference")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 12px;")
        layout.addWidget(title)

        breakpoints = [
            ("xs", "< 576px", "Extra small devices (phones)"),
            ("sm", ">= 576px", "Small devices (landscape phones)"),
            ("md", ">= 768px", "Medium devices (tablets)"),
            ("lg", ">= 992px", "Large devices (desktops)"),
            ("xl", ">= 1200px", "Extra large devices (large desktops)"),
        ]

        for bp, width, desc in breakpoints:
            row = QHBoxLayout()

            bp_label = QLabel(f"{bp}:")
            bp_label.setStyleSheet("font-weight: bold; color: #0078D4; min-width: 30px;")
            row.addWidget(bp_label)

            width_label = QLabel(width)
            width_label.setStyleSheet("min-width: 80px;")
            row.addWidget(width_label)

            desc_label = QLabel(desc)
            desc_label.setProperty("class", "subheading")
            row.addWidget(desc_label)

            row.addStretch()
            layout.addLayout(row)

        return card

    def on_show(self) -> None:
        """Called when page is shown."""
        self.logger.debug("Responsive demo page shown")
