# 06 — Biblioteca de Componentes

Catálogo dos componentes incluídos no template. Cada um vive em `src/components/<categoria>/<nome>.py` e pode ser importado assim:

```python
from src.components.buttons import PrimaryButton
from src.components.cards import InfoCard
from src.components.forms import TextInput
```

---

## Buttons (`src/components/buttons/`)

### `PrimaryButton`

Botão de ação principal. Usado para o call-to-action da tela.

```python
btn = PrimaryButton(text="Salvar")
btn.clicked.connect(self._on_save)
```

### `SecondaryButton`

Botão secundário — mesmas dimensões, estilo menos prominente.

### `IconButton`

Botão que mostra apenas um ícone. Aceita `icon` (QIcon) e `tooltip`.

### `ToggleButton`

Botão com estado ligado/desligado. Usa `isChecked()`/`setChecked()`.

---

## Cards (`src/components/cards/`)

### `BasicCard`

Container simples com borda e padding. Use para agrupar conteúdo.

### `InfoCard`

Card com valor grande (número) + título + cor de acento.

```python
card = InfoCard(title="Total de Vendas", value="R$ 12.340,00", color="#28A745")
# Posteriormente:
card.set_value("R$ 15.000,00")
```

Usado no Dashboard para as métricas.

### `ActionCard`

Card com botões de ação no rodapé.

---

## Dialogs (`src/components/dialogs/`)

### `BaseDialog`

Classe base. Só use diretamente se precisar de um dialog customizado.

### `ConfirmDialog`

Sim/Não para ações destrutivas.

```python
result = ConfirmDialog(title="Apagar?", message="Tem certeza?").exec()
if result == QDialog.Accepted:
    self._delete()
```

### `AlertDialog`

Alerta informativo (info/warning/error).

### `FormDialog`

Dialog com formulário embutido (útil para criar/editar entidades).

---

## Feedback (`src/components/feedback/`)

### `Badge`

Pequeno rótulo colorido para status (ex.: "Novo", "Admin").

### `ProgressBar`

Barra de progresso estilizada.

### `Spinner`

Indicador de carregamento animado.

### `Toast`

Notificação temporária que aparece no canto.

### `Tooltip`

Wrapper de tooltip customizado (prefira `setToolTip()` padrão do Qt na maioria dos casos).

---

## Forms (`src/components/forms/`)

### `TextInput`

Campo de texto com label e suporte a validação.

```python
email_input = TextInput(
    label="E-mail",
    placeholder="seu@email.com",
    validator=lambda value: "@" in value,
)
```

### `SelectInput`

Dropdown (combobox) estilizado com label.

### `Checkbox`

Checkbox com label à direita.

### `RadioGroup`

Grupo de radio buttons.

### `FormField`

Wrapper que adiciona label, hint e mensagem de erro ao redor de qualquer input.

---

## Icons (`src/components/icons/`)

### `Icon`

Wrapper que carrega ícones de `resources/icons/` de forma consistente.

---

## Layout (`src/components/layout/`)

### `Header`

Header da aplicação. Mostra título, botão de voltar (opcional) e toggle de tema.

```python
header = Header(title="Dashboard")
header.set_title("Vendas")
header.show_back_button(True)
```

### `Sidebar`

Barra lateral data-driven. Use `set_items()` para popular:

```python
from src.components.layout.sidebar import Sidebar, SidebarMenuItem

sidebar = Sidebar()
sidebar.set_items([
    SidebarMenuItem(PageId.HOME, "Início", "🏠"),
    SidebarMenuItem(PageId.SETTINGS, "Configurações", "⚙️"),
])
```

O `MainWindow` já faz isso automaticamente a partir de `FEATURE_METADATA` — você só precisa ligar `set_items` manualmente se criar uma sidebar adicional.

### `Footer`

Rodapé da aplicação. Aceita `text` e `show_version`.

### `ContentArea`

Container para conteúdo com scroll opcional e padding.

### `Grid`

Grid de 12 colunas estilo Bootstrap. Veja [Layout Responsivo](10-layout-responsivo.md).

### `FlowLayout`

Layout que faz wrap automático. Veja [Layout Responsivo](10-layout-responsivo.md).

---

## Tables (`src/components/tables/`)

### `DataTable`

Tabela com colunas definidas por lista de dicts.

```python
columns = [
    {"key": "name", "label": "Nome"},
    {"key": "email", "label": "E-mail"},
]
data = [
    {"name": "Alice", "email": "alice@ex.com"},
    {"name": "Bruno", "email": "bruno@ex.com"},
]
table = DataTable(columns=columns, data=data)
```

Sinais: `row_clicked(row, data)`, `row_double_clicked(row, data)`.

Usada no Dashboard para listar vendas.

### `ListView`

Lista vertical simples.

### `TreeView`

Árvore hierárquica.

---

## Como ver cada componente ao vivo

Rode a aplicação e clique em **Componentes** no sidebar. A página Showcase mostra exemplos interativos agrupados por categoria.

## Como criar um componente novo

Veja [Criando um Componente](05-criando-um-componente.md).
