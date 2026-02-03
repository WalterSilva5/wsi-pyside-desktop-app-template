"""Tree view component."""
from __future__ import annotations
from typing import Any
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem
from PySide6.QtCore import Signal
from src.views.components.base import BaseComponent


class TreeView(BaseComponent):
    """Tree view for hierarchical data."""

    item_clicked = Signal(object)
    item_expanded = Signal(object)

    def __init__(self, parent: QWidget | None = None, **kwargs) -> None:
        super().__init__(parent, items=[], headers=[], **kwargs)

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self._tree = QTreeWidget()
        self._tree.setStyleSheet("""
            QTreeWidget { border: 1px solid #e0e0e0; border-radius: 8px; }
            QTreeWidget::item { padding: 8px; }
            QTreeWidget::item:hover { background: #f5f5f5; }
            QTreeWidget::item:selected { background: #0078D4; color: white; }
        """)
        headers = self.get_prop("headers", [])
        if headers:
            self._tree.setHeaderLabels(headers)
        else:
            self._tree.setHeaderHidden(True)
        layout.addWidget(self._tree)
        self._populate()

    def _setup_connections(self) -> None:
        self._tree.itemClicked.connect(self._on_item_clicked)
        self._tree.itemExpanded.connect(self._on_item_expanded)

    def _populate(self) -> None:
        self._tree.clear()
        items = self.get_prop("items", [])
        for item in items:
            self._add_item(item, self._tree.invisibleRootItem())

    def _add_item(self, item_data: dict[str, Any], parent: QTreeWidgetItem) -> None:
        text = item_data.get("text", "")
        tree_item = QTreeWidgetItem([text])
        tree_item.setData(0, 1000, item_data)
        parent.addChild(tree_item)
        for child in item_data.get("children", []):
            self._add_item(child, tree_item)

    def _on_item_clicked(self, item: QTreeWidgetItem, column: int) -> None:
        data = item.data(0, 1000)
        self.item_clicked.emit(data)

    def _on_item_expanded(self, item: QTreeWidgetItem) -> None:
        data = item.data(0, 1000)
        self.item_expanded.emit(data)

    def set_items(self, items: list[dict]) -> None:
        self.set_prop("items", items)
        self._populate()
