"""
Página do Dashboard.

Exemplo de feature que consome um repositório próprio através do
`DashboardController`. Mostra quatro cards de métricas, um filtro
por status e uma tabela com todas as vendas.

Esta página serve como referência de "feature rica" para o template —
use-a como ponto de partida quando precisar criar uma tela que
combina dados agregados + listagem + filtros.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from src.components.cards.info_card import InfoCard
from src.components.tables.data_table import DataTable
from src.core.base_page import BasePage
from src.features.dashboard.controller import DashboardController, DashboardSummary
from src.features.dashboard.models.sale import Sale, SaleStatus


_STATUS_LABELS: dict[SaleStatus, str] = {
    SaleStatus.PAID: "Pago",
    SaleStatus.PENDING: "Pendente",
    SaleStatus.CANCELLED: "Cancelado",
}


def _format_currency(value: float) -> str:
    """Formata valor em Real brasileiro (ex.: 1234.5 → 'R$ 1.234,50')."""
    formatted = f"{value:,.2f}"
    formatted = formatted.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {formatted}"


class DashboardPage(BasePage):
    """
    Página do Dashboard.

    Layout:
        ┌─────────────────────────────────────────────┐
        │  Dashboard                                  │
        │  [Card] [Card] [Card] [Card]                │
        │                                             │
        │  Filtro: [Todas ▾]                          │
        │  ┌─ Tabela de vendas ────────────────────┐  │
        │  │ Produto | Cliente | Valor | Status    │  │
        │  └───────────────────────────────────────┘  │
        └─────────────────────────────────────────────┘
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._controller = DashboardController()
        self._setup_ui()
        self._setup_connections()

    # ------------------------------------------------------------------ UI

    def _setup_ui(self) -> None:
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(24)

        layout.addWidget(self._build_header())
        layout.addWidget(self._build_metrics_row())
        layout.addWidget(self._build_filter_row())
        layout.addWidget(self._build_table(), 1)

        self._main_layout.addWidget(content)

    def _build_header(self) -> QWidget:
        wrapper = QWidget()
        box = QVBoxLayout(wrapper)
        box.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Dashboard")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")
        box.addWidget(title)

        subtitle = QLabel(
            "Visão geral das vendas — exemplo de feature com modelo, "
            "repositório e controlador próprios."
        )
        subtitle.setStyleSheet("font-size: 14px; color: #666;")
        subtitle.setWordWrap(True)
        box.addWidget(subtitle)

        return wrapper

    def _build_metrics_row(self) -> QWidget:
        wrapper = QWidget()
        row = QHBoxLayout(wrapper)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(16)

        self._total_sales_card = InfoCard(title="Total de Vendas", value="0", color="#0078D4")
        self._revenue_card = InfoCard(title="Receita (Pagas)", value="R$ 0,00", color="#28A745")
        self._ticket_card = InfoCard(title="Ticket Médio", value="R$ 0,00", color="#FFC107")
        self._customers_card = InfoCard(title="Clientes Únicos", value="0", color="#DC3545")

        for card in (
            self._total_sales_card,
            self._revenue_card,
            self._ticket_card,
            self._customers_card,
        ):
            row.addWidget(card, 1)

        return wrapper

    def _build_filter_row(self) -> QWidget:
        wrapper = QWidget()
        row = QHBoxLayout(wrapper)
        row.setContentsMargins(0, 0, 0, 0)

        label = QLabel("Filtrar por status:")
        label.setStyleSheet("font-size: 13px; color: #333;")
        row.addWidget(label)

        self._status_combo = QComboBox()
        self._status_combo.addItem("Todas", None)
        for status, status_label in _STATUS_LABELS.items():
            self._status_combo.addItem(status_label, status)
        self._status_combo.setMinimumWidth(160)
        row.addWidget(self._status_combo)

        row.addStretch()
        return wrapper

    def _build_table(self) -> DataTable:
        columns = [
            {"key": "product", "label": "Produto"},
            {"key": "customer", "label": "Cliente"},
            {"key": "amount", "label": "Valor"},
            {"key": "status", "label": "Status"},
            {"key": "sold_at", "label": "Data"},
        ]
        self._table = DataTable(columns=columns, data=[])
        return self._table

    # ------------------------------------------------- signals / lifecycle

    def _setup_connections(self) -> None:
        self._controller.summary_loaded.connect(self._on_summary_loaded)
        self._controller.sales_loaded.connect(self._on_sales_loaded)
        self._status_combo.currentIndexChanged.connect(self._on_filter_changed)

    def on_first_show(self) -> None:
        """Carrega dados na primeira vez que a página é exibida."""
        self._controller.load()

    def on_show(self) -> None:
        self.logger.debug("Dashboard page shown")

    def refresh(self) -> None:
        self._controller.load()

    # ------------------------------------------------------------ handlers

    def _on_summary_loaded(self, summary: DashboardSummary) -> None:
        self._total_sales_card.set_value(str(summary.total_sales))
        self._revenue_card.set_value(_format_currency(summary.total_revenue))
        self._ticket_card.set_value(_format_currency(summary.average_ticket))
        self._customers_card.set_value(str(summary.unique_customers))

    def _on_sales_loaded(self, sales: list[Sale]) -> None:
        self._table.set_data([self._sale_to_row(s) for s in sales])

    def _on_filter_changed(self, _: int) -> None:
        status = self._status_combo.currentData()
        self._controller.filter_by_status(status)

    @staticmethod
    def _sale_to_row(sale: Sale) -> dict[str, str]:
        return {
            "product": sale.product,
            "customer": sale.customer,
            "amount": _format_currency(sale.amount),
            "status": _STATUS_LABELS.get(sale.status, sale.status.value),
            "sold_at": sale.sold_at.strftime("%d/%m/%Y"),
        }
