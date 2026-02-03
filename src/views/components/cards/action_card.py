"""Action card component."""
from __future__ import annotations
from typing import Any
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton
from PySide6.QtCore import Qt
from src.views.components.base import BaseComponent


class ActionCard(BaseComponent):
    """Card with action buttons."""

    def __init__(self, title: str = "", description: str = "", parent: QWidget | None = None, **kwargs) -> None:
        super().__init__(parent, title=title, description=description, actions=[], **kwargs)

    def _setup_ui(self) -> None:
        self._frame = QFrame(self)
        self._frame.setStyleSheet("QFrame { background: white; border: 1px solid #e0e0e0; border-radius: 8px; padding: 16px; }")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self._frame)
        content_layout = QVBoxLayout(self._frame)
        self._title_label = QLabel(self.get_prop("title", ""))
        self._title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        content_layout.addWidget(self._title_label)
        self._desc_label = QLabel(self.get_prop("description", ""))
        self._desc_label.setStyleSheet("font-size: 14px; color: #666;")
        self._desc_label.setWordWrap(True)
        content_layout.addWidget(self._desc_label)
        self._actions_layout = QHBoxLayout()
        self._actions_layout.addStretch()
        content_layout.addLayout(self._actions_layout)
        self._setup_actions()

    def _setup_actions(self) -> None:
        actions = self.get_prop("actions", [])
        for action in actions:
            btn = QPushButton(action.get("text", ""))
            btn.setCursor(Qt.PointingHandCursor)
            variant = action.get("variant", "primary")
            if variant == "danger":
                btn.setStyleSheet("QPushButton { background: #dc3545; color: white; border: none; border-radius: 4px; padding: 8px 16px; }")
            else:
                btn.setStyleSheet("QPushButton { background: #0078D4; color: white; border: none; border-radius: 4px; padding: 8px 16px; }")
            callback = action.get("callback")
            if callback:
                btn.clicked.connect(callback)
            self._actions_layout.addWidget(btn)

    def add_action(self, text: str, callback: Any, variant: str = "primary") -> None:
        """Add an action button."""
        actions = self.get_prop("actions", [])
        actions.append({"text": text, "callback": callback, "variant": variant})
        self.set_prop("actions", actions)
