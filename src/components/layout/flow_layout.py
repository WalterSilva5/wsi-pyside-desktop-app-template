"""
Flow Layout implementation.

A layout that arranges widgets in a flow, wrapping to the next line when needed.
Similar to CSS flexbox with flex-wrap: wrap.
"""

from __future__ import annotations

from PySide6.QtWidgets import QLayout, QWidgetItem, QSizePolicy, QWidget
from PySide6.QtCore import Qt, QRect, QSize, QPoint


class FlowLayout(QLayout):
    """
    A layout that arranges child widgets horizontally, wrapping to new rows as needed.

    This layout is ideal for responsive designs where widgets should flow
    and wrap based on available width.
    """

    def __init__(self, parent: QWidget | None = None, h_spacing: int = 16, v_spacing: int = 16) -> None:
        """
        Initialize the flow layout.

        Args:
            parent: Parent widget
            h_spacing: Horizontal spacing between items
            v_spacing: Vertical spacing between rows
        """
        super().__init__(parent)
        self._items: list[QWidgetItem] = []
        self._h_spacing = h_spacing
        self._v_spacing = v_spacing

    def addItem(self, item: QWidgetItem) -> None:
        """Add an item to the layout."""
        self._items.append(item)

    def count(self) -> int:
        """Return number of items in layout."""
        return len(self._items)

    def itemAt(self, index: int) -> QWidgetItem | None:
        """Return item at index."""
        if 0 <= index < len(self._items):
            return self._items[index]
        return None

    def takeAt(self, index: int) -> QWidgetItem | None:
        """Remove and return item at index."""
        if 0 <= index < len(self._items):
            return self._items.pop(index)
        return None

    def expandingDirections(self) -> Qt.Orientation:
        """Return expanding directions."""
        return Qt.Orientation(0)

    def hasHeightForWidth(self) -> bool:
        """This layout's height depends on its width."""
        return True

    def heightForWidth(self, width: int) -> int:
        """Calculate the height needed for the given width."""
        return self._do_layout(QRect(0, 0, width, 0), test_only=True)

    def setGeometry(self, rect: QRect) -> None:
        """Set the geometry of the layout."""
        super().setGeometry(rect)
        self._do_layout(rect, test_only=False)

    def sizeHint(self) -> QSize:
        """Return the preferred size."""
        return self.minimumSize()

    def minimumSize(self) -> QSize:
        """Return the minimum size."""
        size = QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())

        margins = self.contentsMargins()
        size += QSize(margins.left() + margins.right(), margins.top() + margins.bottom())
        return size

    def _do_layout(self, rect: QRect, test_only: bool) -> int:
        """
        Arrange items within the given rectangle.

        Args:
            rect: The rectangle to arrange items in
            test_only: If True, only calculate height without moving widgets

        Returns:
            The height of the laid out items
        """
        margins = self.contentsMargins()
        effective_rect = rect.adjusted(margins.left(), margins.top(), -margins.right(), -margins.bottom())

        x = effective_rect.x()
        y = effective_rect.y()
        line_height = 0

        for item in self._items:
            widget = item.widget()
            if widget is None or not widget.isVisible():
                continue

            # Get the size hint for this item
            item_size = item.sizeHint()

            # Check if we need to wrap to next line
            next_x = x + item_size.width()
            if next_x > effective_rect.right() + 1 and line_height > 0:
                # Wrap to next line
                x = effective_rect.x()
                y = y + line_height + self._v_spacing
                next_x = x + item_size.width()
                line_height = 0

            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), item_size))

            x = next_x + self._h_spacing
            line_height = max(line_height, item_size.height())

        return y + line_height - rect.y() + margins.bottom()

    def set_horizontal_spacing(self, spacing: int) -> None:
        """Set horizontal spacing between items."""
        self._h_spacing = spacing
        self.invalidate()

    def set_vertical_spacing(self, spacing: int) -> None:
        """Set vertical spacing between rows."""
        self._v_spacing = spacing
        self.invalidate()

    def horizontal_spacing(self) -> int:
        """Get horizontal spacing."""
        return self._h_spacing

    def vertical_spacing(self) -> int:
        """Get vertical spacing."""
        return self._v_spacing
