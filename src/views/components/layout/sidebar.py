"""
Sidebar component.

Navigation sidebar with menu items.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFrame,
)
from PySide6.QtCore import Qt, Signal

from src.views.components.base import BaseComponent
from src.core.container import container
from src.core.types import PageId


class SidebarItem(QPushButton):
    """Sidebar navigation item."""

    def __init__(self, text: str, icon: str = "", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setText(f"{icon}  {text}" if icon else text)
        self.setCursor(Qt.PointingHandCursor)
        self.setCheckable(True)
        self._setup_style()

    def _setup_style(self) -> None:
        """Setup item style. Colors are controlled by theme QSS."""
        self.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 8px;
                padding: 12px 16px;
                text-align: left;
                font-size: 14px;
            }
            QPushButton:hover {
                background: rgba(128, 128, 128, 0.15);
            }
            QPushButton:checked {
                background: #0078D4;
                color: white;
            }
        """)


class Sidebar(BaseComponent):
    """
    Navigation sidebar component.

    Features:
    - Navigation menu items
    - Active item highlighting
    - Collapsible state
    - App branding

    Props:
        collapsed: Whether sidebar is collapsed
        width: Sidebar width when expanded
    """

    # Signals
    item_clicked = Signal(object)  # PageId
    collapse_toggled = Signal(bool)

    def __init__(self, parent: QWidget | None = None, **kwargs) -> None:
        """Initialize the sidebar."""
        super().__init__(parent, collapsed=False, width=250, **kwargs)
        self._active_page: PageId | None = None
        self._setup_navigation_listener()

    def _setup_ui(self) -> None:
        """Setup the sidebar UI."""
        self.setProperty("class", "sidebar")
        self.setFixedWidth(self.get_prop("width", 250))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 16, 12, 16)
        layout.setSpacing(8)

        # App branding
        brand_frame = QFrame()
        brand_layout = QVBoxLayout(brand_frame)
        brand_layout.setContentsMargins(8, 0, 8, 16)

        app_name = QLabel("PySide6 App")
        app_name.setStyleSheet("font-size: 16px; font-weight: bold;")
        app_name.setProperty("class", "sidebar-title")
        brand_layout.addWidget(app_name)

        version = QLabel("v1.0.0")
        version.setStyleSheet("font-size: 11px;")
        version.setProperty("class", "sidebar-subtitle")
        brand_layout.addWidget(version)

        layout.addWidget(brand_frame)

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setProperty("class", "sidebar-separator")
        separator.setFixedHeight(1)
        layout.addWidget(separator)

        # Navigation section
        nav_label = QLabel("Navigation")
        nav_label.setStyleSheet("font-size: 11px; margin-top: 8px;")
        nav_label.setProperty("class", "sidebar-section")
        layout.addWidget(nav_label)

        # Menu items
        self._items: dict[PageId, SidebarItem] = {}

        menu_items = [
            (PageId.HOME, "Home", "🏠"),
            (PageId.SETTINGS, "Settings", "⚙️"),
            (PageId.SHOWCASE, "Components", "🎨"),
            (PageId.RESPONSIVE, "Responsive", "📐"),
        ]

        for page_id, text, icon in menu_items:
            item = SidebarItem(text, icon)
            item.clicked.connect(lambda checked, pid=page_id: self._on_item_clicked(pid))
            self._items[page_id] = item
            layout.addWidget(item)

        # Stretch
        layout.addStretch()

        # Collapse button
        self._collapse_btn = QPushButton("«")
        self._collapse_btn.setFixedHeight(32)
        self._collapse_btn.setCursor(Qt.PointingHandCursor)
        self._collapse_btn.setToolTip("Collapse sidebar")
        self._collapse_btn.setProperty("class", "sidebar-collapse")
        self._collapse_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: 1px solid rgba(128, 128, 128, 0.3);
                border-radius: 4px;
            }
            QPushButton:hover {
                background: rgba(128, 128, 128, 0.15);
            }
        """)
        self._collapse_btn.clicked.connect(self._toggle_collapse)
        layout.addWidget(self._collapse_btn)

    def _setup_navigation_listener(self) -> None:
        """Listen to navigation changes."""
        from src.services.navigation_service import NavigationService
        nav = container.resolve(NavigationService)
        nav.page_changed.connect(self._on_page_changed)

    def _on_item_clicked(self, page_id: PageId) -> None:
        """Handle menu item click."""
        self.item_clicked.emit(page_id)
        from src.services.navigation_service import NavigationService
        nav = container.resolve(NavigationService)
        nav.navigate_to(page_id)

    def _on_page_changed(self, page_id: PageId, params: dict) -> None:
        """Handle page change."""
        self._active_page = page_id
        self._update_active_item()

    def _update_active_item(self) -> None:
        """Update active item highlighting."""
        for pid, item in self._items.items():
            item.setChecked(pid == self._active_page)

    def _toggle_collapse(self) -> None:
        """Toggle sidebar collapse state."""
        collapsed = not self.get_prop("collapsed", False)
        self.set_prop("collapsed", collapsed)

        if collapsed:
            self.setFixedWidth(60)
            self._collapse_btn.setText("»")
            self._collapse_btn.setToolTip("Expand sidebar")
            # Hide text, show only icons
            for item in self._items.values():
                text = item.text()
                if "  " in text:
                    item.setText(text.split("  ")[0])
        else:
            self.setFixedWidth(self.get_prop("width", 250))
            self._collapse_btn.setText("«")
            self._collapse_btn.setToolTip("Collapse sidebar")
            # Restore full text
            texts = {
                PageId.HOME: "🏠  Home",
                PageId.SETTINGS: "⚙️  Settings",
                PageId.SHOWCASE: "🎨  Components",
                PageId.RESPONSIVE: "📐  Responsive",
            }
            for pid, item in self._items.items():
                item.setText(texts.get(pid, ""))

        self.collapse_toggled.emit(collapsed)

    def set_active(self, page_id: PageId) -> None:
        """Set the active page."""
        self._active_page = page_id
        self._update_active_item()
