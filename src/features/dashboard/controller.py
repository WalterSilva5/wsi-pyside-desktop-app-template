"""
Controller da feature Dashboard.

Orquestra a comunicação entre a página do dashboard e o
`SalesRepository`, oferecendo os dados já calculados (resumo de
métricas) e expondo a lista de vendas filtrada por status.
"""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import Signal

from src.core.base_controller import BaseController
from src.features.dashboard.models.sale import Sale, SaleStatus
from src.features.dashboard.repositories.sales_repository import SalesRepository


@dataclass
class DashboardSummary:
    """Resumo agregado exibido nos cards de métrica."""

    total_sales: int
    total_revenue: float
    average_ticket: float
    unique_customers: int


class DashboardController(BaseController):
    """
    Controller do Dashboard.

    Responsabilidades:
    - Carregar dados do repositório de vendas.
    - Calcular métricas agregadas (summary).
    - Oferecer filtragem por status.
    """

    summary_loaded = Signal(object)  # DashboardSummary
    sales_loaded = Signal(list)  # list[Sale]

    def __init__(self) -> None:
        super().__init__()
        self._repository = SalesRepository()

    def load(self) -> None:
        """Carrega resumo e lista completa de vendas."""
        try:
            self.set_loading(True)
            self.log_action("Loading dashboard data")

            summary = self._build_summary()
            sales = self._repository.get_all()

            self.summary_loaded.emit(summary)
            self.sales_loaded.emit(sales)
        except Exception as error:
            self.handle_error(error, "Failed to load dashboard data")
        finally:
            self.set_loading(False)

    def filter_by_status(self, status: SaleStatus | None) -> list[Sale]:
        """
        Filtra as vendas pelo status informado.

        Args:
            status: Status desejado, ou `None` para retornar todas.
        """
        if status is None:
            sales = self._repository.get_all()
        else:
            sales = self._repository.get_by_status(status)
        self.sales_loaded.emit(sales)
        return sales

    def _build_summary(self) -> DashboardSummary:
        """Gera o resumo agregado a partir do repositório."""
        total_sales = self._repository.count()
        paid_revenue = self._repository.total_revenue()
        paid_count = len(self._repository.get_by_status(SaleStatus.PAID))
        average_ticket = paid_revenue / paid_count if paid_count else 0.0
        unique_customers = self._repository.unique_customers_count()

        return DashboardSummary(
            total_sales=total_sales,
            total_revenue=paid_revenue,
            average_ticket=average_ticket,
            unique_customers=unique_customers,
        )
