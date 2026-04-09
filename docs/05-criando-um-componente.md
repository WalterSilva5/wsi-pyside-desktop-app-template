# 05 — Criando um Componente Reutilizável

Componentes vivem em `src/components/` e são **agnósticos de feature**: um componente bem-feito pode ser usado em qualquer tela sem modificação.

## Quando criar um componente?

| Situação | Decisão |
|---|---|
| Uso em uma única feature | **Não** crie componente — deixe inline no `page.py` |
| Uso em duas ou mais features | **Talvez** — se for simples, ok deixar inline e duplicar |
| Uso em 3+ features ou conceito genérico | **Sim** — extraia para `src/components/` |
| Widget Qt composto que você precisa customizar estilizando | Sim, mesmo que use em uma só feature |

**Regra prática:** duplique o código duas vezes antes de extrair. "Three strikes and refactor."

## Estrutura mínima

Todo componente herda de `BaseComponent` (`src/components/base.py:15`). O mínimo é:

```python
"""MyComponent — descrição curta."""

from __future__ import annotations

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from src.components.base import BaseComponent


class MyComponent(BaseComponent):
    """
    Descrição do que o componente faz.

    Props:
        text: Texto exibido.
        color: Cor de fundo.
    """

    def __init__(
        self,
        text: str = "",
        parent: QWidget | None = None,
        **kwargs,
    ) -> None:
        super().__init__(parent, text=text, color="#0078D4", **kwargs)

    def _setup_ui(self) -> None:
        """Chamado automaticamente pelo BaseComponent.__init__."""
        layout = QVBoxLayout(self)
        self._label = QLabel(self.get_prop("text", ""))
        layout.addWidget(self._label)

    def _apply_styles(self) -> None:
        color = self.get_prop("color", "#0078D4")
        self.setStyleSheet(f"background: {color};")

    def set_text(self, text: str) -> None:
        """API pública para atualizar o texto."""
        self.set_prop("text", text)
        self._label.setText(text)
```

## API do `BaseComponent`

| Método | O que faz |
|---|---|
| `get_prop(key, default)` | Lê uma prop |
| `set_prop(key, value)` | Escreve uma prop e dispara `_on_prop_changed` |
| `set_props(**kwargs)` | Atualiza várias props de uma vez |
| `_setup_ui()` | **Sobrescreva** — cria widgets |
| `_setup_connections()` | **Sobrescreva** (opcional) — conecta sinais |
| `_apply_styles()` | **Sobrescreva** (opcional) — QSS |
| `_on_prop_changed(key, old, new)` | **Sobrescreva** (opcional) — reage a mudanças |
| `_update_ui()` | Default: chamado por `_on_prop_changed` |

## Onde colocar o arquivo?

Escolha a subpasta que melhor descreve a categoria:

| Categoria | Exemplos |
|---|---|
| `buttons/` | PrimaryButton, ToggleButton |
| `cards/` | InfoCard, BasicCard |
| `dialogs/` | ConfirmDialog, FormDialog |
| `feedback/` | Toast, Spinner, ProgressBar |
| `forms/` | TextInput, Checkbox |
| `icons/` | Icon wrapper |
| `layout/` | Header, Sidebar, Grid, FlowLayout |
| `tables/` | DataTable, ListView |

Se não se encaixa em nenhuma, crie uma nova subpasta em `src/components/` — mas pense se você realmente precisa.

## Registrando no `__init__.py`

Após criar o arquivo, edite o `__init__.py` da subpasta para re-exportar:

```python
# src/components/cards/__init__.py
from src.components.cards.basic_card import BasicCard
from src.components.cards.info_card import InfoCard
from src.components.cards.action_card import ActionCard
from src.components.cards.my_component import MyComponent  # 👈 NOVO

__all__ = ["BasicCard", "InfoCard", "ActionCard", "MyComponent"]
```

Isso permite importar via `from src.components.cards import MyComponent`.

## Boas práticas

### ✅ Faça

- **Props imutáveis via `**kwargs`**: o componente recebe configuração no `__init__` e pode mudar via `set_prop`.
- **API pública de alto nível**: expor `set_text()`, `set_color()` em vez de forçar o usuário a usar `set_prop`.
- **Signals Qt**: use signals para notificar eventos (`clicked`, `value_changed`). Nunca use callbacks diretos.
- **QSS escopado**: prefira estilizar via `self.setStyleSheet(...)` no próprio widget. Evite modificar estilos globais.
- **Document props**: o docstring do componente deve listar todas as props aceitas.

### ❌ Não faça

- **Importar de `src/features/`**: componentes não conhecem features. Nunca.
- **Importar services diretamente**: se o componente precisa de config, receba como prop. Se precisa disparar navegação, emita um signal e deixe a página tratar.
- **Estado global**: componentes não devem guardar estado global. Use props e signals.
- **Lógica de negócio**: se há "regras", elas vivem no controller, não no componente.

### Exceção: `Sidebar` e `Header`

Esses dois componentes precisam falar com o `NavigationService` e `ThemeService` respectivamente. É aceitável porque eles são **shell components**, sabidamente únicos. Ainda assim, a comunicação deles é através do event bus ou resolve do container — nunca importam features.

## Exemplo completo: `InfoCard`

Veja `src/components/cards/info_card.py` para um exemplo real, pequeno e completo. Ele:

1. Recebe `title`, `value`, `color` como props.
2. Constrói dois `QLabel` com estilos inline.
3. Expõe `set_value()` para atualização dinâmica.

Reutilizado pela feature Dashboard (`src/features/dashboard/page.py`) para os 4 cards de métrica.

## Dica: estilizando com tema

Se seu componente precisa reagir ao tema (claro/escuro), conecte ao `ThemeService`:

```python
def _setup_connections(self) -> None:
    from src.core.container import container
    from src.services.theme_service import ThemeService

    theme_service = container.resolve(ThemeService)
    theme_service.theme_changed.connect(self._on_theme_changed)

def _on_theme_changed(self, theme) -> None:
    # Reaplica estilos conforme o tema
    self._apply_styles()
```

Mas antes de fazer isso, veja se o QSS global em `resources/styles/{light,dark}.qss` resolve por você via classes CSS (`self.setProperty("class", "my-component")`).

## Próximo passo

Veja [Biblioteca de Componentes](06-biblioteca-de-componentes.md) para o catálogo dos componentes já incluídos no template.
