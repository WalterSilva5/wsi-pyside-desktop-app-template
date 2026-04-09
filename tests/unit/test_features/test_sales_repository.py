"""Testes do SalesRepository (feature Dashboard)."""

from __future__ import annotations

from src.features.dashboard.models.sale import SaleStatus
from src.features.dashboard.repositories.sales_repository import SalesRepository


class TestSalesRepository:
    """Exemplo de teste de repositório específico de uma feature."""

    def test_get_all_returns_non_empty_and_sorted_desc(self) -> None:
        repo = SalesRepository()
        sales = repo.get_all()
        assert len(sales) > 0

        # Ordenado do mais recente para o mais antigo
        timestamps = [s.sold_at for s in sales]
        assert timestamps == sorted(timestamps, reverse=True)

    def test_filter_by_status_returns_only_matching(self) -> None:
        repo = SalesRepository()
        paid = repo.get_by_status(SaleStatus.PAID)
        assert all(s.status == SaleStatus.PAID for s in paid)

    def test_total_revenue_uses_only_paid_by_default(self) -> None:
        repo = SalesRepository()
        total = repo.total_revenue()
        paid_sum = sum(s.amount for s in repo.get_by_status(SaleStatus.PAID))
        assert total == paid_sum

    def test_unique_customers_count_positive(self) -> None:
        repo = SalesRepository()
        assert repo.unique_customers_count() > 0

    def test_count_matches_len_of_get_all(self) -> None:
        repo = SalesRepository()
        assert repo.count() == len(repo.get_all())
