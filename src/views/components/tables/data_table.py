"""Data table component."""
from __future__ import annotations
from typing import Any
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Signal
from src.views.components.base import BaseComponent


class DataTable(BaseComponent):
    """Data table with sorting."""

    row_clicked = Signal(int, dict)
    row_double_clicked = Signal(int, dict)

    def __init__(self, parent: QWidget | None = None, **kwargs) -> None:
        super().__init__(parent, columns=[], data=[], sortable=True, **kwargs)

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self._table = QTableWidget()
        self._table.setStyleSheet("""
            QTableWidget { border: 1px solid #e0e0e0; border-radius: 8px; }
            QHeaderView::section { background: #f5f5f5; padding: 10px; border: none; font-weight: bold; }
        """)
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._table.verticalHeader().setVisible(False)
        self._table.setSelectionBehavior(QTableWidget.SelectRows)
        self._table.setSortingEnabled(self.get_prop("sortable", True))
        layout.addWidget(self._table)
        self._populate()

    def _setup_connections(self) -> None:
        self._table.cellClicked.connect(self._on_row_clicked)
        self._table.cellDoubleClicked.connect(self._on_row_double_clicked)

    def _populate(self) -> None:
        columns = self.get_prop("columns", [])
        data = self.get_prop("data", [])
        self._table.setColumnCount(len(columns))
        self._table.setHorizontalHeaderLabels([c.get("label", "") for c in columns])
        self._table.setRowCount(len(data))
        for row_idx, row_data in enumerate(data):
            for col_idx, col in enumerate(columns):
                key = col.get("key", "")
                value = str(row_data.get(key, ""))
                self._table.setItem(row_idx, col_idx, QTableWidgetItem(value))

    def _on_row_clicked(self, row: int, col: int) -> None:
        data = self.get_prop("data", [])
        if 0 <= row < len(data):
            self.row_clicked.emit(row, data[row])

    def _on_row_double_clicked(self, row: int, col: int) -> None:
        data = self.get_prop("data", [])
        if 0 <= row < len(data):
            self.row_double_clicked.emit(row, data[row])

    def set_data(self, data: list[dict[str, Any]]) -> None:
        self.set_prop("data", data)
        self._populate()

    def get_selected_row(self) -> int:
        return self._table.currentRow()
