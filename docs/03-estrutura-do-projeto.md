# 03 — Estrutura do Projeto

Este documento é um mapa comentado da estrutura de pastas. Se você quer saber **onde colocar algo**, comece por aqui.

## Árvore completa

```
wsi-pyside-desktop-app-template/
│
├── main.py                          # Entry point — apenas chama Application().run()
├── pyproject.toml                   # Config do projeto (dependências, black, mypy, pytest)
├── requirements.txt                 # Mantido para compat com `pip install -r`
├── uv.lock                          # Lock file do uv (não editar à mão)
├── .python-version                  # Python 3.12
├── README.md                        # README do projeto (aponta para docs/)
├── LICENSE                          # Licença
│
├── src/
│   │
│   ├── __init__.py
│   ├── app.py                       # Wrapper do entry point
│   │
│   ├── core/                        # ⚙️ FRAMEWORK — infraestrutura base
│   │   ├── application.py           # Classe Application (inicialização)
│   │   ├── container.py             # DI Container (Singleton/Transient/Instance/Factory)
│   │   ├── signals.py               # EventBus global (Observer pattern)
│   │   ├── types.py                 # Enums: PageId, Theme, ToastType, ...
│   │   ├── exceptions.py            # AppException e subclasses
│   │   ├── base_page.py             # BasePage (herda QWidget) — lifecycle hooks
│   │   └── base_controller.py       # BaseController (herda QObject) — services + logging
│   │
│   ├── services/                    # 🔧 SERVIÇOS — singletons do container
│   │   ├── base.py                  # BaseService (QObject + ABC + metaclass)
│   │   ├── config_service.py        # JSON persist com dot notation
│   │   ├── logger_service.py        # Rotating file logs
│   │   ├── navigation_service.py    # Rotas + history + guards
│   │   ├── theme_service.py         # Light/Dark + QSS + QPalette
│   │   └── storage_service.py       # Key-value storage com namespaces
│   │
│   ├── components/                  # 🧩 BIBLIOTECA DE COMPONENTES — UI reutilizável
│   │   ├── base.py                  # BaseComponent (props, lifecycle)
│   │   │
│   │   ├── buttons/                 # PrimaryButton, SecondaryButton, IconButton, ToggleButton
│   │   ├── cards/                   # BasicCard, InfoCard, ActionCard
│   │   ├── dialogs/                 # BaseDialog, ConfirmDialog, AlertDialog, FormDialog
│   │   ├── feedback/                # Badge, ProgressBar, Spinner, Toast, Tooltip
│   │   ├── forms/                   # TextInput, SelectInput, Checkbox, RadioGroup, FormField
│   │   ├── icons/                   # Icon wrapper
│   │   ├── tables/                  # DataTable, ListView, TreeView
│   │   └── layout/                  # Header, Sidebar, Footer, ContentArea,
│   │                                # Grid (12 col), FlowLayout
│   │
│   ├── features/                    # ✨ FEATURES — uma pasta por tela
│   │   ├── registry.py              # 📝 ÚNICO lugar onde features são registradas
│   │   │
│   │   ├── home/                    # Feature: página inicial
│   │   │   ├── page.py
│   │   │   └── controller.py
│   │   │
│   │   ├── settings/                # Feature: configurações
│   │   │   ├── page.py
│   │   │   └── controller.py
│   │   │
│   │   ├── showcase/                # Feature: catálogo de componentes
│   │   │   ├── page.py
│   │   │   ├── controller.py
│   │   │   └── sections/            # Uma seção por categoria de componente
│   │   │
│   │   ├── dashboard/               # Feature rica — com models e repositórios
│   │   │   ├── page.py
│   │   │   ├── controller.py
│   │   │   ├── models/
│   │   │   │   └── sale.py
│   │   │   └── repositories/
│   │   │       └── sales_repository.py
│   │   │
│   │   └── responsive_demo/         # Feature: demo do sistema de grid responsivo
│   │       └── page.py
│   │
│   ├── views/                       # 🏠 Shell — só o que é da janela principal
│   │   └── main_window.py           # MainWindow (sidebar + header + stack)
│   │
│   ├── models/                      # 📦 Modelos compartilhados (apenas base)
│   │   ├── base.py                  # BaseModel (dataclass + validate + serialize)
│   │   └── repositories/
│   │       └── base.py              # BaseRepository abstract + JsonFileRepository
│   │
│   └── utils/                       # 🔩 Utilidades
│       ├── decorators.py            # @singleton, @debounce, @throttle
│       ├── validators.py            # Validadores (email, required, ...)
│       └── helpers.py               # Funções auxiliares
│
├── resources/                       # 📁 Recursos estáticos
│   ├── config/
│   │   └── default_settings.json    # Configurações iniciais
│   ├── styles/
│   │   ├── base.qss                 # Estilos comuns
│   │   ├── light.qss                # Override do tema claro
│   │   └── dark.qss                 # Override do tema escuro
│   ├── icons/                       # Ícones (.png, .svg)
│   └── images/                      # Imagens
│
├── tests/                           # 🧪 Testes (pytest + pytest-qt)
│   ├── conftest.py                  # Fixtures globais (qapp, reset_services, fresh_container)
│   ├── unit/
│   │   ├── test_core/
│   │   ├── test_services/
│   │   └── test_features/
│   ├── integration/
│   └── ui/
│
├── docs/                            # 📚 Documentação (pt-br)
│   ├── README.md                    # Índice principal
│   └── 01..14-*.md                  # Guides
│
└── .github/
    └── workflows/
        └── ci.yml                   # Pipeline GitHub Actions
```

## Onde colocar o quê?

| Eu quero... | Coloque em... |
|---|---|
| Adicionar uma **tela nova** | `src/features/<nome>/page.py` + `controller.py` |
| Criar um **componente reutilizável** | `src/components/<categoria>/<nome>.py` |
| Criar um **modelo de dados usado só por uma feature** | `src/features/<feature>/models/<nome>.py` |
| Criar um **modelo compartilhado entre features** | Não crie compartilhado. Duplique. Se realmente for genérico, `src/models/` (mas prefira duplicar) |
| Criar um **service novo** (global, singleton) | `src/services/<nome>_service.py` herdando `BaseService` |
| Adicionar um **ícone** | `resources/icons/` |
| Adicionar estilos de um componente | Dentro do próprio componente (`_apply_styles()`) ou em `resources/styles/base.qss` |
| Criar um **teste** | Espelhe a estrutura de `src/`: `tests/unit/test_features/test_minha_feature.py` |

## Pastas que você normalmente **não** deveria mexer

- `src/core/` — só se for adicionar algo fundamentalmente novo ao framework (raro)
- `src/models/base.py` — extender por herança, não modificar
- `src/models/repositories/base.py` — idem

## Arquivos especiais

- **`src/features/registry.py`** — único lugar onde as features são conectadas. Ao criar uma feature, você sempre passa por aqui.
- **`src/core/types.py`** — enum `PageId` precisa de uma entrada para cada feature.
- **`pyproject.toml`** — dependências novas entram aqui (via `uv add <pkg>`).
- **`resources/config/default_settings.json`** — valores padrão das configs.

## O que foi **removido** do template original

- `src/controllers/` (pasta) — controllers agora ficam dentro de cada feature
- `src/factories/` — simplificado por `src/features/registry.py`
- `src/views/pages/` — pages agora ficam em `src/features/<name>/page.py`
- `src/views/home.py`, `src/views/settings.py` — legado, substituídos pelas features
- `src/models/user.py`, `src/models/settings.py` — modelos específicos devem viver dentro da feature que os usa

Se você precisa de algum desses, veja no git history o conteúdo ou abra uma issue.
