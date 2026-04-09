"""
Base component class.

Provides common functionality for all reusable UI components.
"""

from __future__ import annotations

from typing import Any

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal


class BaseComponent(QWidget):
    """
    Base class for all reusable UI components.

    Provides:
    - Props system for configuration
    - Common signals
    - Lifecycle hooks
    - Styling helpers

    All reusable components should inherit from this class.
    """

    # Common signals
    clicked = Signal()
    value_changed = Signal(object)
    state_changed = Signal(object)

    def __init__(self, parent: QWidget | None = None, **kwargs: Any) -> None:
        """
        Initialize the component.

        Args:
            parent: Parent widget
            **kwargs: Component props
        """
        super().__init__(parent)
        self._props: dict[str, Any] = kwargs
        self._is_initialized = False

        self._setup_ui()
        self._setup_connections()
        self._apply_styles()
        self._is_initialized = True

    def _setup_ui(self) -> None:
        """
        Setup the component UI.

        Override in subclasses to create UI elements.
        """
        pass

    def _setup_connections(self) -> None:
        """
        Setup signal connections.

        Override in subclasses to connect signals.
        """
        pass

    def _apply_styles(self) -> None:
        """
        Apply component styles.

        Override in subclasses to apply custom styles.
        """
        pass

    def get_prop(self, key: str, default: Any = None) -> Any:
        """
        Get a component prop value.

        Args:
            key: Prop key
            default: Default value if not found

        Returns:
            Prop value
        """
        return self._props.get(key, default)

    def set_prop(self, key: str, value: Any) -> None:
        """
        Set a component prop value.

        Args:
            key: Prop key
            value: Prop value
        """
        old_value = self._props.get(key)
        self._props[key] = value

        if self._is_initialized and old_value != value:
            self._on_prop_changed(key, old_value, value)

    def set_props(self, **kwargs: Any) -> None:
        """
        Set multiple props at once.

        Args:
            **kwargs: Props to set
        """
        for key, value in kwargs.items():
            self.set_prop(key, value)

    def _on_prop_changed(self, key: str, old_value: Any, new_value: Any) -> None:
        """
        Called when a prop changes.

        Override in subclasses to handle prop changes.

        Args:
            key: Changed prop key
            old_value: Previous value
            new_value: New value
        """
        self._update_ui()

    def _update_ui(self) -> None:
        """
        Update UI based on current props.

        Override in subclasses to update UI elements.
        """
        pass

    @property
    def props(self) -> dict[str, Any]:
        """Get all props."""
        return self._props.copy()
