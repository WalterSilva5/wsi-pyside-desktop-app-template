"""Tests for NavigationService."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest


class TestNavigationService:
    """Test cases for NavigationService."""

    def test_register_page(self):
        """Test registering a page."""
        from src.core.types import PageId
        from src.services.navigation_service import NavigationService

        service = NavigationService()
        mock_page = MagicMock()

        service.register_page(PageId.HOME, mock_page)

        assert PageId.HOME in service._pages
        assert service._pages[PageId.HOME] == mock_page

    def test_navigate_to(self):
        """Test navigating to a page."""
        from src.core.types import PageId
        from src.services.navigation_service import NavigationService

        service = NavigationService()
        mock_page = MagicMock()
        service.register_page(PageId.HOME, mock_page)

        result = service.navigate_to(PageId.HOME)

        assert result is True
        assert service.current_page == PageId.HOME

    def test_navigate_to_unregistered_page(self):
        """Test navigating to unregistered page fails."""
        from src.core.types import PageId
        from src.services.navigation_service import NavigationService

        service = NavigationService()

        result = service.navigate_to(PageId.HOME)

        assert result is False

    def test_navigation_history(self):
        """Test navigation history is maintained."""
        from src.core.types import PageId
        from src.services.navigation_service import NavigationService

        service = NavigationService()
        service.register_page(PageId.HOME, MagicMock())
        service.register_page(PageId.SETTINGS, MagicMock())

        service.navigate_to(PageId.HOME)
        service.navigate_to(PageId.SETTINGS)

        assert len(service._history) == 2
        assert service._history[0] == PageId.HOME
        assert service._history[1] == PageId.SETTINGS

    def test_go_back(self):
        """Test going back in history."""
        from src.core.types import PageId
        from src.services.navigation_service import NavigationService

        service = NavigationService()
        service.register_page(PageId.HOME, MagicMock())
        service.register_page(PageId.SETTINGS, MagicMock())

        service.navigate_to(PageId.HOME)
        service.navigate_to(PageId.SETTINGS)
        result = service.go_back()

        assert result is True
        assert service.current_page == PageId.HOME

    def test_go_back_empty_history(self):
        """Test going back with empty history fails."""
        from src.services.navigation_service import NavigationService

        service = NavigationService()

        result = service.go_back()

        assert result is False

    def test_can_go_back(self):
        """Test checking if can go back."""
        from src.core.types import PageId
        from src.services.navigation_service import NavigationService

        service = NavigationService()
        service.register_page(PageId.HOME, MagicMock())
        service.register_page(PageId.SETTINGS, MagicMock())

        assert service.can_go_back is False

        service.navigate_to(PageId.HOME)
        assert service.can_go_back is False

        service.navigate_to(PageId.SETTINGS)
        assert service.can_go_back is True

    def test_clear_history(self):
        """Test clearing navigation history."""
        from src.core.types import PageId
        from src.services.navigation_service import NavigationService

        service = NavigationService()
        service.register_page(PageId.HOME, MagicMock())
        service.register_page(PageId.SETTINGS, MagicMock())

        service.navigate_to(PageId.HOME)
        service.navigate_to(PageId.SETTINGS)
        service.clear_history()

        assert len(service._history) == 0
        assert service.can_go_back is False


class TestNavigationServiceCallbacks:
    """Test navigation callbacks."""

    def test_on_navigate_callback(self):
        """Test on_navigate callback is called."""
        from src.core.types import PageId
        from src.services.navigation_service import NavigationService

        service = NavigationService()
        mock_page = MagicMock()
        mock_page.on_navigate = MagicMock()
        mock_page.on_show = MagicMock()

        service.register_page(PageId.HOME, mock_page)
        service.navigate_to(PageId.HOME)

        mock_page.on_navigate.assert_called_once()

    def test_on_hide_callback(self):
        """Test on_hide callback is called when leaving page."""
        from src.core.types import PageId
        from src.services.navigation_service import NavigationService

        service = NavigationService()

        mock_home = MagicMock()
        mock_home.on_navigate = MagicMock()
        mock_home.on_show = MagicMock()
        mock_home.on_hide = MagicMock()

        mock_settings = MagicMock()
        mock_settings.on_navigate = MagicMock()
        mock_settings.on_show = MagicMock()

        service.register_page(PageId.HOME, mock_home)
        service.register_page(PageId.SETTINGS, mock_settings)

        service.navigate_to(PageId.HOME)
        service.navigate_to(PageId.SETTINGS)

        mock_home.on_hide.assert_called_once()


class TestNavigationServiceEdgeCases:
    """Edge case tests for NavigationService."""

    def test_navigate_to_same_page(self):
        """Test navigating to same page doesn't add to history."""
        from src.core.types import PageId
        from src.services.navigation_service import NavigationService

        service = NavigationService()
        service.register_page(PageId.HOME, MagicMock())

        service.navigate_to(PageId.HOME)
        initial_history_len = len(service._history)

        service.navigate_to(PageId.HOME)

        # Should not duplicate in history
        assert len(service._history) == initial_history_len

    def test_history_limit(self):
        """Test history has a reasonable limit."""
        from src.core.types import PageId
        from src.services.navigation_service import NavigationService

        service = NavigationService()
        service.register_page(PageId.HOME, MagicMock())
        service.register_page(PageId.SETTINGS, MagicMock())

        # Navigate many times
        for i in range(100):
            page = PageId.HOME if i % 2 == 0 else PageId.SETTINGS
            service.navigate_to(page)

        # History should be bounded
        assert len(service._history) <= 50  # Reasonable limit
