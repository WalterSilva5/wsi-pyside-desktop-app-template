# 08 — Navegação

O `NavigationService` gerencia a troca de páginas, o histórico e os parâmetros.

## Conceitos

- **PageId** — enum em `src/core/types.py` que identifica cada página de forma type-safe.
- **Page** — qualquer `QWidget` (normalmente `BasePage`) registrado no `NavigationService`.
- **Stack widget** — `QStackedWidget` do `MainWindow` que mostra uma página por vez.
- **History** — lista de `NavigationEntry(page_id, params)` com índice do atual.
- **Guard** — função que decide se uma navegação pode prosseguir.
- **Params** — dict opcional passado ao navegar.

## Uso básico

```python
from src.core.container import container
from src.core.types import PageId
from src.services.navigation_service import NavigationService

nav = container.resolve(NavigationService)

# Navegar
nav.navigate_to(PageId.SETTINGS)

# Com parâmetros
nav.navigate_to(PageId.DASHBOARD, {"highlight_id": 42})

# Voltar / avançar (como browser)
if nav.can_go_back():
    nav.go_back()

if nav.can_go_forward():
    nav.go_forward()

# Ir para home (página marcada como default em FEATURE_METADATA)
nav.go_home()
```

## Helpers em `BasePage`

Dentro de uma página que herda de `BasePage`, use os atalhos:

```python
class MyPage(BasePage):
    def _on_save_clicked(self) -> None:
        self.navigate_to(PageId.DASHBOARD, {"refresh": True})

    def _on_cancel_clicked(self) -> None:
        self.go_back()
```

`self.navigate_to` e `self.go_back` delegam para o `NavigationService` — açúcar sintático para ficar mais legível.

## Lifecycle hooks de uma página

Quando você navega para uma página, o seguinte acontece:

```
1. NavigationService.navigate_to(PageId.X, params)
      │
      ▼
2. Guards rodam (pode bloquear)
      │
      ▼
3. Entry adicionada ao history
      │
      ▼
4. page.on_navigate(params)  ────────┐
      │                               │
      ▼                               │
5. QStackedWidget.setCurrentWidget    │
      │                               │
      ▼                               │
6. Signals emitidos                   │
                                      │
                                      ▼
                            BasePage.on_navigate:
                              - salva params
                              - se primeira vez: on_first_show()
                              - sempre: on_show()
                              - emite page_shown
```

E ao sair da página: `on_hide()`.

**Sobrescreva esses hooks na sua página:**

```python
class MyPage(BasePage):
    def on_first_show(self) -> None:
        """Chamado só na primeira exibição — carregue dados aqui."""
        self._controller.load()

    def on_show(self) -> None:
        """Chamado a cada exibição — atualize indicadores rápidos."""
        self.logger.debug("MyPage shown")

    def on_hide(self) -> None:
        """Chamado quando sai da página — salve rascunhos, pare timers."""
        super().on_hide()
        self._autosave()

    def on_navigate(self, params: dict) -> None:
        """Chamado antes de on_show — leia params aqui."""
        super().on_navigate(params)
        highlight = params.get("highlight_id")
        if highlight:
            self._scroll_to(highlight)
```

## Passando parâmetros

Os parâmetros são um dict simples. Serialize qualquer coisa que precisar:

```python
# Na origem
self.navigate_to(PageId.EDIT_CLIENT, {
    "client_id": 42,
    "tab": "billing",
    "preload": {"name": "Alice"},
})

# No destino
def on_navigate(self, params: dict) -> None:
    super().on_navigate(params)
    self._client_id = params.get("client_id")
    self._active_tab = params.get("tab", "general")
    self._preload_form(params.get("preload", {}))
```

## Guards (proteção de navegação)

Use guards para impedir que o usuário vá a uma página sem permissão:

```python
from src.core.types import PageId

def auth_guard(page_id: PageId, params: dict) -> bool:
    """Retorna True para permitir, False para bloquear."""
    protected = {PageId.DASHBOARD, PageId.SETTINGS}
    if page_id in protected and not is_user_authenticated():
        # Opcional: redirecionar para login
        container.resolve(NavigationService).navigate_to(PageId.LOGIN)
        return False
    return True

nav = container.resolve(NavigationService)
nav.add_guard(auth_guard)
```

Guards são chamados **na ordem em que foram registrados**. Se qualquer guard retorna `False`, a navegação é abortada.

## Mudando a página default

A página padrão (para onde o app vai após inicialização e o que `go_home()` faz) é definida em `src/features/registry.py` via `is_default=True`:

```python
FEATURE_METADATA: list[FeatureMetadata] = [
    FeatureMetadata(PageId.HOME, "Início", ..., is_default=True),  # 👈
    ...
]
```

## Signals úteis do `NavigationService`

```python
nav.page_changed.connect(lambda page_id, params: print(f"Foi pra {page_id}"))
nav.navigation_failed.connect(lambda page_id, error: print(f"Falhou: {error}"))
nav.can_go_back_changed.connect(lambda can: self._back_btn.setEnabled(can))
```

## Perguntas frequentes

**Q: Como faço uma navegação "modal" (abrir uma tela por cima)?**
A: Use um `QDialog` (ex.: `FormDialog`), não o `NavigationService`. Navegação serve para páginas de nível superior.

**Q: Posso ter duas instâncias da mesma página?**
A: O `NavigationService` registra uma página por `PageId`. Se você precisa de múltiplas, crie vários `PageId`s ou aceite um parâmetro `id` e reaproveite a mesma instância.

**Q: O history cresce infinitamente?**
A: Sim — a implementação atual não tem limite. Se isso for um problema, adicione um `maxlen` na lista `_history`.

**Q: Como implemento uma rota com parâmetros dinâmicos tipo "/clients/:id"?**
A: Passe `{"client_id": 42}` no segundo argumento. PageIds são estáticos; o parâmetro fica no dict.

## Próximo passo

- [Tema e Estilos](09-tema-e-estilos.md) — como o `ThemeService` funciona.
