"""
Responsive Grid Layout System.

A 12-column grid system similar to Bootstrap for responsive layouts.
"""

from __future__ import annotations

from typing import List, Optional
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFrame,
    QSizePolicy,
)
from PySide6.QtCore import Qt, QSize

from src.views.components.base import BaseComponent
from src.views.components.layout.flow_layout import FlowLayout


class GridColumn(QFrame):
    """
    A grid column that spans a specified number of columns out of 12.

    Supports responsive breakpoints:
    - xs: < 576px (extra small)
    - sm: >= 576px (small)
    - md: >= 768px (medium)
    - lg: >= 992px (large)
    - xl: >= 1200px (extra large)
    """

    TOTAL_COLUMNS = 12

    # Breakpoint widths in pixels
    BREAKPOINTS = {
        'xs': 0,
        'sm': 576,
        'md': 768,
        'lg': 992,
        'xl': 1200,
    }

    def __init__(
        self,
        span: int = 12,
        xs: Optional[int] = None,
        sm: Optional[int] = None,
        md: Optional[int] = None,
        lg: Optional[int] = None,
        xl: Optional[int] = None,
        parent: QWidget | None = None
    ) -> None:
        """
        Initialize a grid column.

        Args:
            span: Default column span (1-12)
            xs: Column span for extra small screens
            sm: Column span for small screens
            md: Column span for medium screens
            lg: Column span for large screens
            xl: Column span for extra large screens
            parent: Parent widget
        """
        super().__init__(parent)

        self._default_span = max(1, min(12, span))
        self._responsive_spans = {
            'xs': xs,
            'sm': sm,
            'md': md,
            'lg': lg,
            'xl': xl,
        }
        self._current_span = self._default_span
        self._container_width = 1200
        self._spacing = 16

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(8)

        # Allow column to be resized
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setMinimumWidth(100)

    def add_widget(self, widget: QWidget) -> None:
        """Add a widget to this column."""
        self._layout.addWidget(widget)

    def add_stretch(self) -> None:
        """Add stretch to the column."""
        self._layout.addStretch()

    def get_span_for_width(self, container_width: int) -> int:
        """Get the column span for a given container width."""
        # Determine which breakpoint we're at
        current_breakpoint = 'xs'
        for bp, width in sorted(self.BREAKPOINTS.items(), key=lambda x: x[1], reverse=True):
            if container_width >= width:
                current_breakpoint = bp
                break

        # Check breakpoints from current down to xs
        breakpoint_order = ['xl', 'lg', 'md', 'sm', 'xs']
        start_index = breakpoint_order.index(current_breakpoint)

        for bp in breakpoint_order[start_index:]:
            span = self._responsive_spans.get(bp)
            if span is not None:
                return span

        return self._default_span

    def update_size_for_container(self, container_width: int, spacing: int = 16) -> None:
        """Update the column's size based on container width."""
        self._container_width = max(100, container_width)
        self._spacing = spacing
        self._current_span = self.get_span_for_width(container_width)

        # Calculate width as percentage of container
        # Each column unit is 1/12 of the container
        # Account for spacing: we have (span - 1) internal gaps not needed
        available_width = self._container_width
        column_unit = available_width / 12

        # Width = span * column_unit - spacing (to account for gap)
        width = int(column_unit * self._current_span) - spacing
        width = max(100, width)

        self.setFixedWidth(width)

    def sizeHint(self) -> QSize:
        """Return the preferred size based on current span."""
        available_width = self._container_width
        column_unit = available_width / 12
        width = int(column_unit * self._current_span) - self._spacing
        width = max(100, width)

        # Get height from children
        height = 0
        for i in range(self._layout.count()):
            item = self._layout.itemAt(i)
            if item and item.widget():
                height += item.widget().sizeHint().height()

        return QSize(width, max(height, 80))

    @property
    def default_span(self) -> int:
        """Get the default column span."""
        return self._default_span

    @property
    def current_span(self) -> int:
        """Get the current column span."""
        return self._current_span


class GridRow(QFrame):
    """
    A row in the grid system that contains columns.

    Uses FlowLayout for automatic wrapping when columns exceed available width.
    """

    def __init__(self, parent: QWidget | None = None, spacing: int = 16) -> None:
        """
        Initialize a grid row.

        Args:
            parent: Parent widget
            spacing: Spacing between columns
        """
        super().__init__(parent)

        self._columns: List[GridColumn] = []
        self._spacing = spacing
        self._container_width = 0

        # Use FlowLayout for automatic wrapping
        self._flow_layout = FlowLayout(self, h_spacing=spacing, v_spacing=spacing)
        self._flow_layout.setContentsMargins(0, 0, 0, 0)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    def add_column(self, column: GridColumn) -> GridColumn:
        """Add a column to this row."""
        self._columns.append(column)
        self._flow_layout.addWidget(column)
        # Trigger initial sizing if we have a width
        if self._container_width > 0:
            self._update_column_sizes()
        return column

    def create_column(
        self,
        span: int = 12,
        xs: Optional[int] = None,
        sm: Optional[int] = None,
        md: Optional[int] = None,
        lg: Optional[int] = None,
        xl: Optional[int] = None,
    ) -> GridColumn:
        """Create and add a new column."""
        column = GridColumn(span, xs, sm, md, lg, xl, self)
        return self.add_column(column)

    def _update_column_sizes(self) -> None:
        """Update column sizes based on current container width."""
        if self._container_width <= 0:
            return

        for column in self._columns:
            column.update_size_for_container(self._container_width, self._spacing)

        # Force layout update
        self._flow_layout.invalidate()
        self.updateGeometry()

    def resizeEvent(self, event) -> None:
        """Handle resize to update column sizes."""
        super().resizeEvent(event)
        new_width = event.size().width()
        if new_width > 0 and new_width != self._container_width:
            self._container_width = new_width
            self._update_column_sizes()

    def showEvent(self, event) -> None:
        """Handle show event to ensure proper initial sizing."""
        super().showEvent(event)
        if self._container_width <= 0 and self.width() > 0:
            self._container_width = self.width()
            self._update_column_sizes()


class Grid(BaseComponent):
    """
    A responsive 12-column grid container.

    Usage:
        grid = Grid()

        row1 = grid.add_row()
        col1 = row1.create_column(span=6, md=4, sm=12)  # 6 cols default, 4 on md, 12 on sm
        col1.add_widget(my_widget)

        col2 = row1.create_column(span=6, md=8, sm=12)
        col2.add_widget(another_widget)
    """

    def __init__(self, parent: QWidget | None = None, **kwargs) -> None:
        """Initialize the grid."""
        super().__init__(parent, **kwargs)

    def _setup_ui(self) -> None:
        """Setup the grid UI."""
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(16)

        self._rows: List[GridRow] = []

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    def add_row(self, spacing: int = 16) -> GridRow:
        """Add a new row to the grid."""
        row = GridRow(self, spacing)
        self._rows.append(row)
        self._layout.addWidget(row)
        return row

    def add_stretch(self) -> None:
        """Add stretch at the end of the grid."""
        self._layout.addStretch()

    def clear(self) -> None:
        """Clear all rows from the grid."""
        for row in self._rows:
            self._layout.removeWidget(row)
            row.deleteLater()
        self._rows.clear()


# Convenience function to create a simple grid layout
def create_responsive_columns(
    widgets: List[QWidget],
    columns_lg: int = 4,
    columns_md: int = 6,
    columns_sm: int = 12,
    parent: QWidget | None = None
) -> Grid:
    """
    Create a responsive grid with widgets distributed evenly.

    Args:
        widgets: List of widgets to add
        columns_lg: Column span on large screens (e.g., 4 = 3 columns per row)
        columns_md: Column span on medium screens
        columns_sm: Column span on small screens
        parent: Parent widget

    Returns:
        A Grid with all widgets arranged responsively
    """
    grid = Grid(parent)
    row = grid.add_row()

    for widget in widgets:
        col = row.create_column(
            span=columns_lg,
            lg=columns_lg,
            md=columns_md,
            sm=columns_sm
        )
        col.add_widget(widget)

    return grid
