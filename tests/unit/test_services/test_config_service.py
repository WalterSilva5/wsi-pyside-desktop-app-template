"""Testes do ConfigService."""

from __future__ import annotations

import pytest


@pytest.mark.usefixtures("reset_services")
class TestConfigService:
    """Testes do `ConfigService` — cobre dot notation e persistência."""

    def test_get_with_default(self) -> None:
        from src.services.config_service import ConfigService

        service = ConfigService()
        assert service.get("definitely.missing.key", "fallback") == "fallback"

    def test_set_and_get_nested_value(self) -> None:
        from src.services.config_service import ConfigService

        service = ConfigService()
        service.set("test.nested.key", "valor", save=False)
        assert service.get("test.nested.key") == "valor"

    def test_has_existing_key(self) -> None:
        from src.services.config_service import ConfigService

        service = ConfigService()
        service.set("teste.has", True, save=False)
        assert service.has("teste.has") is True

    def test_remove_key(self) -> None:
        from src.services.config_service import ConfigService

        service = ConfigService()
        service.set("teste.remove", 42, save=False)
        assert service.remove("teste.remove", save=False) is True
        assert service.get("teste.remove") is None

    def test_get_all_returns_copy(self) -> None:
        from src.services.config_service import ConfigService

        service = ConfigService()
        all_settings = service.get_all()
        # Deve ser uma cópia — modificá-la não afeta o service
        all_settings["__sentinel__"] = "injetado"
        assert service.get("__sentinel__") is None
