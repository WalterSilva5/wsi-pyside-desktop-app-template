"""
Repositório de vendas para a feature Dashboard.

Este é um repositório in-memory que fornece dados de exemplo para o
template. Em um projeto real, troque pela implementação adequada
(ex.: `JsonFileRepository` de `src/models/repositories/base.py`, um
repositório HTTP, ou um ORM).
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Iterable

from src.features.dashboard.models.sale import Sale, SaleStatus


class SalesRepository:
    """
    Repositório in-memory de vendas.

    Expõe uma API simples que o `DashboardController` pode consumir:
    - `get_all()`       — lista todas as vendas
    - `get_by_status()` — filtra por status
    - `total_revenue()` — soma dos valores de vendas pagas
    - `unique_customers_count()` — quantos clientes distintos
    """

    def __init__(self) -> None:
        self._sales: list[Sale] = self._build_seed_data()

    @staticmethod
    def _build_seed_data() -> list[Sale]:
        """Gera 20 vendas fictícias para visualização."""
        now = datetime.now()
        seed: list[tuple[str, str, float, SaleStatus, int]] = [
            ("Notebook Pro 15", "Alice Souza", 8499.90, SaleStatus.PAID, 0),
            ("Mouse Ergonômico", "Bruno Lima", 249.00, SaleStatus.PAID, 0),
            ("Teclado Mecânico", "Carla Dias", 659.00, SaleStatus.PAID, 1),
            ("Monitor 27\" 4K", "Diego Alves", 2899.00, SaleStatus.PAID, 1),
            ("Headset Wireless", "Elisa Melo", 899.00, SaleStatus.PENDING, 2),
            ("Webcam Full HD", "Felipe Araújo", 449.00, SaleStatus.PAID, 2),
            ("SSD NVMe 1TB", "Gabriela Nunes", 589.00, SaleStatus.PAID, 3),
            ("Cadeira Gamer", "Hugo Ferreira", 1990.00, SaleStatus.CANCELLED, 3),
            ("Mesa Digitalizadora", "Isabela Castro", 1299.00, SaleStatus.PAID, 4),
            ("Impressora Laser", "João Pereira", 1499.00, SaleStatus.PAID, 5),
            ("Dock USB-C", "Karina Rocha", 799.00, SaleStatus.PENDING, 5),
            ("Pendrive 256GB", "Lucas Teixeira", 149.00, SaleStatus.PAID, 6),
            ("Tablet 10\"", "Marina Silva", 2199.00, SaleStatus.PAID, 6),
            ("Suporte Monitor", "Nicolas Ribeiro", 299.00, SaleStatus.PAID, 7),
            ("Roteador Wi-Fi 6", "Olivia Mendes", 899.00, SaleStatus.PENDING, 7),
            ("HD Externo 4TB", "Paulo Martins", 649.00, SaleStatus.PAID, 8),
            ("Câmera DSLR", "Queila Costa", 4499.00, SaleStatus.CANCELLED, 9),
            ("Fone Bluetooth", "Rafael Gomes", 399.00, SaleStatus.PAID, 10),
            ("Cabo HDMI 2m", "Sofia Andrade", 59.00, SaleStatus.PAID, 11),
            ("Tripé Profissional", "Tiago Barros", 449.00, SaleStatus.PENDING, 12),
        ]
        return [
            Sale(
                product=product,
                customer=customer,
                amount=amount,
                status=status,
                sold_at=now - timedelta(days=days_ago),
            )
            for product, customer, amount, status, days_ago in seed
        ]

    def get_all(self) -> list[Sale]:
        """Retorna todas as vendas (ordenadas do mais recente para o mais antigo)."""
        return sorted(self._sales, key=lambda s: s.sold_at, reverse=True)

    def get_by_status(self, status: SaleStatus) -> list[Sale]:
        """Retorna apenas as vendas com o status informado."""
        return [s for s in self.get_all() if s.status == status]

    def total_revenue(self, statuses: Iterable[SaleStatus] | None = None) -> float:
        """
        Soma o valor das vendas que estão em um dos status informados.

        Args:
            statuses: Status que devem entrar na soma. Se None, usa
                apenas vendas `PAID`.
        """
        allowed = set(statuses) if statuses is not None else {SaleStatus.PAID}
        return sum(s.amount for s in self._sales if s.status in allowed)

    def unique_customers_count(self) -> int:
        """Conta quantos clientes distintos existem na base."""
        return len({s.customer for s in self._sales})

    def count(self) -> int:
        """Número total de vendas."""
        return len(self._sales)
