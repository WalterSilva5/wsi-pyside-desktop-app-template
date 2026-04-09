# 13 — Testes

O template usa **pytest** + **pytest-qt** para testes. A estrutura de `tests/` espelha a de `src/`.

## Rodando os testes

```bash
# Todos os testes
uv run pytest

# Com cobertura
uv run pytest --cov=src --cov-report=term-missing

# Um arquivo específico
uv run pytest tests/unit/test_core/test_container.py

# Uma classe ou função específica
uv run pytest tests/unit/test_core/test_container.py::TestContainer::test_singleton_returns_same_instance

# Verbose + para no primeiro erro
uv run pytest -xvs
```

## Estrutura de `tests/`

```
tests/
├── conftest.py                     # Fixtures globais
├── unit/
│   ├── test_core/                  # Testes de core (container, types, exceptions)
│   ├── test_services/              # Testes de services
│   └── test_features/              # Testes de features (pages, controllers, repos)
├── integration/                    # Testes que tocam várias camadas
└── ui/                             # Testes de UI (usando pytest-qt + qtbot)
```

Regra: para cada arquivo em `src/`, crie um arquivo de teste espelhado em `tests/`.

## Fixtures disponíveis (`conftest.py`)

### `qapp`

QApplication compartilhado para a sessão inteira. Use quando precisar criar widgets:

```python
def test_widget_shows_title(qapp):
    from src.components.layout.header import Header
    header = Header(title="Test")
    assert header is not None
```

### `reset_services`

Reseta os singletons dos services entre testes. **Sempre use** se seu teste resolve algum service:

```python
@pytest.mark.usefixtures("reset_services")
class TestMyService:
    def test_foo(self):
        ...
```

### `fresh_container`

Snapshot do DI container — limpa tudo no início do teste e restaura ao final:

```python
def test_register_singleton(fresh_container):
    class S: pass
    fresh_container.register_singleton(S)
    assert fresh_container.resolve(S) is fresh_container.resolve(S)
```

## Testando um repositório (puro, sem Qt)

Modelos e repositórios devem ser testáveis sem `QApplication`:

```python
# tests/unit/test_features/test_sales_repository.py
from src.features.dashboard.models.sale import SaleStatus
from src.features.dashboard.repositories.sales_repository import SalesRepository


def test_total_revenue_uses_paid_only():
    repo = SalesRepository()
    assert repo.total_revenue() > 0

    paid_sum = sum(s.amount for s in repo.get_by_status(SaleStatus.PAID))
    assert repo.total_revenue() == paid_sum
```

Nenhum fixture necessário — o código de domínio é puro Python.

## Testando um controller

Controllers herdam de `BaseController`, que resolve services via container. Use `reset_services` para isolar:

```python
import pytest
from unittest.mock import MagicMock


@pytest.mark.usefixtures("reset_services", "qapp")
class TestDashboardController:
    def test_load_emits_summary(self):
        from src.features.dashboard.controller import DashboardController

        controller = DashboardController()
        received = []
        controller.summary_loaded.connect(lambda s: received.append(s))

        controller.load()

        assert len(received) == 1
        assert received[0].total_sales > 0
```

## Testando uma page (com pytest-qt)

Use `qtbot` (fornecido pelo pytest-qt) para interagir com widgets:

```python
@pytest.mark.usefixtures("reset_services")
class TestHomePage:
    def test_home_page_renders(self, qtbot, qapp):
        from src.features.home.page import HomePage

        page = HomePage()
        qtbot.addWidget(page)

        # Dispara lifecycle como se navegasse
        page.on_navigate({})

        assert page.isVisible() is False  # não foi mostrada ainda
        page.show()
        qtbot.waitExposed(page)
        assert page.isVisible()
```

### Simulando cliques

```python
def test_save_button_calls_controller(qtbot, qapp, mocker):
    page = ClientsPage()
    qtbot.addWidget(page)

    controller_mock = mocker.patch.object(page, "_controller")
    qtbot.mouseClick(page._save_button, Qt.LeftButton)

    controller_mock.save.assert_called_once()
```

## Mocking de services via container

Quando você quer substituir um service por um mock:

```python
def test_something_with_mocked_config(fresh_container):
    from unittest.mock import MagicMock
    from src.services.config_service import ConfigService

    mock_config = MagicMock()
    mock_config.get.return_value = "fake_value"
    fresh_container.register_instance(ConfigService, mock_config)

    # Qualquer código que resolver ConfigService vai receber o mock
    ...
```

## Cobertura

Configuração em `pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = "-v --cov=src --cov-report=term-missing --cov-report=html"

[tool.coverage.run]
source = ["src"]
omit = ["tests/*", "*/__init__.py"]
```

Após rodar `uv run pytest`, abra `htmlcov/index.html` no browser para ver cobertura linha-a-linha.

## Meta pragmática de cobertura

- **Services**: 90%+ — são o coração da aplicação
- **Repositories**: 90%+ — lógica de dados é fácil de testar
- **Controllers**: 70%+ — testar signals emitidos e side-effects
- **Pages**: 40%+ — testes de renderização e interação básica
- **Components**: 60%+ — testes unitários de cada componente
- **Core**: 95%+ — container, event bus, types

Não persiga 100% — alguns caminhos de erro são impossíveis de testar sem mock complicado.

## Anti-padrões

**Não teste implementação, teste comportamento.** Em vez de verificar que `_private_method` foi chamado, verifique que o signal correto foi emitido.

**Não mocke tudo.** Se você tem um controller pequeno que usa um repository pequeno, teste os dois juntos — é mais valioso e mais legível.

**Não use `sleep()` em testes.** Use `qtbot.waitUntil(lambda: ...)` ou `qtbot.waitSignal(signal)`.

## Próximo passo

- [Build e Empacotamento](14-build-e-empacotamento.md) — gerar executável com PyInstaller.
