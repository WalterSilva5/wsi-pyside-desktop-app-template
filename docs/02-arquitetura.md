# 02 — Arquitetura

Este documento explica a arquitetura do template, os padrões usados e **por quê** cada escolha foi feita.

## Visão geral em uma imagem

```
┌──────────────────────────────────────────────────────────────┐
│                          main.py                            │
│                             │                                │
│                             ▼                                │
│                src/core/application.py                      │
│          (QApplication + registra services +                │
│                 cria MainWindow)                             │
│                             │                                │
│                             ▼                                │
│                   src/views/main_window.py                   │
│     (shell: Sidebar + Header + QStackedWidget)               │
│                             │                                │
│                             ▼                                │
│                 src/features/registry.py                     │
│         (cria cada página e registra no                      │
│                 NavigationService)                           │
│                             │                                │
│    ┌────────┬──────────┬────┴─────┬───────────┬───────────┐  │
│    ▼        ▼          ▼          ▼           ▼           ▼  │
│  home/   settings/  showcase/  dashboard/  responsive_demo/  │
│                                                              │
│       Cada feature usa:                                      │
│         - src/components/  (UI reutilizável)                 │
│         - src/services/    (Config, Theme, Nav, ...)         │
│         - src/models/      (BaseModel, repositories base)    │
│         - src/utils/       (decorators, validators, helpers) │
└──────────────────────────────────────────────────────────────┘
```

## As camadas

### 1. `src/core/` — Framework

Infraestrutura que tudo depende, mas que **não depende de nada mais** do projeto.

| Arquivo | Função |
|---|---|
| `application.py` | Classe `Application` — inicializa `QApplication`, registra services, cria `MainWindow`, roda o event loop |
| `container.py` | DI Container (`register_singleton`, `register_transient`, `register_instance`, `resolve`) |
| `signals.py` | `EventBus` global (sinais Qt para comunicação entre componentes desacoplados) |
| `types.py` | Enums: `PageId`, `Theme`, `ToastType`, `DialogResult`, etc. |
| `exceptions.py` | Hierarquia de exceptions customizadas (`AppException`, `ConfigurationError`, `NavigationError`, ...) |
| `base_page.py` | Classe `BasePage` da qual toda página herda |
| `base_controller.py` | Classe `BaseController` da qual todo controller herda |

**Regra de ouro:** `src/core/` **NUNCA** importa de `src/features/` ou `src/components/`. Se você se vê precisando disso, é sinal de que a lógica está no lugar errado.

### 2. `src/services/` — Serviços globais

Singletons resolvidos via DI container. Estado/lógica que vive durante toda a execução da aplicação.

| Serviço | Responsabilidade |
|---|---|
| `ConfigService` | Configurações persistidas em JSON (`~/AppData/Local/...`), dot notation (`config.get("theme.current")`) |
| `LoggerService` | Logs em console + arquivo com rotação (5MB × 5 arquivos) |
| `NavigationService` | Rotas entre páginas, histórico, guards, parâmetros |
| `ThemeService` | Aplicar QSS light/dark, atualizar `QPalette`, persistir preferência |
| `StorageService` | Storage key-value em JSON, suporte a namespaces |

**Regra:** sempre resolva via container:

```python
from src.core.container import container
from src.services.config_service import ConfigService

config = container.resolve(ConfigService)
theme = config.get("theme.current", "light")
```

Nunca faça `ConfigService()` direto — você quebra o contrato de singleton e pode acabar com dois estados diferentes.

### 3. `src/components/` — UI reutilizável

Componentes puros de interface, organizados por categoria: `buttons/`, `cards/`, `dialogs/`, `feedback/`, `forms/`, `icons/`, `layout/`, `tables/`.

**Regra importantíssima:** componentes **não conhecem features**. Isto é, `src/components/layout/sidebar.py` não pode importar nada de `src/features/`. A sidebar recebe a lista de itens via `set_items(...)` chamada pelo `MainWindow`.

Todo componente herda de `BaseComponent` (`src/components/base.py`), que oferece:
- Sistema de props (`get_prop`, `set_prop`)
- Hook `_setup_ui()` para construir a UI
- Hook `_apply_styles()` para aplicar estilos

Veja [Biblioteca de Componentes](06-biblioteca-de-componentes.md) para o catálogo completo.

### 4. `src/features/` — Features

Cada feature é uma **pasta auto-contida**:

```
src/features/minha_feature/
├── __init__.py          # re-exporta Page e Controller
├── page.py              # View (herda BasePage)
├── controller.py        # Lógica de negócio (herda BaseController)
├── models/              # (opcional) modelos específicos
│   └── entidade.py
└── repositories/        # (opcional) repositórios específicos
    └── entidade_repository.py
```

Esta é a unidade de reuso. Se você quiser copiar a feature Dashboard para outro projeto, basta copiar a pasta `src/features/dashboard/` e adicionar ao `src/features/registry.py` do novo projeto.

Veja [Criando uma Feature](04-criando-uma-feature.md) para o passo a passo.

### 5. `src/models/` — Modelos compartilhados

Contém apenas `BaseModel` e as implementações base de `Repository`. Modelos específicos de uma feature **vivem dentro da feature**, não aqui.

### 6. `src/views/` — Shell da UI

Apenas `main_window.py` — o shell que hospeda sidebar, header e stack de páginas. Páginas das features **não** ficam aqui.

### 7. `src/utils/` — Utilitários

Funções puras e decorators reutilizáveis: `decorators.py` (`@singleton`, `@debounce`, `@throttle`), `validators.py`, `helpers.py`.

## Padrões de design usados

| Padrão | Onde está | Por quê |
|---|---|---|
| **Dependency Injection (Container)** | `src/core/container.py` | Acoplamento fraco entre camadas, testabilidade |
| **Observer (Event Bus)** | `src/core/signals.py` | Comunicação pub/sub sem acoplamento direto |
| **Repository** | `src/models/repositories/base.py` | Abstrai acesso a dados — troca backend sem tocar nas features |
| **Singleton (via BaseService)** | `src/services/base.py` | Services têm uma única instância por processo |
| **MVC** | Pages (V) + Controllers (C) + Models | Separação clássica de responsabilidades |
| **Factory** (implícito) | `src/features/registry.py` | Centraliza criação de páginas |

## Fluxo de uma interação típica

Exemplo: usuário clica em "Filtrar por status" no Dashboard.

```
1. QComboBox emite currentIndexChanged
      │
      ▼
2. DashboardPage._on_filter_changed(index)
      │ (reads status from currentData())
      ▼
3. DashboardController.filter_by_status(status)
      │
      ▼
4. SalesRepository.get_by_status(status)
      │ (returns list[Sale])
      ▼
5. DashboardController.sales_loaded.emit(sales)
      │
      ▼
6. DashboardPage._on_sales_loaded(sales)
      │ (converte para lista de dicts)
      ▼
7. DataTable.set_data(rows)
      │
      ▼
8. QTableWidget atualiza exibição
```

Note que **nenhum widget Qt fala diretamente com outro widget Qt** através de features — sempre passa por Signal + Slot. Isso mantém as camadas desacopladas.

## Lifecycle de uma página

Quando você navega para uma página:

```
nav.navigate_to(PageId.HOME, {"param": 1})
      │
      ▼
NavigationService:
  - executa guards (se houver)
  - registra entry no history
  - chama page.on_navigate(params)  ────────────┐
  - QStackedWidget.setCurrentWidget(page)       │
                                                │
                                                ▼
BasePage.on_navigate(params):
  - grava self._params
  - se primeira vez, chama self.on_first_show()
  - sempre chama self.on_show()
  - emite page_shown signal
```

Você sobrescreve `on_first_show()` para carregar dados uma única vez e `on_show()` para refrescar a cada visita. Ao sair da página, `on_hide()` é chamado.

## Por que esta arquitetura?

**Feature-based ao invés de layered MVC clássico**: em layered MVC, criar uma tela nova significa editar 3 arquivos em 3 diretórios diferentes (`views/`, `controllers/`, `models/`). Em feature-based, você edita 1 pasta e 1 arquivo de registry. Escala melhor para equipes e features independentes.

**DI container explícito ao invés de singletons globais**: singletons globais fazem seus testes chorar. Com DI container, você pode registrar mocks facilmente no `fresh_container` fixture.

**Event bus ao invés de callbacks diretos**: se a `SettingsPage` precisa notificar a `Header` sobre mudança de tema, ela poderia manter referência à header. Mas isso acopla as duas. Com event bus, ambas assinam `theme_change_requested` sem se conhecerem.
