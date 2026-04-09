# 09 — Tema e Estilos

O template suporta tema **claro** e **escuro** via `ThemeService`, que aplica QSS + `QPalette` na `QApplication`.

## Arquivos de estilo

```
resources/styles/
├── base.qss      # Estilos comuns a ambos os temas
├── light.qss     # Overrides do tema claro
└── dark.qss      # Overrides do tema escuro
```

Ao setar um tema, o `ThemeService` carrega `base.qss` + o arquivo do tema específico, concatena, e aplica via `QApplication.setStyleSheet()`.

## Trocando o tema em código

```python
from src.core.container import container
from src.core.types import Theme
from src.services.theme_service import ThemeService

theme_service = container.resolve(ThemeService)

theme_service.set_theme(Theme.DARK)
theme_service.set_theme(Theme.LIGHT)
theme_service.set_theme(Theme.SYSTEM)  # detecta do OS

# Toggle rápido
theme_service.toggle_theme()
```

## Trocando o tema via UI

- O `Header` tem um botão 🌙/☀️ que chama `toggle_theme()` automaticamente.
- A página **Configurações** tem um combo para escolher light/dark/system.

## Persistência

A preferência é salva em `config.set("theme.current", ...)` e recarregada no próximo boot. Assim o usuário não precisa re-selecionar.

## Reagindo a mudanças de tema

Conecte ao signal `theme_changed`:

```python
class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        from src.core.container import container
        from src.services.theme_service import ThemeService

        theme = container.resolve(ThemeService)
        theme.theme_changed.connect(self._on_theme_changed)

    def _on_theme_changed(self, theme):
        # Reaplica estilos específicos, se necessário
        self._refresh_colors()
```

**Dica:** a maioria dos widgets não precisa fazer nada — eles herdam do QSS automaticamente. Só intervenha se você tem cores hardcoded no código Python.

## Escrevendo QSS

PySide6/Qt aceita um subset de CSS. Exemplos úteis:

```qss
/* Seletor por classe Qt */
QPushButton {
    background: #0078D4;
    color: white;
    border-radius: 4px;
    padding: 8px 16px;
}

QPushButton:hover {
    background: #106EBE;
}

QPushButton:disabled {
    background: #E0E0E0;
    color: #999;
}

/* Seletor por property — bom para variantes */
QPushButton[class="primary"] {
    background: #0078D4;
}

QPushButton[class="danger"] {
    background: #DC3545;
}

/* Aplicável via self.setProperty("class", "primary") no Python */
```

Use `setProperty("class", "xxx")` + reaplique estilo com `self.style().unpolish(widget); self.style().polish(widget)` se mudar dinamicamente.

## Adicionando um tema custom

Suponha que você queira um tema "high contrast":

### 1. Crie o arquivo QSS

```
resources/styles/high_contrast.qss
```

### 2. Adicione ao enum `Theme`

```python
# src/core/types.py
class Theme(Enum):
    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"
    HIGH_CONTRAST = "high_contrast"  # 👈 NOVO
```

### 3. Atualize `_apply_palette()` em `theme_service.py`

Adicione o branch para `HIGH_CONTRAST` com as cores da paleta nativa.

### 4. Teste

```python
theme_service.set_theme(Theme.HIGH_CONTRAST)
```

## Acessando cores do tema no código

```python
theme_service = container.resolve(ThemeService)

primary = theme_service.get_color("primary")   # QColor
danger = theme_service.get_color("danger")
background = theme_service.get_color("background")
text = theme_service.get_color("text")
```

Cores disponíveis: `primary`, `secondary`, `success`, `danger`, `warning`, `info`, `light`, `dark`, `background`, `surface`, `text`, `text_secondary`, `border`.

Use para widgets customizados que precisam de cores dinâmicas (ex.: gráficos desenhados no `paintEvent`).

## Perguntas frequentes

**Q: Por que usar `QPalette` E `setStyleSheet`?**
A: QSS cobre a maioria dos widgets, mas alguns (especialmente nativos) respondem só à `QPalette`. Aplicar ambos garante consistência visual.

**Q: Meu componente não fica dark quando troco o tema.**
A: Provavelmente você tem cores hardcoded no `setStyleSheet(...)` do próprio componente. Ou você extrai para `base.qss` via classes, ou conecta ao `theme_changed` e reaplica.

**Q: Como faço um "glow" / "shadow"?**
A: Use `QGraphicsDropShadowEffect` — QSS não suporta box-shadow no Qt.

**Q: Posso usar variáveis CSS (como `var(--primary)`)?**
A: Qt não suporta. Defina constantes Python e monte QSS via f-string, ou use `theme_service.get_color()`.

## Próximo passo

- [Layout Responsivo](10-layout-responsivo.md) — Grid e FlowLayout.
