"""
Configuração e fixtures do pytest.

Este arquivo é lido automaticamente pelo pytest e disponibiliza
fixtures compartilhadas para os testes. Os serviços da aplicação
são singletons (ver `src/services/base.py`), então o fixture
`reset_services` garante isolamento entre testes.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Generator

import pytest

# Garante que `src` está no sys.path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture(scope="session")
def qapp():
    """
    QApplication compartilhado para toda a sessão.

    pytest-qt também fornece `qtbot` e `qapp` próprios — este fixture
    existe para casos em que você só precisa de uma `QApplication`
    sem usar pytest-qt explicitamente.
    """
    from PySide6.QtWidgets import QApplication

    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


@pytest.fixture
def reset_services() -> Generator[None, None, None]:
    """
    Reseta os singletons dos services entre testes.

    Use este fixture em testes que criam ou resolvem services para
    garantir que cada teste começa com um estado limpo.
    """
    from src.services.base import BaseService

    # Guarda o estado anterior e limpa
    saved = dict(BaseService._instances)
    BaseService._instances.clear()
    yield
    # Restaura
    BaseService._instances.clear()
    BaseService._instances.update(saved)


@pytest.fixture
def fresh_container() -> Generator:
    """
    Container DI limpo para cada teste.

    Cuidado: `Container` é singleton, então este fixture limpa o
    container global e o restaura ao final.
    """
    from src.core.container import Container

    c = Container()
    snapshot_services = dict(c._services)
    snapshot_factories = dict(c._factories)
    c.clear()
    yield c
    c._services.clear()
    c._services.update(snapshot_services)
    c._factories.clear()
    c._factories.update(snapshot_factories)
