# PySide6 Desktop Application Template

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![PySide6](https://img.shields.io/badge/PySide6-6.8%2B-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

Template escalável para aplicações desktop com **PySide6**. Projetado para que criar uma feature nova seja copiar uma pasta e editar três arquivos — nem mais, nem menos.

---

## Destaques

- **Arquitetura feature-based** — cada tela é uma pasta auto-contida em `src/features/`.
- **DI Container** + **Event Bus** para desacoplar camadas sem perder testabilidade.
- **Biblioteca de componentes** reutilizáveis (botões, cards, formulários, tabelas, diálogos, layout responsivo).
- **Grid de 12 colunas** estilo Bootstrap com breakpoints + **FlowLayout** estilo flexbox.
- **Temas light/dark** com QSS e `QPalette`.
- **Dashboard de exemplo** com modelos, repositório, controller e tabela com filtros — pronto para copiar.
- **Documentação completa em português** em [`docs/`](docs/README.md).
- **Type hints** em todo o código + `mypy` configurado.
- **Testes** com pytest + pytest-qt.

---

## Início rápido

### Com `uv` (recomendado)

```bash
git clone https://github.com/walterpsilva/wsi-pyside-desktop-app-template.git
cd wsi-pyside-desktop-app-template

uv sync
uv run python main.py
```

### Com pip

```bash
git clone https://github.com/walterpsilva/wsi-pyside-desktop-app-template.git
cd wsi-pyside-desktop-app-template

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

python main.py
```

Guia completo: [`docs/01-inicio-rapido.md`](docs/01-inicio-rapido.md).

---

## Estrutura

```
src/
├── core/           # Framework: DI container, event bus, types, base classes
├── services/       # Singletons: Config, Logger, Navigation, Theme, Storage
├── components/     # UI reutilizável: buttons, cards, forms, dialogs, layout
├── features/       # ✨ Cada tela em sua pasta (page + controller + models)
│   ├── home/
│   ├── settings/
│   ├── showcase/
│   ├── dashboard/  # Exemplo rico com models e repositório
│   ├── responsive_demo/
│   └── registry.py # Ponto único de registro de features
├── views/          # main_window.py (shell da UI)
├── models/         # BaseModel + Repository abstract
└── utils/          # Decorators, validators, helpers

docs/               # Documentação em português
resources/          # QSS, ícones, imagens, defaults
tests/              # pytest + pytest-qt
```

Detalhes: [`docs/03-estrutura-do-projeto.md`](docs/03-estrutura-do-projeto.md).

---

## Criando uma feature nova

```python
# 1. Adicione o PageId em src/core/types.py
class PageId(Enum):
    ...
    CLIENTS = auto()

# 2. Crie src/features/clients/page.py
from src.core.base_page import BasePage

class ClientsPage(BasePage):
    def _setup_ui(self):
        ...

# 3. Registre em src/features/registry.py
from src.features.clients.page import ClientsPage

def create_feature_pages(parent):
    return {
        ...,
        PageId.CLIENTS: ClientsPage(parent),
    }

FEATURE_METADATA = [
    ...,
    FeatureMetadata(PageId.CLIENTS, "Clientes", "Listagem de clientes", "👥"),
]
```

Pronto — o sidebar se atualiza automaticamente. Passo a passo completo em [`docs/04-criando-uma-feature.md`](docs/04-criando-uma-feature.md).

---

## Documentação

Toda a documentação está em [`docs/`](docs/README.md), em **português brasileiro**:

1. [Início Rápido](docs/01-inicio-rapido.md)
2. [Arquitetura](docs/02-arquitetura.md)
3. [Estrutura do Projeto](docs/03-estrutura-do-projeto.md)
4. [Criando uma Feature](docs/04-criando-uma-feature.md) ⭐
5. [Criando um Componente](docs/05-criando-um-componente.md)
6. [Biblioteca de Componentes](docs/06-biblioteca-de-componentes.md)
7. [Serviços](docs/07-servicos.md)
8. [Navegação](docs/08-navegacao.md)
9. [Tema e Estilos](docs/09-tema-e-estilos.md)
10. [Layout Responsivo](docs/10-layout-responsivo.md)
11. [Modelos e Repositórios](docs/11-modelos-e-repositorios.md)
12. [Event Bus](docs/12-event-bus.md)
13. [Testes](docs/13-testes.md)
14. [Build e Empacotamento](docs/14-build-e-empacotamento.md)

---

## Desenvolvimento

```bash
# Testes
uv run pytest
uv run pytest --cov=src

# Lint e type-check
uv run black src/ tests/
uv run isort src/ tests/
uv run flake8 src/ tests/
uv run mypy src/

# Pre-commit hooks
pre-commit install
pre-commit run --all-files
```

---

## Stack

- **Python 3.10+** (3.12 recomendado)
- **PySide6 ≥ 6.8** — bindings Qt para Python
- **pytest** + **pytest-qt** — testes unitários e de UI
- **black**, **isort**, **flake8**, **mypy** — qualidade de código
- **uv** — gerenciador de pacotes (opcional mas recomendado)

---

## Contribuindo

1. Abra uma issue descrevendo o que você quer mudar.
2. Fork + branch (`git checkout -b feat/minha-feature`).
3. Commit (`git commit -m 'feat: adiciona X'`).
4. Push + Pull Request.

---

## Licença

MIT — veja [LICENSE](LICENSE).

---

## Agradecimentos

- [PySide6](https://doc.qt.io/qtforpython/) pela excelente stack Qt for Python.
- [uv](https://docs.astral.sh/uv/) pelo gerenciador de pacotes ridiculamente rápido.
