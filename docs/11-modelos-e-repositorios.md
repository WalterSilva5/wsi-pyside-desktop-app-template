# 11 — Modelos e Repositórios

Modelos representam **dados de domínio** (ex.: `Sale`, `Client`, `Product`). Repositórios abstraem **como você lê e grava** esses modelos (JSON, banco, API HTTP, ...).

## `BaseModel` (`src/models/base.py`)

Todo modelo deve herdar de `BaseModel`, um `@dataclass` que já vem com:

- `id: str` — UUID gerado automaticamente
- `created_at: datetime`
- `updated_at: datetime`
- `validate()` — hook para validações (raise `ValueError`)
- `to_dict()` / `from_dict()` — serialização
- `update(**kwargs)` — atualiza campos e bumpa `updated_at`
- `copy(**changes)` — cópia com id novo e timestamps reset
- `__eq__` / `__hash__` — baseados no `id`

### Exemplo

```python
from dataclasses import dataclass

from src.models.base import BaseModel


@dataclass
class Client(BaseModel):
    name: str = ""
    email: str = ""
    active: bool = True

    def validate(self) -> None:
        if not self.name:
            raise ValueError("Client.name é obrigatório")
        if "@" not in self.email:
            raise ValueError("Client.email inválido")
```

Uso:

```python
alice = Client(name="Alice", email="alice@example.com")
print(alice.id)           # UUID gerado
print(alice.to_dict())    # dict com todos os campos

# Atualização
alice.update(name="Alice Souza")  # updated_at vira now()

# Cópia (novo id, timestamps zerados)
alice_copy = alice.copy(email="alice.souza@example.com")
```

## Onde mora o modelo?

| Caso | Localização |
|---|---|
| Modelo **específico** de uma feature (ex.: `Sale` no Dashboard) | `src/features/<feature>/models/<nome>.py` |
| Modelo **compartilhado** entre várias features | Só crie compartilhado em último caso. Prefira duplicar. |

**Filosofia:** acoplar um modelo a uma feature é melhor que ter um pacote `src/models/` gigante que ninguém sabe onde usar. Se dois modelos de features diferentes começam a divergir, não há dívida; se estão acoplados a um modelo comum, qualquer mudança quebra as duas features.

## Repository Pattern

O `BaseRepository` (`src/models/repositories/base.py`) define a API abstrata de CRUD:

```python
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class BaseRepository(Generic[T], ABC):
    @abstractmethod
    def get(self, id: str) -> T | None: ...

    @abstractmethod
    def get_all(self) -> list[T]: ...

    @abstractmethod
    def add(self, entity: T) -> T: ...

    @abstractmethod
    def update(self, entity: T) -> T: ...

    @abstractmethod
    def delete(self, id: str) -> bool: ...
```

E há uma implementação pronta baseada em JSON: `JsonFileRepository`.

### Usando `JsonFileRepository`

```python
from pathlib import Path

from src.models.repositories.base import JsonFileRepository

from src.features.clients.models.client import Client


class ClientRepository(JsonFileRepository[Client]):
    def __init__(self) -> None:
        super().__init__(
            file_path=Path.home() / ".myapp" / "clients.json",
            model_cls=Client,
        )


# Uso
repo = ClientRepository()
alice = Client(name="Alice", email="alice@ex.com")
repo.add(alice)

todos = repo.get_all()
achado = repo.get(alice.id)
repo.delete(alice.id)
```

### Criando um repositório custom

Para um repositório com regras específicas (ex.: filtros, agregados), herde de `JsonFileRepository` ou implemente `BaseRepository` direto:

```python
class SalesRepository:
    """Repositório de vendas com métricas agregadas."""

    def __init__(self) -> None:
        self._sales: list[Sale] = self._load_seed()

    def get_all(self) -> list[Sale]:
        return sorted(self._sales, key=lambda s: s.sold_at, reverse=True)

    def get_by_status(self, status: SaleStatus) -> list[Sale]:
        return [s for s in self._sales if s.status == status]

    def total_revenue(self, statuses=None) -> float:
        allowed = set(statuses) if statuses else {SaleStatus.PAID}
        return sum(s.amount for s in self._sales if s.status in allowed)
```

Veja `src/features/dashboard/repositories/sales_repository.py` para o exemplo completo.

## Quando criar um repositório?

| Situação | Decisão |
|---|---|
| Dados mockados no código | **Não precisa** — use um `@dataclass` dentro do controller |
| Leitura/escrita em JSON/SQLite/arquivo | **Sim** — crie um repositório |
| Múltiplas fontes (cache + API) | **Sim** — repositório abstrai a complexidade |
| Cálculos agregados sobre uma coleção | **Sim** — os métodos ficam no repositório, não no controller |

## Integração com o controller

O controller **resolve** ou **instancia** o repositório e faz a ponte com a page:

```python
class DashboardController(BaseController):
    summary_loaded = Signal(object)

    def __init__(self) -> None:
        super().__init__()
        self._repository = SalesRepository()

    def load(self) -> None:
        summary = self._build_summary()
        self.summary_loaded.emit(summary)

    def _build_summary(self) -> DashboardSummary:
        total = self._repository.count()
        revenue = self._repository.total_revenue()
        return DashboardSummary(total_sales=total, total_revenue=revenue, ...)
```

O controller **nunca** vaza objetos Qt para o repository. O repository é puro Python — testável sem `QApplication`.

## Testando um repositório

```python
# tests/unit/test_features/test_sales_repository.py
from src.features.dashboard.models.sale import SaleStatus
from src.features.dashboard.repositories.sales_repository import SalesRepository


def test_total_revenue_uses_paid_only():
    repo = SalesRepository()
    total = repo.total_revenue()
    paid_sum = sum(s.amount for s in repo.get_by_status(SaleStatus.PAID))
    assert total == paid_sum
```

Sem fixtures de Qt, sem mocks complicados — exatamente como deve ser testar código de domínio.

## Próximo passo

- [Event Bus](12-event-bus.md) — comunicação entre componentes desacoplados.
