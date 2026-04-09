"""Testes do DI Container."""

from __future__ import annotations

import pytest


@pytest.mark.usefixtures("fresh_container")
class TestContainer:
    """Testes do `Container` — singleton, transient, factory, instance."""

    def test_singleton_returns_same_instance(self, fresh_container) -> None:
        class Service:
            pass

        fresh_container.register_singleton(Service)
        a = fresh_container.resolve(Service)
        b = fresh_container.resolve(Service)
        assert a is b

    def test_transient_returns_new_instances(self, fresh_container) -> None:
        class Service:
            pass

        fresh_container.register_transient(Service)
        a = fresh_container.resolve(Service)
        b = fresh_container.resolve(Service)
        assert a is not b

    def test_register_instance(self, fresh_container) -> None:
        class Service:
            pass

        existing = Service()
        fresh_container.register_instance(Service, existing)
        assert fresh_container.resolve(Service) is existing

    def test_register_factory(self, fresh_container) -> None:
        counter = {"calls": 0}

        class Service:
            pass

        def factory() -> Service:
            counter["calls"] += 1
            return Service()

        fresh_container.register_factory(Service, factory)
        fresh_container.resolve(Service)
        fresh_container.resolve(Service)
        assert counter["calls"] == 2

    def test_resolve_unregistered_raises(self, fresh_container) -> None:
        class NotRegistered:
            pass

        with pytest.raises(KeyError):
            fresh_container.resolve(NotRegistered)
