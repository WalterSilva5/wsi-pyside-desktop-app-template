"""
Registro central de features.

Este módulo é o **único** lugar onde as features são conectadas ao
`NavigationService`. Quando você criar uma feature nova:

1. Adicione seu `PageId` em `src/core/types.py`.
2. Implemente a pasta `src/features/<nome>/` com `page.py`.
3. Importe e registre aqui na função `register_all_features`.
4. (Opcional) Adicione metadados em `FEATURE_METADATA` para o sidebar
   exibir o label/ícone correto.

Consulte `docs/04-criando-uma-feature.md` para o passo a passo
detalhado.
"""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtWidgets import QWidget

from src.core.types import PageId
from src.services.navigation_service import NavigationService


@dataclass(frozen=True)
class FeatureMetadata:
    """Metadados exibidos em elementos de navegação (sidebar, header)."""

    page_id: PageId
    title: str
    description: str
    icon: str = ""
    is_default: bool = False


FEATURE_METADATA: list[FeatureMetadata] = [
    FeatureMetadata(
        page_id=PageId.HOME,
        title="Início",
        description="Página inicial com atalhos e métricas",
        icon="🏠",
        is_default=True,
    ),
    FeatureMetadata(
        page_id=PageId.DASHBOARD,
        title="Dashboard",
        description="Exemplo com modelos, repositório e tabela",
        icon="📊",
    ),
    FeatureMetadata(
        page_id=PageId.SHOWCASE,
        title="Componentes",
        description="Catálogo de componentes reutilizáveis",
        icon="🧩",
    ),
    FeatureMetadata(
        page_id=PageId.RESPONSIVE,
        title="Layout Responsivo",
        description="Demonstração de Grid 12-col e FlowLayout",
        icon="📐",
    ),
    FeatureMetadata(
        page_id=PageId.SETTINGS,
        title="Configurações",
        description="Preferências e tema da aplicação",
        icon="⚙️",
    ),
]


def create_feature_pages(parent: QWidget | None = None) -> dict[PageId, QWidget]:
    """
    Instancia todas as páginas de feature.

    Feito dentro de uma função para postergar os imports — isso evita
    carregar o código de todas as features quando este módulo é
    importado só para ler `FEATURE_METADATA`.
    """
    # Imports locais (lazy) — uma linha por feature.
    from src.features.home.page import HomePage
    from src.features.settings.page import SettingsPage
    from src.features.showcase.page import ShowcasePage
    from src.features.dashboard.page import DashboardPage
    from src.features.responsive_demo.page import ResponsivePage

    return {
        PageId.HOME: HomePage(parent),
        PageId.SETTINGS: SettingsPage(parent),
        PageId.SHOWCASE: ShowcasePage(parent),
        PageId.DASHBOARD: DashboardPage(parent),
        PageId.RESPONSIVE: ResponsivePage(parent),
    }


def register_all_features(
    nav: NavigationService,
    parent: QWidget | None = None,
) -> dict[PageId, QWidget]:
    """
    Cria e registra todas as features no `NavigationService`.

    Args:
        nav: Serviço de navegação onde as páginas serão registradas.
        parent: Widget pai usado na construção das páginas (normalmente
            o `MainWindow`).

    Returns:
        Mapa `PageId -> QWidget` com todas as páginas já instanciadas,
        útil caso o chamador queira adicioná-las manualmente a um
        `QStackedWidget` sem depender do `NavigationService`.
    """
    pages = create_feature_pages(parent)
    default_ids = {meta.page_id for meta in FEATURE_METADATA if meta.is_default}

    for page_id, page in pages.items():
        nav.register_page(
            page_id,
            page,
            is_default=page_id in default_ids,
        )
    return pages


def get_metadata(page_id: PageId) -> FeatureMetadata | None:
    """Retorna os metadados de uma feature pelo seu `PageId`."""
    for meta in FEATURE_METADATA:
        if meta.page_id == page_id:
            return meta
    return None
