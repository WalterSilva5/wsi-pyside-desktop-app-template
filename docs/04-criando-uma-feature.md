# 04 — Criando uma Feature (passo a passo)

Este é o guia mais importante do template. Ao final, você terá criado uma feature completa chamada **"Clientes"** com listagem, filtro e controller.

## Resumo dos passos

```
1. Adicionar PageId.CLIENTS em src/core/types.py
2. Criar src/features/clients/
   ├── __init__.py
   ├── page.py
   └── controller.py
3. Registrar em src/features/registry.py
4. Adicionar metadata (label + ícone) em FEATURE_METADATA
```

Pronto. Você não precisa editar `MainWindow`, `Sidebar`, ou qualquer `factory` — o template é projetado para que **uma feature nova seja linear de criar**.

## Passo 1: Adicionar o PageId

Abra `src/core/types.py` e adicione sua feature ao enum:

```python
class PageId(Enum):
    HOME = auto()
    SETTINGS = auto()
    SHOWCASE = auto()
    DASHBOARD = auto()
    RESPONSIVE = auto()
    CLIENTS = auto()  # 👈 NOVO
```

## Passo 2: Criar a estrutura da feature

```bash
mkdir -p src/features/clients
touch src/features/clients/__init__.py
touch src/features/clients/page.py
touch src/features/clients/controller.py
```

### 2.1 — `__init__.py`

```python
"""Feature Clients — listagem e gestão de clientes."""

from src.features.clients.page import ClientsPage
from src.features.clients.controller import ClientsController

__all__ = ["ClientsPage", "ClientsController"]
```

### 2.2 — `controller.py`

```python
"""Controller da feature Clients."""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import Signal

from src.core.base_controller import BaseController


@dataclass
class Client:
    """Um cliente. Feature-specific — mora dentro da feature."""

    id: int
    name: str
    email: str
    active: bool


class ClientsController(BaseController):
    """Controller dos Clients — por enquanto com dados mockados."""

    clients_loaded = Signal(list)  # list[Client]

    def __init__(self) -> None:
        super().__init__()
        self._clients: list[Client] = []

    def load(self) -> None:
        """Carrega clientes (aqui é mockado)."""
        try:
            self.set_loading(True)
            self.log_action("Loading clients")

            self._clients = [
                Client(1, "Alice Souza", "alice@exemplo.com", True),
                Client(2, "Bruno Lima", "bruno@exemplo.com", True),
                Client(3, "Carla Dias", "carla@exemplo.com", False),
            ]
            self.clients_loaded.emit(self._clients)
        except Exception as e:
            self.handle_error(e, "Falha ao carregar clientes")
        finally:
            self.set_loading(False)

    def filter_active(self, active_only: bool) -> None:
        """Filtra apenas ativos (ou todos)."""
        if active_only:
            filtered = [c for c in self._clients if c.active]
        else:
            filtered = self._clients
        self.clients_loaded.emit(filtered)
```

### 2.3 — `page.py`

```python
"""Página Clients."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from src.components.tables.data_table import DataTable
from src.core.base_page import BasePage
from src.features.clients.controller import Client, ClientsController


class ClientsPage(BasePage):
    """Listagem de clientes com filtro de ativos."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._controller = ClientsController()
        self._setup_ui()
        self._setup_connections()

    # --- UI ------------------------------------------------------------

    def _setup_ui(self) -> None:
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("Clientes")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")
        layout.addWidget(title)

        # Filtro
        filter_row = QHBoxLayout()
        self._active_check = QCheckBox("Mostrar apenas ativos")
        self._active_check.setChecked(False)
        filter_row.addWidget(self._active_check)
        filter_row.addStretch()
        layout.addLayout(filter_row)

        # Tabela
        columns = [
            {"key": "id", "label": "ID"},
            {"key": "name", "label": "Nome"},
            {"key": "email", "label": "E-mail"},
            {"key": "active", "label": "Ativo?"},
        ]
        self._table = DataTable(columns=columns, data=[])
        layout.addWidget(self._table, 1)

        self._main_layout.addWidget(content)

    def _setup_connections(self) -> None:
        self._controller.clients_loaded.connect(self._on_clients_loaded)
        self._active_check.stateChanged.connect(self._on_filter_changed)

    # --- Lifecycle -----------------------------------------------------

    def on_first_show(self) -> None:
        """Primeira exibição — carrega dados."""
        self._controller.load()

    def refresh(self) -> None:
        self._controller.load()

    # --- Handlers ------------------------------------------------------

    def _on_clients_loaded(self, clients: list[Client]) -> None:
        rows = [
            {
                "id": str(c.id),
                "name": c.name,
                "email": c.email,
                "active": "Sim" if c.active else "Não",
            }
            for c in clients
        ]
        self._table.set_data(rows)

    def _on_filter_changed(self, state: int) -> None:
        self._controller.filter_active(bool(state))
```

## Passo 3: Registrar no `registry.py`

Abra `src/features/registry.py` e **adicione duas coisas**:

### 3.1 — Adicione à função `create_feature_pages`

```python
def create_feature_pages(parent: QWidget | None = None) -> dict[PageId, QWidget]:
    from src.features.home.page import HomePage
    from src.features.settings.page import SettingsPage
    from src.features.showcase.page import ShowcasePage
    from src.features.dashboard.page import DashboardPage
    from src.features.responsive_demo.page import ResponsivePage
    from src.features.clients.page import ClientsPage  # 👈 NOVO

    return {
        PageId.HOME: HomePage(parent),
        PageId.SETTINGS: SettingsPage(parent),
        PageId.SHOWCASE: ShowcasePage(parent),
        PageId.DASHBOARD: DashboardPage(parent),
        PageId.RESPONSIVE: ResponsivePage(parent),
        PageId.CLIENTS: ClientsPage(parent),  # 👈 NOVO
    }
```

### 3.2 — Adicione à lista `FEATURE_METADATA`

```python
FEATURE_METADATA: list[FeatureMetadata] = [
    FeatureMetadata(PageId.HOME, "Início", "Página inicial", "🏠", is_default=True),
    FeatureMetadata(PageId.DASHBOARD, "Dashboard", "Exemplo com tabela", "📊"),
    FeatureMetadata(PageId.CLIENTS, "Clientes", "Listagem de clientes", "👥"),  # 👈 NOVO
    FeatureMetadata(PageId.SHOWCASE, "Componentes", "Catálogo de componentes", "🧩"),
    FeatureMetadata(PageId.RESPONSIVE, "Layout Responsivo", "Grid 12-col", "📐"),
    FeatureMetadata(PageId.SETTINGS, "Configurações", "Preferências", "⚙️"),
]
```

O sidebar é data-driven: ele pega essa lista e cria os botões automaticamente. **Você não edita o sidebar.**

## Passo 4: Rodar

```bash
uv run python main.py
```

O item "Clientes" aparece no sidebar. Ao clicar, sua página carrega com a tabela preenchida.

## Dica: quando criar models/ e repositories/ dentro da feature?

Só quando realmente precisar. Para mocks simples (o exemplo acima), um `@dataclass` dentro do `controller.py` basta. Crie subpastas só quando:

- **Models**: há lógica de validação não trivial, ou múltiplos modelos relacionados (ex.: `Sale` + `SaleItem` + `Customer`).
- **Repositories**: há mais de uma fonte de dados, cache, ou você quer separar a abstração (ex.: `SalesRepositoryAPI` + `SalesRepositoryJsonFile`).

A feature `dashboard/` mostra a versão com models e repositories — use como referência.

## Dica: lifecycle hooks disponíveis

Dentro de `BasePage` (herdado pela sua `ClientsPage`) você tem:

| Hook | Quando é chamado | O que colocar aí |
|---|---|---|
| `__init__` | Construção | Só chame `_setup_ui()` e `_setup_connections()` |
| `on_first_show` | Primeira vez que a página é exibida | Carregar dados iniciais |
| `on_show` | Toda vez que a página é exibida | Atualizar indicadores rápidos (badge, contador) |
| `on_hide` | Quando sai da página | Salvar rascunhos, cancelar timers |
| `refresh` | Quando o usuário pede refresh | Recarregar dados |
| `on_navigate(params)` | Antes de `on_show`, com os params da navegação | Ler `params.get("id")` etc. |

## Passando parâmetros ao navegar

```python
# Em outra página:
self.navigate_to(PageId.CLIENTS, {"highlight_id": 42})

# Em ClientsPage.on_navigate:
def on_navigate(self, params: dict) -> None:
    super().on_navigate(params)
    highlight = params.get("highlight_id")
    if highlight:
        # ... scrolla até o cliente com id == highlight
        pass
```

## Erros comuns

**1. Esqueci de adicionar PageId**
Erro: `AttributeError: CLIENTS`.
Fix: passo 1.

**2. Esqueci de registrar em `create_feature_pages`**
Erro: `NavigationError: Page CLIENTS not registered`.
Fix: passo 3.1.

**3. Importei algo de `src.features.clients` dentro de `src/core/` ou `src/components/`**
Isso quebra a regra arquitetural. `core` e `components` nunca devem importar `features`. Se você se vê querendo fazer isso, provavelmente está tentando passar algo para um componente genérico — passe como **prop** em vez de importar.

**4. Controller tenta resolver service antes dele ser registrado**
Erro: `KeyError: Service NavigationService not registered`.
Causa: você está instanciando o controller fora do fluxo normal (ex.: em um teste sem `reset_services`).
Fix: use o fixture `reset_services` ou registre o service manualmente antes.

## Próximo passo

Agora que você sabe criar features, veja [Criando um Componente](05-criando-um-componente.md) para saber quando vale a pena extrair algo para `src/components/`.
