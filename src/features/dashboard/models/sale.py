"""
Modelo Sale — representa uma venda no dashboard de exemplo.

Este arquivo demonstra como criar modelos específicos de uma feature,
herdando de `BaseModel` (que oferece id, created_at, updated_at e
serialização para dict).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from src.models.base import BaseModel


class SaleStatus(Enum):
    """Status possíveis de uma venda."""

    PAID = "paid"
    PENDING = "pending"
    CANCELLED = "cancelled"


@dataclass
class Sale(BaseModel):
    """
    Venda registrada no sistema.

    Atributos:
        product: Nome do produto vendido.
        customer: Nome do cliente.
        amount: Valor da venda em BRL.
        status: Status atual (paid, pending, cancelled).
        sold_at: Data/hora da venda.
    """

    product: str = ""
    customer: str = ""
    amount: float = 0.0
    status: SaleStatus = SaleStatus.PENDING
    sold_at: datetime = field(default_factory=datetime.now)

    def validate(self) -> None:
        """Valida campos obrigatórios."""
        if not self.product:
            raise ValueError("Sale.product não pode ser vazio")
        if not self.customer:
            raise ValueError("Sale.customer não pode ser vazio")
        if self.amount < 0:
            raise ValueError("Sale.amount não pode ser negativo")
