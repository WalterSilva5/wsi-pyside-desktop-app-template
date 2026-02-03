"""Page Factory."""
from __future__ import annotations
from typing import Type, Any
from PySide6.QtWidgets import QWidget
from src.core.types import PageId


class PageFactory:
    """Factory for creating pages."""

    _pages: dict[PageId, Type[QWidget]] = {}

    @classmethod
    def register(cls, page_id: PageId, page_class: Type[QWidget]) -> None:
        """Register a page class."""
        cls._pages[page_id] = page_class

    @classmethod
    def create(cls, page_id: PageId, parent: QWidget | None = None, **kwargs: Any) -> QWidget:
        """Create a page by ID."""
        if page_id not in cls._pages:
            raise ValueError(f"Page '{page_id}' not registered")
        return cls._pages[page_id](parent, **kwargs)

    @classmethod
    def get_registered(cls) -> list[PageId]:
        """Get list of registered pages."""
        return list(cls._pages.keys())

    @classmethod
    def is_registered(cls, page_id: PageId) -> bool:
        """Check if a page is registered."""
        return page_id in cls._pages


def register_default_pages() -> None:
    """Register all default pages."""
    from src.views.pages.home_page import HomePage
    from src.views.pages.settings_page import SettingsPage
    from src.views.pages.showcase_page import ShowcasePage

    PageFactory.register(PageId.HOME, HomePage)
    PageFactory.register(PageId.SETTINGS, SettingsPage)
    PageFactory.register(PageId.SHOWCASE, ShowcasePage)
