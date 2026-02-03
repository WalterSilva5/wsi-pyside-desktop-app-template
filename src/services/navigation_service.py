"""
Navigation Service.

Manages page navigation with history support.
Implements type-safe routing using PageId enum.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, TYPE_CHECKING

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QStackedWidget, QWidget

from src.core.types import PageId
from src.core.exceptions import NavigationError
from src.services.base import BaseService

if TYPE_CHECKING:
    from src.views.base import BasePage


@dataclass
class NavigationEntry:
    """Navigation history entry."""
    page_id: PageId
    params: dict[str, Any] = field(default_factory=dict)


NavigationGuard = Callable[[PageId, dict[str, Any]], bool]


class NavigationService(BaseService):
    """
    Navigation/Router Service.

    Features:
    - Type-safe navigation using PageId enum
    - Navigation history with back support
    - Navigation guards for access control
    - Parameter passing between pages
    - Page lifecycle hooks

    Usage:
        nav = NavigationService()

        # Register pages
        nav.register_page(PageId.HOME, home_page)

        # Navigate
        nav.navigate_to(PageId.SETTINGS, {"tab": "general"})

        # Go back
        nav.go_back()

        # Add guard
        nav.add_guard(my_auth_guard)
    """

    # Signals
    page_changed = Signal(object, dict)  # page_id, params
    navigation_started = Signal(object, dict)  # page_id, params
    navigation_completed = Signal(object)  # page_id
    navigation_failed = Signal(object, str)  # page_id, error
    can_go_back_changed = Signal(bool)

    def _on_init(self) -> None:
        """Initialize the navigation service."""
        self._stack_widget: QStackedWidget | None = None
        self._pages: dict[PageId, QWidget] = {}
        self._history: list[NavigationEntry] = []
        self._current_index: int = -1
        self._guards: list[NavigationGuard] = []
        self._default_page: PageId | None = None

    def set_stack_widget(self, stack: QStackedWidget) -> None:
        """
        Set the QStackedWidget for navigation.

        Args:
            stack: The QStackedWidget that holds all pages
        """
        self._stack_widget = stack

    def register_page(
        self,
        page_id: PageId,
        page: QWidget,
        is_default: bool = False
    ) -> None:
        """
        Register a page with the navigation service.

        Args:
            page_id: Unique identifier for the page
            page: The page widget
            is_default: Whether this is the default/home page
        """
        self._pages[page_id] = page

        if self._stack_widget:
            self._stack_widget.addWidget(page)

        if is_default:
            self._default_page = page_id

    def unregister_page(self, page_id: PageId) -> bool:
        """
        Unregister a page.

        Args:
            page_id: Page to unregister

        Returns:
            True if unregistered, False if not found
        """
        if page_id in self._pages:
            page = self._pages[page_id]
            if self._stack_widget:
                self._stack_widget.removeWidget(page)
            del self._pages[page_id]
            return True
        return False

    def navigate_to(
        self,
        page_id: PageId,
        params: dict[str, Any] | None = None
    ) -> bool:
        """
        Navigate to a page.

        Args:
            page_id: Target page identifier
            params: Optional parameters to pass to the page

        Returns:
            True if navigation successful, False otherwise

        Raises:
            NavigationError: If page is not registered
        """
        params = params or {}

        # Emit navigation started
        self.navigation_started.emit(page_id, params)

        # Check if page is registered
        if page_id not in self._pages:
            error_msg = f"Page {page_id.name} not registered"
            self.navigation_failed.emit(page_id, error_msg)
            raise NavigationError(error_msg, page_id=page_id)

        # Run navigation guards
        if not self._run_guards(page_id, params):
            self.navigation_failed.emit(page_id, "Navigation blocked by guard")
            return False

        # Truncate forward history if navigating from middle
        if self._current_index < len(self._history) - 1:
            self._history = self._history[:self._current_index + 1]

        # Add to history
        entry = NavigationEntry(page_id, params)
        self._history.append(entry)
        self._current_index = len(self._history) - 1

        # Get and update page
        page = self._pages[page_id]

        # Call page lifecycle hook if available
        if hasattr(page, "on_navigate"):
            page.on_navigate(params)

        # Update stack widget
        if self._stack_widget:
            self._stack_widget.setCurrentWidget(page)

        # Emit signals
        self.page_changed.emit(page_id, params)
        self.navigation_completed.emit(page_id)
        self.can_go_back_changed.emit(self.can_go_back())

        return True

    def go_back(self) -> bool:
        """
        Navigate back in history.

        Returns:
            True if navigation successful, False if at beginning
        """
        if not self.can_go_back():
            return False

        self._current_index -= 1
        entry = self._history[self._current_index]

        page = self._pages[entry.page_id]

        # Call page lifecycle hook
        if hasattr(page, "on_navigate"):
            page.on_navigate(entry.params)

        # Update stack widget
        if self._stack_widget:
            self._stack_widget.setCurrentWidget(page)

        # Emit signals
        self.page_changed.emit(entry.page_id, entry.params)
        self.navigation_completed.emit(entry.page_id)
        self.can_go_back_changed.emit(self.can_go_back())

        return True

    def go_forward(self) -> bool:
        """
        Navigate forward in history.

        Returns:
            True if navigation successful, False if at end
        """
        if not self.can_go_forward():
            return False

        self._current_index += 1
        entry = self._history[self._current_index]

        page = self._pages[entry.page_id]

        # Call page lifecycle hook
        if hasattr(page, "on_navigate"):
            page.on_navigate(entry.params)

        # Update stack widget
        if self._stack_widget:
            self._stack_widget.setCurrentWidget(page)

        # Emit signals
        self.page_changed.emit(entry.page_id, entry.params)
        self.can_go_back_changed.emit(self.can_go_back())

        return True

    def go_home(self) -> bool:
        """
        Navigate to the default/home page.

        Returns:
            True if navigation successful
        """
        if self._default_page:
            return self.navigate_to(self._default_page)
        return False

    def can_go_back(self) -> bool:
        """Check if back navigation is possible."""
        return self._current_index > 0

    def can_go_forward(self) -> bool:
        """Check if forward navigation is possible."""
        return self._current_index < len(self._history) - 1

    def get_current_page_id(self) -> PageId | None:
        """Get current page ID."""
        if 0 <= self._current_index < len(self._history):
            return self._history[self._current_index].page_id
        return None

    def get_current_page(self) -> QWidget | None:
        """Get current page widget."""
        page_id = self.get_current_page_id()
        if page_id:
            return self._pages.get(page_id)
        return None

    def get_current_params(self) -> dict[str, Any]:
        """Get current page parameters."""
        if 0 <= self._current_index < len(self._history):
            return self._history[self._current_index].params
        return {}

    def add_guard(self, guard: NavigationGuard) -> None:
        """
        Add a navigation guard.

        Guards are functions that return True to allow navigation
        or False to block it.

        Args:
            guard: Guard function (page_id, params) -> bool
        """
        self._guards.append(guard)

    def remove_guard(self, guard: NavigationGuard) -> bool:
        """
        Remove a navigation guard.

        Args:
            guard: Guard to remove

        Returns:
            True if removed, False if not found
        """
        if guard in self._guards:
            self._guards.remove(guard)
            return True
        return False

    def _run_guards(self, page_id: PageId, params: dict[str, Any]) -> bool:
        """
        Run all navigation guards.

        Returns:
            True if all guards pass, False otherwise
        """
        for guard in self._guards:
            try:
                if not guard(page_id, params):
                    return False
            except Exception:
                return False
        return True

    def clear_history(self) -> None:
        """Clear navigation history."""
        self._history.clear()
        self._current_index = -1
        self.can_go_back_changed.emit(False)

    def get_history(self) -> list[NavigationEntry]:
        """Get navigation history."""
        return self._history.copy()

    def is_page_registered(self, page_id: PageId) -> bool:
        """Check if a page is registered."""
        return page_id in self._pages

    def get_registered_pages(self) -> list[PageId]:
        """Get list of registered page IDs."""
        return list(self._pages.keys())
