# 01 — Início Rápido

Este guia mostra como instalar as dependências, rodar o template e entender o que você está vendo.

## Pré-requisitos

- **Python 3.10 ou superior** (3.12 é a versão recomendada e está fixada em `.python-version`)
- **[uv](https://docs.astral.sh/uv/)** (recomendado) ou **pip**
- **Windows**, **macOS** ou **Linux** — o template é multiplataforma

## Instalando uv (opcional, mas recomendado)

`uv` é um gerenciador de pacotes Python escrito em Rust que instala dependências 10–100× mais rápido que o pip.

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Clonando e rodando

### Com uv (recomendado)

```bash
git clone https://github.com/walterpsilva/wsi-pyside-desktop-app-template.git
cd wsi-pyside-desktop-app-template

# Cria o venv e instala as dependências
uv sync

# Roda a aplicação
uv run python main.py
```

### Com pip

```bash
git clone https://github.com/walterpsilva/wsi-pyside-desktop-app-template.git
cd wsi-pyside-desktop-app-template

# Cria o venv
python -m venv .venv

# Ativa
# Windows (cmd):
.venv\Scripts\activate.bat
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate

# Instala em modo editável com extras de dev
pip install -e ".[dev]"

# Roda
python main.py
```

## O que você deve ver

Ao rodar, uma janela 1200×800 abre centralizada na tela, com:

- **Sidebar à esquerda** com os itens: Início, Dashboard, Componentes, Layout Responsivo, Configurações.
- **Header no topo** com o título da página atual e um botão de toggle de tema (🌙/☀️).
- **Área central** mostrando a página inicial.

Cada item da sidebar abre uma feature diferente. Todos são exemplos de padrões que você pode copiar e adaptar.

## Primeiras explorações

Experimente:

1. **Clicar em "Dashboard"** — você verá cards de métricas + tabela de vendas. Esta feature mostra como combinar `BaseController`, um repositório próprio e componentes `InfoCard`/`DataTable`.
2. **Clicar em "Layout Responsivo"** e redimensionar a janela — os cards reorganizam automaticamente nos breakpoints (xs/sm/md/lg/xl).
3. **Clicar no 🌙 no header** — a aplicação alterna entre tema claro e escuro. Essa preferência é salva em `~/AppData/Local/PySide6AppTemplate/settings.json` (Windows) ou equivalente.
4. **Clicar em "Configurações"** — muda o tema, idioma e opções de janela. As mudanças persistem entre execuções.

## Próximos passos

- Leia [Arquitetura](02-arquitetura.md) para entender a estrutura.
- Leia [Criando uma Feature](04-criando-uma-feature.md) quando quiser adicionar sua primeira tela.

## Troubleshooting

### `ModuleNotFoundError: No module named 'PySide6'`

Suas dependências não foram instaladas. Rode `uv sync` (ou `pip install -e ".[dev]"`).

### `error: No Python at ...` ao rodar `uv run`

O venv está apontando para um Python que não existe mais. Delete `.venv/` e rode `uv sync` novamente.

### Janela abre e fecha imediatamente

Provavelmente um erro no import. Rode `python main.py` (sem redirecionar) no terminal e leia a stack trace.

### Problemas de display no Linux

Instale as dependências do Qt:

```bash
sudo apt install libegl1-mesa libxkbcommon0 libxcb-cursor0
```
