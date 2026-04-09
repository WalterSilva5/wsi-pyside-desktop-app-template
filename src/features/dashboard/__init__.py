"""
Feature Dashboard — exemplo de feature com modelos e repositórios próprios.

Demonstra como organizar uma feature mais rica que precisa de:
- Modelos de dados específicos (Sale)
- Repositório próprio (SalesRepository)
- Controller orquestrando dados para a view
- Página consumindo cards de métrica + tabela de dados
"""

from src.features.dashboard.page import DashboardPage
from src.features.dashboard.controller import DashboardController

__all__ = ["DashboardPage", "DashboardController"]
