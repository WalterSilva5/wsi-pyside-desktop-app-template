"""Testes do NavigationService."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from src.core.exceptions import NavigationError


@pytest.mark.usefixtures("reset_services")
class TestNavigationService:
    """Testes do `NavigationService` — registro, navegação e history."""

    def test_register_and_navigate(self, qapp) -> None:
        from src.core.types import PageId
        from src.services.navigation_service import NavigationService

        service = NavigationService()
        mock_page = MagicMock()
        service.register_page(PageId.HOME, mock_page)

        assert service.navigate_to(PageId.HOME) is True
        assert service.get_current_page_id() == PageId.HOME

    def test_navigate_to_unregistered_raises(self, qapp) -> None:
        from src.core.types import PageId
        from src.services.navigation_service import NavigationService

        service = NavigationService()
        with pytest.raises(NavigationError):
            service.navigate_to(PageId.HOME)

    def test_history_back_and_forward(self, qapp) -> None:
        from src.core.types import PageId
        from src.services.navigation_service import NavigationService

        service = NavigationService()
        service.register_page(PageId.HOME, MagicMock())
        service.register_page(PageId.SETTINGS, MagicMock())

        service.navigate_to(PageId.HOME)
        service.navigate_to(PageId.SETTINGS)
        assert service.can_go_back() is True
        assert service.go_back() is True
        assert service.get_current_page_id() == PageId.HOME
        assert service.can_go_forward() is True
        assert service.go_forward() is True
        assert service.get_current_page_id() == PageId.SETTINGS

    def test_on_navigate_callback_called(self, qapp) -> None:
        from src.core.types import PageId
        from src.services.navigation_service import NavigationService

        service = NavigationService()
        page = MagicMock()
        service.register_page(PageId.HOME, page)
        service.navigate_to(PageId.HOME, {"x": 1})

        page.on_navigate.assert_called_once_with({"x": 1})

    def test_guard_blocks_navigation(self, qapp) -> None:
        from src.core.types import PageId
        from src.services.navigation_service import NavigationService

        service = NavigationService()
        service.register_page(PageId.HOME, MagicMock())

        service.add_guard(lambda _page_id, _params: False)
        assert service.navigate_to(PageId.HOME) is False
