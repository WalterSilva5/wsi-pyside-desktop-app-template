"""List view component."""
from __future__ import annotations
from typing import Any
from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem
from PySide6.QtCore import Signal
from src.views.components.base import BaseComponent


class ListView(BaseComponent):
    """Simple list view."""

    item_clicked = Signal(int, object)
    item_double_clicked = Signal(int, object)

    def __init__(self, parent: QWidget | None = None, **kwargs) -> None:
        super().__init__(parent, items=[], **kwargs)

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self._list = QListWidget()
        self._list.setStyleSheet("""
            QListWidget { border: 1px solid #e0e0e0; border-radius: 8px; }
            QListWidget::item { padding: 12px; }
            QListWidget::item:hover { background: #f5f5f5; }
            QListWidget::item:selected { background: #0078D4; color: white; }
        """)
        layout.addWidget(self._list)
        self._populate()

    def _setup_connections(self) -> None:
        self._list.itemClicked.connect(self._on_item_clicked)
        self._list.itemDoubleClicked.connect(self._on_item_double_clicked)

    def _populate(self) -> None:
        self._list.clear()
        for item in self.get_prop("items", []):
            text = item if isinstance(item, str) else item.get("text", str(item))
            self._list.addItem(text)

    def _on_item_clicked(self, item: QListWidgetItem) -> None:
        row = self._list.row(item)
        items = self.get_prop("items", [])
        data = items[row] if row < len(items) else None
        self.item_clicked.emit(row, data)

    def _on_item_double_clicked(self, item: QListWidgetItem) -> None:
        row = self._list.row(item)
        items = self.get_prop("items", [])
        data = items[row] if row < len(items) else None
        self.item_double_clicked.emit(row, data)

    def set_items(self, items: list) -> None:
        self.set_prop("items", items)
        self._populate()

    def get_selected_index(self) -> int:
        return self._list.currentRow()
