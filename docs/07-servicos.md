# 07 — Serviços

Serviços são **singletons globais** resolvidos via DI container. Eles encapsulam estado e lógica que precisa ser compartilhada por várias features.

## Resolvendo um serviço

**Sempre use o container:**

```python
from src.core.container import container
from src.services.config_service import ConfigService

config = container.resolve(ConfigService)
```

**Nunca instancie diretamente:**

```python
# ❌ ERRADO
config = ConfigService()

# Quebra o contrato de singleton e em alguns casos o BaseService vai
# retornar a instância existente, mas o código fica confuso.
```

Os services são registrados em `src/core/application.py` durante a inicialização. Eles estão disponíveis logo após `Application().run()` começar.

## Quais são?

### `ConfigService` (`src/services/config_service.py`)

Configurações persistidas em JSON. Suporta dot notation.

```python
config = container.resolve(ConfigService)

# Ler
theme = config.get("theme.current", "light")  # default = "light"
width = config.get("window.width", 1200)

# Escrever (já persiste)
config.set("theme.current", "dark")

# Escrever em lote sem persistir
config.set("user.name", "Alice", save=False)
config.set("user.email", "alice@ex.com", save=False)
config.save()

# Verificar existência
if config.has("user.email"):
    ...

# Remover
config.remove("user.name")

# Resetar para defaults
config.reset_to_defaults()
```

**Onde os dados são salvos:**
- Windows: `%LOCALAPPDATA%\PySide6AppTemplate\settings.json`
- macOS: `~/Library/Application Support/PySide6AppTemplate/settings.json`
- Linux: `~/.config/PySide6AppTemplate/settings.json`

**Defaults:** carregados de `resources/config/default_settings.json` na primeira execução.

**Signals:**
- `settings_changed(key, value)` — emitido em cada `set`
- `settings_loaded()` — após carregar do disco
- `settings_saved()` — após salvar

---

### `LoggerService` (`src/services/logger_service.py`)

Logs em console e arquivo (com rotação).

```python
logger = container.resolve(LoggerService)

logger.debug("Dados carregados: %s", data)
logger.info("Usuário logou")
logger.warning("Config faltando, usando default")
logger.error("Falha ao salvar", exc_info=True)
logger.critical("Banco offline")

# Exception completa com stack trace
try:
    ...
except Exception:
    logger.exception("Falha em X")
```

**Onde os logs são salvos:**
- Windows: `%LOCALAPPDATA%\PySide6AppTemplate\logs\app_YYYYMMDD.log`
- macOS: `~/Library/Application Support/PySide6AppTemplate/logs/`
- Linux: `~/.local/share/PySide6AppTemplate/logs/`

**Rotação:** 5 arquivos × 5MB = ~25MB máximos.

---

### `NavigationService` (`src/services/navigation_service.py`)

Navegação entre páginas com história. Veja [Navegação](08-navegacao.md) para detalhes.

```python
nav = container.resolve(NavigationService)

# Navegar
nav.navigate_to(PageId.DASHBOARD, {"highlight_id": 42})

# Voltar
nav.go_back()
nav.go_forward()
nav.go_home()

# Estado
nav.can_go_back()
nav.get_current_page_id()
nav.get_current_params()

# Guards (ex.: exigir login)
def auth_guard(page_id: PageId, params: dict) -> bool:
    if page_id == PageId.DASHBOARD and not user_is_logged_in():
        return False
    return True

nav.add_guard(auth_guard)
```

---

### `ThemeService` (`src/services/theme_service.py`)

Aplica QSS e atualiza `QPalette` da `QApplication`. Veja [Tema e Estilos](09-tema-e-estilos.md) para detalhes.

```python
from src.core.types import Theme

theme_service = container.resolve(ThemeService)

# Setar tema
theme_service.set_theme(Theme.DARK)
theme_service.set_theme(Theme.LIGHT)
theme_service.set_theme(Theme.SYSTEM)  # detecta do OS

# Toggle
new_theme = theme_service.toggle_theme()

# Estado
current = theme_service.get_current_theme()
is_dark = theme_service.is_dark

# Cores do tema (úteis para QSS dinâmico)
primary_color = theme_service.get_color("primary")
```

**Signals:**
- `theme_changed(theme)` — emitido após aplicar um tema

---

### `StorageService` (`src/services/storage_service.py`)

Storage key-value em JSON, com suporte a múltiplos namespaces. Usado para dados que não são "configurações" (ex.: cache, estado de formulário em andamento).

```python
storage = container.resolve(StorageService)

# Namespace "default"
storage.set("last_search", "python qt")
search = storage.get("last_search", "")

# Namespace customizado
storage.set("draft", {"title": "..."}, namespace="articles")
draft = storage.get("draft", {}, namespace="articles")

# Verificar existência
if storage.has("last_search"):
    ...

# Remover
storage.remove("last_search")

# Limpar namespace inteiro
storage.clear(namespace="articles")
```

Use `StorageService` para **dados**, `ConfigService` para **preferências**. Isso mantém o `settings.json` do usuário limpo.

---

## Criando um service novo

1. **Crie o arquivo** `src/services/my_service.py` herdando de `BaseService`:

```python
from PySide6.QtCore import Signal

from src.services.base import BaseService


class MyService(BaseService):
    """Descrição."""

    something_happened = Signal(str)

    def _on_init(self) -> None:
        """Chamado uma única vez após construção."""
        self._state: dict[str, int] = {}

    def do_something(self, key: str) -> None:
        self._state[key] = self._state.get(key, 0) + 1
        self.something_happened.emit(key)
```

2. **Registre em `src/core/application.py`**, dentro de `_register_services`:

```python
def _register_services(self) -> None:
    # ... outros services
    from src.services.my_service import MyService
    container.register_singleton(MyService)
```

3. **Use onde precisar:**

```python
my = container.resolve(MyService)
my.do_something("foo")
```

## Por que não usar Python módulos globais como "services"?

Porque testar fica horrível. Com o DI container:

- No teste, você registra um **mock** no container antes do código rodar.
- Fixture `reset_services` garante isolamento entre testes.
- Nenhum estado vaza entre testes.

Com módulos globais você teria que monkey-patch, e aí boa sorte.

## Próximo passo

- [Navegação](08-navegacao.md) para o `NavigationService` em detalhes.
- [Tema e Estilos](09-tema-e-estilos.md) para o `ThemeService`.
