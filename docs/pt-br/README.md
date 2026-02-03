# Template de Aplicacao Desktop PySide6

Um template escalavel e bem estruturado para construir aplicacoes desktop multiplataforma com PySide6, implementando design patterns modernos e boas praticas.

## Recursos

- **Arquitetura Moderna**: Padrao MVC com injecao de dependencia
- **Navegacao Type-safe**: Roteamento baseado em Enum com suporte a historico
- **Sistema de Temas**: Modo claro/escuro com folhas de estilo QSS
- **Biblioteca de Componentes**: 20+ componentes de UI reutilizaveis
- **Event Bus**: Comunicacao desacoplada via Qt Signals
- **Gerenciamento de Configuracao**: Configuracoes baseadas em JSON com acesso por notacao de ponto
- **Sistema de Logging**: Logs com rotacao de arquivos e multiplos niveis
- **Padrao Repository**: Abstracao de persistencia de dados
- **Padrao Factory**: Criacao dinamica de componentes e paginas
- **Type Hints Completos**: Tipagem completa para melhor suporte da IDE

## Estrutura do Projeto

```
wsi-pyside-desktop-app-template/
├── main.py                     # Ponto de entrada
├── pyproject.toml              # Configuracao do projeto
├── .python-version             # Versao Python para uv
│
├── src/
│   ├── app.py                  # Entrada do modulo
│   │
│   ├── core/                   # Infraestrutura core
│   │   ├── application.py      # Classe principal Application
│   │   ├── container.py        # Container de Injecao de Dependencia
│   │   ├── signals.py          # Event Bus (padrao Observer)
│   │   ├── exceptions.py       # Excecoes customizadas
│   │   └── types.py            # Enums e definicoes de tipos
│   │
│   ├── services/               # Servicos da aplicacao (Singleton)
│   │   ├── config_service.py   # Gerenciamento de configuracao
│   │   ├── navigation_service.py # Roteamento type-safe
│   │   ├── theme_service.py    # Troca de temas
│   │   ├── logger_service.py   # Logging centralizado
│   │   └── storage_service.py  # Armazenamento local key-value
│   │
│   ├── models/                 # Modelos de dados
│   │   ├── user.py             # Modelo de usuario
│   │   ├── settings.py         # Configuracoes da aplicacao
│   │   └── repositories/       # Camada de acesso a dados
│   │
│   ├── controllers/            # Logica de negocios
│   │   ├── home_controller.py
│   │   ├── settings_controller.py
│   │   └── showcase_controller.py
│   │
│   ├── views/                  # Camada de UI
│   │   ├── main_window.py      # Janela principal
│   │   ├── pages/              # Paginas da aplicacao
│   │   └── components/         # Componentes reutilizaveis
│   │
│   ├── factories/              # Padrao Factory
│   │   ├── component_factory.py
│   │   ├── page_factory.py
│   │   └── dialog_factory.py
│   │
│   └── utils/                  # Utilitarios
│       ├── decorators.py       # Singleton, debounce, throttle
│       ├── validators.py       # Validacao de entrada
│       └── helpers.py          # Funcoes auxiliares
│
├── resources/                  # Recursos estaticos
│   ├── config/                 # Arquivos de configuracao
│   ├── styles/                 # Folhas de estilo QSS
│   ├── icons/                  # Icones da aplicacao
│   └── images/                 # Imagens
│
├── tests/                      # Suite de testes
│   ├── unit/                   # Testes unitarios
│   ├── integration/            # Testes de integracao
│   └── ui/                     # Testes de UI
│
└── docs/                       # Documentacao
    ├── en/                     # Docs em ingles
    └── pt-br/                  # Docs em portugues
```

---

## Inicio Rapido

### Pre-requisitos

- Python 3.10+ (3.12 recomendado)
- [uv](https://docs.astral.sh/uv/) (recomendado) ou pip

### Opcao 1: Usando uv (Recomendado)

[uv](https://docs.astral.sh/uv/) e um gerenciador de pacotes e projetos Python extremamente rapido, escrito em Rust. Oferece instalacao de dependencias 10-100x mais rapida que o pip.

#### Instalar uv

**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Configurar e Executar

```bash
# Clonar o repositorio
git clone https://github.com/user/wsi-pyside-desktop-app-template.git
cd wsi-pyside-desktop-app-template

# Sincronizar dependencias (cria venv e instala tudo)
uv sync

# Executar a aplicacao
uv run python main.py

# Ou executar como modulo
uv run python -m src.app
```

#### Desenvolvimento com uv

```bash
# Instalar com dependencias de desenvolvimento
uv sync --all-extras

# Adicionar nova dependencia
uv add nome-do-pacote

# Adicionar dependencia de desenvolvimento
uv add --dev nome-do-pacote

# Executar testes
uv run pytest

# Executar linting
uv run black src/ tests/
uv run flake8 src/ tests/
uv run mypy src/

# Atualizar dependencias
uv lock --upgrade
uv sync
```

### Opcao 2: Usando pip

```bash
# Clonar o repositorio
git clone https://github.com/user/wsi-pyside-desktop-app-template.git
cd wsi-pyside-desktop-app-template

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -e .

# Ou com dependencias de desenvolvimento
pip install -e ".[dev]"

# Executar a aplicacao
python main.py
```

---

## Executando a Aplicacao

### Com uv (recomendado)

```bash
# Executar script principal
uv run python main.py

# Executar como modulo
uv run python -m src.app

# Executar com versao especifica do Python
uv run --python 3.12 python main.py
```

### Com pip/venv

```bash
# Certifique-se que o venv esta ativado
python main.py

# Ou como modulo
python -m src.app
```

### Usando o comando instalado

Apos a instalacao, voce tambem pode executar:

```bash
# Com uv
uv run pyside6-app

# Com pip (apos pip install -e .)
pyside6-app
```

---

## Uso

### Adicionando uma Nova Pagina

1. Crie uma pagina em `src/views/pages/`:

```python
from src.views.base import BasePage

class MinhaPagina(BasePage):
    def _setup_ui(self) -> None:
        # Construa sua UI aqui
        pass

    def on_show(self) -> None:
        # Chamado quando a pagina se torna visivel
        pass
```

2. Registre o ID da pagina em `src/core/types.py`:

```python
class PageId(Enum):
    HOME = "home"
    SETTINGS = "settings"
    MINHA_PAGINA = "minha_pagina"  # Adicione sua pagina
```

3. Registre na factory de paginas (`src/factories/page_factory.py`):

```python
from src.views.pages.minha_pagina import MinhaPagina

PageFactory.register(PageId.MINHA_PAGINA, MinhaPagina)
```

4. Adicione navegacao na sidebar ou header.

### Usando Componentes

```python
from src.views.components.buttons import PrimaryButton, SecondaryButton
from src.views.components.cards import InfoCard
from src.views.components.forms import TextInput, SelectInput

# Criar um botao
btn = PrimaryButton("Clique Aqui")
btn.clicked.connect(self._on_click)

# Criar um card de informacao
card = InfoCard(
    title="Estatisticas",
    value="1.234",
    description="Total de usuarios"
)

# Criar um campo de formulario
email_input = TextInput(
    label="Email",
    placeholder="Digite seu email",
    validator=lambda x: "@" in x
)
```

### Usando Servicos

```python
from src.core.container import container
from src.services.config_service import ConfigService
from src.services.navigation_service import NavigationService
from src.core.types import PageId

# Obter servicos do container
config = container.resolve(ConfigService)
nav = container.resolve(NavigationService)

# Usar configuracao
theme = config.get("theme", "light")
config.set("user.name", "Joao")

# Navegar para uma pagina
nav.navigate_to(PageId.SETTINGS)
nav.go_back()
```

### Troca de Tema

```python
from src.services.theme_service import ThemeService
from src.core.types import Theme

theme_service = container.resolve(ThemeService)
theme_service.set_theme(Theme.DARK)
current = theme_service.current_theme
```

---

## Design Patterns

| Padrao | Implementacao | Proposito |
|--------|---------------|-----------|
| **Singleton** | Servicos (Config, Logger, etc.) | Gerenciamento de instancia unica |
| **Observer** | EventBus com Qt Signals | Comunicacao desacoplada |
| **Factory** | ComponentFactory, PageFactory | Criacao dinamica de objetos |
| **Repository** | JsonFileRepository | Abstracao de acesso a dados |
| **Injecao de Dependencia** | Classe Container | Baixo acoplamento |
| **MVC** | Models, Views, Controllers | Separacao de responsabilidades |

---

## Biblioteca de Componentes

### Botoes

- `PrimaryButton` - Botao de acao principal
- `SecondaryButton` - Acoes secundarias
- `IconButton` - Botao apenas com icone
- `ToggleButton` - Toggle liga/desliga

### Cards

- `BasicCard` - Card de conteudo simples
- `InfoCard` - Card com titulo, valor, descricao
- `ActionCard` - Card com botoes de acao

### Formularios

- `TextInput` - Campo de texto com validacao
- `SelectInput` - Selecao dropdown
- `Checkbox` - Checkbox com label
- `RadioGroup` - Grupo de radio buttons
- `FormField` - Wrapper generico de campo

### Dialogos

- `ConfirmDialog` - Confirmacao Sim/Nao
- `AlertDialog` - Alerta informativo
- `FormDialog` - Formulario em dialogo

### Feedback

- `Badge` - Badge de status
- `ProgressBar` - Indicador de progresso
- `Spinner` - Spinner de carregamento
- `Toast` - Notificacao toast
- `Tooltip` - Tooltip de hover

### Tabelas

- `DataTable` - Tabela de dados completa
- `ListView` - Lista vertical
- `TreeView` - Visualizacao em arvore hierarquica

### Layout

- `Header` - Cabecalho da aplicacao
- `Sidebar` - Sidebar de navegacao
- `Footer` - Rodape da aplicacao
- `ContentArea` - Wrapper de conteudo principal

---

## Desenvolvimento

### Executando Testes

```bash
# Com uv
uv run pytest
uv run pytest --cov=src
uv run pytest tests/unit/test_services/test_config_service.py

# Com pip
pytest
pytest --cov=src
```

### Estilo de Codigo

```bash
# Com uv
uv run black src/ tests/
uv run isort src/ tests/
uv run flake8 src/ tests/
uv run mypy src/

# Com pip
black src/ tests/
isort src/ tests/
flake8 src/ tests/
mypy src/
```

### Pre-commit Hooks

```bash
# Instalar hooks
pre-commit install

# Executar em todos os arquivos
pre-commit run --all-files
```

---

## Solucao de Problemas

### Problemas Comuns

**PySide6 nao encontrado:**

```bash
# Com uv
uv sync --reinstall

# Com pip
pip install --force-reinstall PySide6
```

**Erros de permissao no Windows:**

Execute o PowerShell como Administrador ou use:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Problemas de display no Linux:**

Instale os pacotes de sistema necessarios:

```bash
sudo apt-get install libegl1-mesa libxkbcommon0 libxcb-cursor0
```

**uv nao encontrado apos instalacao:**

Reinicie seu terminal ou adicione ao PATH:

```bash
# Linux/macOS
export PATH="$HOME/.cargo/bin:$PATH"

# Windows - reinicie o PowerShell ou adicione ao PATH do sistema
```

---

## Contribuindo

1. Faca um fork do repositorio
2. Crie uma branch de feature (`git checkout -b feature/recurso-incrivel`)
3. Commit suas mudancas (`git commit -m 'Adiciona recurso incrivel'`)
4. Push para a branch (`git push origin feature/recurso-incrivel`)
5. Abra um Pull Request

---

## Licenca

Este projeto esta licenciado sob a Licenca MIT - veja o arquivo [LICENSE](../../LICENSE) para detalhes.

---

## Agradecimentos

- [PySide6](https://doc.qt.io/qtforpython/) - Qt para Python
- [Qt](https://www.qt.io/) - Framework multiplataforma
- [uv](https://docs.astral.sh/uv/) - Gerenciador de pacotes Python rapido
