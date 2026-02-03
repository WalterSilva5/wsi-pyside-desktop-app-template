"""
Layout components module.

Contains structural layout components:
- Header
- Sidebar
- Footer
- ContentArea
- Grid (responsive 12-column grid system)
"""

from src.views.components.layout.header import Header
from src.views.components.layout.sidebar import Sidebar
from src.views.components.layout.footer import Footer
from src.views.components.layout.content_area import ContentArea
from src.views.components.layout.grid import Grid, GridRow, GridColumn, create_responsive_columns
from src.views.components.layout.flow_layout import FlowLayout

__all__ = [
    "Header",
    "Sidebar",
    "Footer",
    "ContentArea",
    "Grid",
    "GridRow",
    "GridColumn",
    "create_responsive_columns",
    "FlowLayout",
]
