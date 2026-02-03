# PySide6 Desktop Application Template

A scalable, well-structured template for building cross-platform desktop applications with PySide6, implementing modern design patterns and best practices.

## Features

- **Modern Architecture**: MVC pattern with dependency injection
- **Type-safe Navigation**: Enum-based routing with history support
- **Theme System**: Light/Dark mode with QSS stylesheets
- **Component Library**: 20+ reusable UI components
- **Event Bus**: Decoupled communication via Qt Signals
- **Configuration Management**: JSON-based settings with dot notation access
- **Logging System**: Rotating file logs with multiple levels
- **Repository Pattern**: Data persistence abstraction
- **Factory Pattern**: Dynamic component and page creation
- **Full Type Hints**: Complete typing for better IDE support

## Project Structure

```
wsi-pyside-desktop-app-template/
├── main.py                     # Application entry point
├── pyproject.toml              # Project configuration
├── .python-version             # Python version for uv
│
├── src/
│   ├── app.py                  # Module entry point
│   │
│   ├── core/                   # Core infrastructure
│   │   ├── application.py      # Main Application class
│   │   ├── container.py        # Dependency Injection container
│   │   ├── signals.py          # Event Bus (Observer pattern)
│   │   ├── exceptions.py       # Custom exceptions
│   │   └── types.py            # Enums and type definitions
│   │
│   ├── services/               # Application services (Singleton)
│   │   ├── config_service.py   # Configuration management
│   │   ├── navigation_service.py # Type-safe routing
│   │   ├── theme_service.py    # Theme switching
│   │   ├── logger_service.py   # Centralized logging
│   │   └── storage_service.py  # Local key-value storage
│   │
│   ├── models/                 # Data models
│   │   ├── user.py             # User model
│   │   ├── settings.py         # Application settings
│   │   └── repositories/       # Data access layer
│   │
│   ├── controllers/            # Business logic
│   │   ├── home_controller.py
│   │   ├── settings_controller.py
│   │   └── showcase_controller.py
│   │
│   ├── views/                  # UI layer
│   │   ├── main_window.py      # Main window
│   │   ├── pages/              # Application pages
│   │   └── components/         # Reusable components
│   │
│   ├── factories/              # Factory pattern
│   │   ├── component_factory.py
│   │   ├── page_factory.py
│   │   └── dialog_factory.py
│   │
│   └── utils/                  # Utilities
│       ├── decorators.py       # Singleton, debounce, throttle
│       ├── validators.py       # Input validation
│       └── helpers.py          # Helper functions
│
├── resources/                  # Static resources
│   ├── config/                 # Configuration files
│   ├── styles/                 # QSS stylesheets
│   ├── icons/                  # Application icons
│   └── images/                 # Images
│
├── tests/                      # Test suite
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   └── ui/                     # UI tests
│
└── docs/                       # Documentation
    ├── en/                     # English docs
    └── pt-br/                  # Portuguese docs
```

---

## Quick Start

### Prerequisites

- Python 3.10+ (3.12 recommended)
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Option 1: Using uv (Recommended)

[uv](https://docs.astral.sh/uv/) is an extremely fast Python package and project manager written in Rust. It provides 10-100x faster dependency installation than pip.

#### Install uv

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Setup and Run

```bash
# Clone the repository
git clone https://github.com/user/wsi-pyside-desktop-app-template.git
cd wsi-pyside-desktop-app-template

# Sync dependencies (creates venv and installs everything)
uv sync

# Run the application
uv run python main.py

# Or run as module
uv run python -m src.app
```

#### Development with uv

```bash
# Install with dev dependencies
uv sync --all-extras

# Add a new dependency
uv add package-name

# Add a dev dependency
uv add --dev package-name

# Run tests
uv run pytest

# Run linting
uv run black src/ tests/
uv run flake8 src/ tests/
uv run mypy src/

# Update dependencies
uv lock --upgrade
uv sync
```

### Option 2: Using pip

```bash
# Clone the repository
git clone https://github.com/user/wsi-pyside-desktop-app-template.git
cd wsi-pyside-desktop-app-template

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -e .

# Or with dev dependencies
pip install -e ".[dev]"

# Run the application
python main.py
```

---

## Running the Application

### With uv (recommended)

```bash
# Run main script
uv run python main.py

# Run as module
uv run python -m src.app

# Run with specific Python version
uv run --python 3.12 python main.py
```

### With pip/venv

```bash
# Make sure venv is activated
python main.py

# Or as module
python -m src.app
```

### Using the installed command

After installation, you can also run:

```bash
# With uv
uv run pyside6-app

# With pip (after pip install -e .)
pyside6-app
```

---

## Usage

### Adding a New Page

1. Create a page in `src/views/pages/`:

```python
from src.views.base import BasePage

class MyPage(BasePage):
    def _setup_ui(self) -> None:
        # Build your UI here
        pass

    def on_show(self) -> None:
        # Called when page becomes visible
        pass
```

2. Register the page ID in `src/core/types.py`:

```python
class PageId(Enum):
    HOME = "home"
    SETTINGS = "settings"
    MY_PAGE = "my_page"  # Add your page
```

3. Register in the page factory (`src/factories/page_factory.py`):

```python
from src.views.pages.my_page import MyPage

PageFactory.register(PageId.MY_PAGE, MyPage)
```

4. Add navigation in sidebar or header.

### Using Components

```python
from src.views.components.buttons import PrimaryButton, SecondaryButton
from src.views.components.cards import InfoCard
from src.views.components.forms import TextInput, SelectInput

# Create a button
btn = PrimaryButton("Click Me")
btn.clicked.connect(self._on_click)

# Create an info card
card = InfoCard(
    title="Statistics",
    value="1,234",
    description="Total users"
)

# Create a form input
email_input = TextInput(
    label="Email",
    placeholder="Enter your email",
    validator=lambda x: "@" in x
)
```

### Using Services

```python
from src.core.container import container
from src.services.config_service import ConfigService
from src.services.navigation_service import NavigationService
from src.core.types import PageId

# Get services from container
config = container.resolve(ConfigService)
nav = container.resolve(NavigationService)

# Use configuration
theme = config.get("theme", "light")
config.set("user.name", "John")

# Navigate to a page
nav.navigate_to(PageId.SETTINGS)
nav.go_back()
```

### Theme Switching

```python
from src.services.theme_service import ThemeService
from src.core.types import Theme

theme_service = container.resolve(ThemeService)
theme_service.set_theme(Theme.DARK)
current = theme_service.current_theme
```

---

## Design Patterns

| Pattern | Implementation | Purpose |
|---------|----------------|---------|
| **Singleton** | Services (Config, Logger, etc.) | Single instance management |
| **Observer** | EventBus with Qt Signals | Decoupled communication |
| **Factory** | ComponentFactory, PageFactory | Dynamic object creation |
| **Repository** | JsonFileRepository | Data access abstraction |
| **Dependency Injection** | Container class | Loose coupling |
| **MVC** | Models, Views, Controllers | Separation of concerns |

---

## Component Library

### Buttons

- `PrimaryButton` - Main action button
- `SecondaryButton` - Secondary actions
- `IconButton` - Button with icon only
- `ToggleButton` - On/off toggle

### Cards

- `BasicCard` - Simple content card
- `InfoCard` - Card with title, value, description
- `ActionCard` - Card with action buttons

### Forms

- `TextInput` - Text field with validation
- `SelectInput` - Dropdown selection
- `Checkbox` - Checkbox with label
- `RadioGroup` - Radio button group
- `FormField` - Generic form field wrapper

### Dialogs

- `ConfirmDialog` - Yes/No confirmation
- `AlertDialog` - Information alert
- `FormDialog` - Form in dialog

### Feedback

- `Badge` - Status badge
- `ProgressBar` - Progress indicator
- `Spinner` - Loading spinner
- `Toast` - Notification toast
- `Tooltip` - Hover tooltip

### Tables

- `DataTable` - Full-featured data table
- `ListView` - Vertical list view
- `TreeView` - Hierarchical tree view

### Layout

- `Header` - Application header
- `Sidebar` - Navigation sidebar
- `Footer` - Application footer
- `ContentArea` - Main content wrapper

---

## Development

### Running Tests

```bash
# With uv
uv run pytest
uv run pytest --cov=src
uv run pytest tests/unit/test_services/test_config_service.py

# With pip
pytest
pytest --cov=src
```

### Code Style

```bash
# With uv
uv run black src/ tests/
uv run isort src/ tests/
uv run flake8 src/ tests/
uv run mypy src/

# With pip
black src/ tests/
isort src/ tests/
flake8 src/ tests/
mypy src/
```

### Pre-commit Hooks

```bash
# Install hooks
pre-commit install

# Run on all files
pre-commit run --all-files
```

---

## Troubleshooting

### Common Issues

**PySide6 not found:**
```bash
# With uv
uv sync --reinstall

# With pip
pip install --force-reinstall PySide6
```

**Permission errors on Windows:**
Run PowerShell as Administrator or use:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Display issues on Linux:**
Install required system packages:
```bash
sudo apt-get install libegl1-mesa libxkbcommon0 libxcb-cursor0
```

**uv not found after installation:**
Restart your terminal or add to PATH:
```bash
# Linux/macOS
export PATH="$HOME/.cargo/bin:$PATH"

# Windows - restart PowerShell or add to system PATH
```

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [PySide6](https://doc.qt.io/qtforpython/) - Qt for Python
- [Qt](https://www.qt.io/) - Cross-platform framework
- [uv](https://docs.astral.sh/uv/) - Fast Python package manager
