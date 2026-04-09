# 12 — Event Bus

O `EventBus` (em `src/core/signals.py`, instanciado como `event_bus`) é um **`QObject` global** com sinais Qt que qualquer parte do código pode emitir ou assinar. Serve para comunicação entre componentes que **não se conhecem**.

## Quando usar?

| Cenário | Solução |
|---|---|
| Componente A precisa avisar B, e A tem referência direta a B | Signal direto do A para B — **não use event bus** |
| Componente A precisa avisar "alguém interessado", sem saber quem | **Use event bus** |
| Notificação global (ex.: "erro aconteceu", "tema mudou") | **Use event bus** |
| Página precisa disparar um toast sem se acoplar ao container de toasts | **Use event bus** |

**Regra de ouro:** prefira signals diretos entre widget-pai e widget-filho. Use o event bus para comunicação **horizontal** entre componentes que não têm relação hierárquica.

## Sinais disponíveis

Definidos em `src/core/signals.py`:

### Navegação
- `navigate_to(page_id, params)`
- `navigation_completed(page_id)`
- `navigation_failed(page_id, error)`
- `go_back_requested()`

### Tema
- `theme_changed(theme)`
- `theme_change_requested(theme)`

### Lifecycle da aplicação
- `app_ready()`
- `app_closing()`
- `app_minimized()`
- `app_restored()`

### User
- `user_logged_in(user)`
- `user_logged_out()`
- `user_updated(user)`

### Configurações
- `settings_changed(key, value)`
- `settings_saved()`
- `settings_loaded()`

### Erros
- `error_occurred(error_type, message)`
- `warning_occurred(warning_type, message)`

### UI
- `loading_started(context)`
- `loading_finished(context)`
- `toast_requested(message, type, duration_ms)`
- `dialog_requested(dialog_type, params)`

### Custom
- `custom_event(event_name, data)` — use para seus próprios eventos ad-hoc

## Uso básico

```python
from src.core.signals import event_bus

# Assinar (em qualquer lugar)
event_bus.theme_changed.connect(self._on_theme_changed)

# Emitir
event_bus.emit_theme_change(Theme.DARK)

# Ou manualmente
event_bus.theme_changed.emit(Theme.DARK)
```

### Helpers de conveniência

```python
event_bus.emit_navigation(PageId.HOME)
event_bus.emit_theme_change(Theme.LIGHT)
event_bus.emit_toast("Salvo com sucesso!", "success", 3000)
event_bus.emit_error("ValidationError", "E-mail inválido")
event_bus.emit_custom("my_event", {"key": "value"})
```

## Exemplo: disparar toast de qualquer lugar

```python
# Em uma página:
def _on_save_clicked(self) -> None:
    try:
        self._controller.save()
        self.show_toast("Dados salvos!", "success")  # helper de BasePage
    except Exception as e:
        event_bus.emit_error("SaveError", str(e))
```

Em algum container de toasts no `MainWindow`:

```python
event_bus.toast_requested.connect(self._show_toast)

def _show_toast(self, message: str, toast_type: str, duration: int):
    Toast.show(self, message, toast_type, duration)
```

A página não conhece o container de toasts — só dispara o sinal.

## Custom events

Para eventos específicos da sua aplicação, use `custom_event` em vez de adicionar signals novos ao event bus (isso evita poluir o arquivo central):

```python
# Emitindo
event_bus.emit_custom("client_created", {"id": 42, "name": "Alice"})

# Assinando
event_bus.custom_event.connect(self._on_custom_event)

def _on_custom_event(self, name: str, data: Any) -> None:
    if name == "client_created":
        self._refresh_client_list()
```

Se um custom event vira permanente e é usado em muitos lugares, vale promovê-lo para um signal dedicado no `signals.py`.

## Cuidados

**1. Memory leaks**
Qt automaticamente desconecta signals quando o QObject é destruído. Mas se você conecta um **lambda com closure**, o objeto pode ficar vivo indefinidamente. Prefira métodos:

```python
# ❌ Risco de leak
event_bus.theme_changed.connect(lambda t: self._apply(t))

# ✅ Limpo
event_bus.theme_changed.connect(self._on_theme_changed)
```

**2. Ordem de emissão**
Sinais Qt são entregues **na ordem** em que foram conectados. Se você precisa de garantia de ordem, use prioridades através de camadas (ex.: services escutam primeiro, views depois).

**3. Threads**
Os signals por default são `AutoConnection`, que vira `Direct` se emitido e recebido na mesma thread, ou `Queued` se cross-thread. Se você emite do background, confirme a conexão com `Qt.QueuedConnection` explicitamente.

**4. Evite loops**
Emitir dentro de um slot que escuta o mesmo signal causa loop infinito. Proteja com flags:

```python
def _on_theme_changed(self, theme):
    if self._applying_theme:
        return
    self._applying_theme = True
    try:
        # ... lógica
    finally:
        self._applying_theme = False
```

## Anti-padrões

**Não use o event bus como banco de dados**: event bus é para notificar, não para guardar estado. Use `ConfigService` ou `StorageService` para estado.

**Não abuse do `custom_event`**: se você tem mais de 3-4 custom events, é sinal de que precisam virar signals dedicados.

**Não emita para "simular callback"**: se A chama uma função de B e espera resposta, é uma chamada direta — não enfie event bus no meio só pra "desacoplar".

## Próximo passo

- [Testes](13-testes.md) — como escrever testes com pytest + pytest-qt.
