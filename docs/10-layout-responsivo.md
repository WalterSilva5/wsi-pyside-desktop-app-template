# 10 — Layout Responsivo

O template oferece dois sistemas de layout responsivo inspirados em CSS:

- **`Grid`** — sistema de **12 colunas** com breakpoints (estilo Bootstrap).
- **`FlowLayout`** — wrap automático de widgets de largura fixa (estilo flexbox `wrap`).

Ambos vivem em `src/components/layout/`.

## Breakpoints

| Nome | Largura | Descrição |
|---|---|---|
| `xs` | `< 576px` | Telefones em retrato |
| `sm` | `>= 576px` | Telefones em paisagem |
| `md` | `>= 768px` | Tablets |
| `lg` | `>= 992px` | Desktops |
| `xl` | `>= 1200px` | Desktops grandes |

## `Grid` — 12 colunas com breakpoints

### Conceito

Cada linha do grid tem 12 colunas virtuais. Um `GridColumn` ocupa `span` colunas (1–12). Você pode definir spans diferentes por breakpoint — quando a janela encolhe, as colunas se reorganizam.

### Exemplo básico

```python
from src.components.layout.grid import Grid
from src.components.cards.info_card import InfoCard

grid = Grid()

# Row com 4 cards iguais (3 colunas cada = 12 total)
row = grid.add_row()
for i in range(4):
    col = row.create_column(
        span=3,    # 4 cards por linha em xl (12/3=4)
        md=6,      # 2 cards por linha em md (12/6=2)
        sm=12,     # 1 card por linha em sm/xs (full width)
    )
    col.add_widget(InfoCard(title=f"Métrica {i}", value=str(i * 100)))
```

**Resultado:**
- **xl (≥1200px)**: 4 cards lado a lado
- **md (≥768px)**: 2 cards por linha
- **sm (<768px)**: 1 card por linha (empilhado)

### Layout mais complexo

```python
grid = Grid()

# Row 1: header full width
header_row = grid.add_row()
header_row.create_column(span=12).add_widget(Header(title="Minha App"))

# Row 2: sidebar + conteúdo principal + painel direito
main_row = grid.add_row()

sidebar_col = main_row.create_column(span=3, md=4, sm=12)
sidebar_col.add_widget(self._create_sidebar())

content_col = main_row.create_column(span=6, md=8, sm=12)
content_col.add_widget(self._create_content())

right_col = main_row.create_column(span=3, md=12, sm=12)
right_col.add_widget(self._create_right_panel())
```

Neste exemplo:
- **xl/lg**: 3 colunas lado a lado (sidebar 3, content 6, right 3)
- **md**: sidebar vai pra esquerda com 4/12, content ao lado com 8/12, right panel **quebra pra linha de baixo** com 12/12
- **sm**: tudo empilhado, cada um 12/12

### Regras dos spans

- `span` (obrigatório): valor para o maior breakpoint (`xl`).
- `lg`, `md`, `sm`, `xs`: valores para breakpoints menores. Se omitidos, herdam do breakpoint maior mais próximo.
- Total por linha **não precisa** somar 12 — o grid só limita; espaço extra fica vazio.
- Se a soma ultrapassa 12, a coluna seguinte quebra pra próxima linha automaticamente.

## `FlowLayout` — wrap automático

Use quando você tem **widgets de largura fixa** que devem se reorganizar automaticamente quando o container é redimensionado.

### Exemplo

```python
from src.components.layout.flow_layout import FlowLayout
from src.components.cards.info_card import InfoCard

container = QWidget()
flow = FlowLayout(container, h_spacing=16, v_spacing=16)
flow.setContentsMargins(16, 16, 16, 16)

for i in range(12):
    card = InfoCard(title=f"Item {i}", value=f"#{i:02d}")
    card.setFixedWidth(200)  # ← largura fixa é importante
    flow.addWidget(card)
```

**Resultado:** os cards fluem como palavras em um parágrafo — quantos couberem na linha, e depois vão pra próxima.

### Quando usar qual?

| Situação | Use |
|---|---|
| Layout estruturado (header/sidebar/content) | **`Grid`** |
| Diferentes proporções por breakpoint | **`Grid`** |
| Grade de cards, tags, ou itens iguais | **`FlowLayout`** |
| Precisa controlar exatamente o espaçamento por coluna | **`Grid`** |
| Quero lista de filtros/chips que quebram linha | **`FlowLayout`** |

## Vendo na prática

Rode a aplicação, abra **Layout Responsivo** no sidebar, e redimensione a janela. Você vê:

1. **Seção 1:** FlowLayout com cards de larguras diferentes — quebram linha conforme a janela.
2. **Seção 2:** Grid com 4 cards igual-tamanho — reorganizam nos breakpoints.
3. **Seção 3:** Layout com spans mistos (8+4, 3+6+3, etc.).
4. **Seção 4:** Layout real (header + sidebar + conteúdo + right panel + footer).
5. **Referência:** tabela com os breakpoints atuais.

Código de referência: `src/features/responsive_demo/page.py`.

## Dicas de performance

- O `Grid` escuta `resizeEvent` e recalcula. Para layouts muito pesados (centenas de widgets), considere debouncing.
- `FlowLayout` também reposiciona em cada resize — se você tem 1000+ items, prefira `QListView` com delegate customizado.
- Teste em uma janela menor (ex.: 600px) para garantir que os empilhamentos funcionam.

## Perguntas frequentes

**Q: Posso ter grids aninhados?**
A: Sim. Um `GridColumn` aceita qualquer widget — inclusive outro `Grid`.

**Q: E se eu quiser um gap customizado entre colunas?**
A: Ajuste o `setSpacing()` do layout interno, ou use widgets `spacer` entre os `add_widget()`.

**Q: Os breakpoints são ajustáveis?**
A: Eles são constantes em `grid.py`. Altere lá se precisar de outros valores — só tome cuidado para atualizar a documentação.

**Q: E para mobile/touch?**
A: Este é um template desktop. Para mobile, Qt oferece Qt Quick/QML, que é uma stack separada.

## Próximo passo

- [Modelos e Repositórios](11-modelos-e-repositorios.md) — persistência de dados.
