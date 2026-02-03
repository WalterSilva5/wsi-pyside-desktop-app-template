# Architecture Overview

This document describes the architecture and design patterns used in the PySide6 Desktop Application Template.

## Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Views (UI Layer)                       │
│    MainWindow, Pages, Components                            │
├─────────────────────────────────────────────────────────────┤
│                   Controllers (Logic)                        │
│    HomeController, SettingsController, ShowcaseController   │
├─────────────────────────────────────────────────────────────┤
│                    Services (Business)                       │
│    Navigation, Config, Theme, Logger, Storage               │
├─────────────────────────────────────────────────────────────┤
│                   Models (Data Layer)                        │
│    User, Settings, Repositories                             │
├─────────────────────────────────────────────────────────────┤
│                   Core (Infrastructure)                      │
│    Container, EventBus, Types, Exceptions                   │
└─────────────────────────────────────────────────────────────┘
```

## Design Patterns

### 1. Dependency Injection Container

The DI Container (`src/core/container.py`) manages service lifecycles and dependencies.

```python
from src.core.container import Container, container

# Register services
container.register_singleton(ConfigService)
container.register_transient(UserRepository)
container.register_factory(lambda: SomeService())

# Resolve services
config = container.resolve(ConfigService)
```

**Benefits:**

- Loose coupling between components
- Easy testing with mock services
- Centralized service management

### 2. Observer Pattern (Event Bus)

The EventBus (`src/core/signals.py`) enables decoupled communication using Qt Signals.

```python
from src.core.signals import event_bus
from src.core.types import PageId

# Connect to events
event_bus.navigate_to.connect(self._on_navigate)
event_bus.theme_changed.connect(self._on_theme_change)

# Emit events
event_bus.navigate_to.emit(PageId.SETTINGS)
event_bus.theme_changed.emit(Theme.DARK)
```

**Available Signals:**

- `navigate_to(PageId)` - Navigation requests
- `theme_changed(Theme)` - Theme changes
- `user_logged_in(User)` - User authentication
- `user_logged_out()` - User logout
- `error_occurred(str)` - Error notifications
- `settings_changed(str, object)` - Settings updates

### 3. Factory Pattern

Factories create objects dynamically by name or type.

```python
from src.factories.component_factory import ComponentFactory
from src.factories.page_factory import PageFactory

# Create components
button = ComponentFactory.create("primary_button", text="Click")
card = ComponentFactory.create("info_card", title="Stats")

# Create pages
page = PageFactory.create(PageId.HOME)
```

### 4. Repository Pattern

Repositories abstract data access operations.

```python
from src.models.repositories.user_repository import UserRepository

repo = UserRepository()

# CRUD operations
user = repo.create(User(username="john", email="john@example.com"))
user = repo.get_by_id("user-123")
users = repo.get_all()
repo.update(user)
repo.delete("user-123")

# Custom queries
active_users = repo.find_active()
user = repo.find_by_email("john@example.com")
```

### 5. Singleton Pattern

Services use the singleton pattern for shared state.

```python
from src.services.base import BaseService

class MyService(BaseService):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

## Service Layer

### ConfigService

JSON-based configuration with dot notation access.

```python
config = container.resolve(ConfigService)

# Get values
theme = config.get("theme", "light")
width = config.get("window.width", 800)

# Set values
config.set("theme", "dark")
config.set("user.preferences.notifications", True)

# Save to file
config.save()
```

### NavigationService

Type-safe navigation with history support.

```python
nav = container.resolve(NavigationService)

# Navigate
nav.navigate_to(PageId.SETTINGS)
nav.navigate_to(PageId.HOME, data={"tab": "profile"})

# History
nav.go_back()
nav.clear_history()

# Properties
current = nav.current_page
can_back = nav.can_go_back
```

### ThemeService

Light/Dark theme switching.

```python
theme = container.resolve(ThemeService)

# Switch themes
theme.set_theme(Theme.DARK)
theme.toggle_theme()

# Get current
current = theme.current_theme
is_dark = theme.is_dark
```

### LoggerService

Centralized logging with file rotation.

```python
logger = container.resolve(LoggerService)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.exception("Error with traceback")
```

## View Layer

### BasePage

All pages inherit from `BasePage` with lifecycle hooks.

```python
class MyPage(BasePage):
    def _setup_ui(self) -> None:
        """Build the UI (called once)."""
        pass

    def on_navigate(self, data: dict | None = None) -> None:
        """Called when navigating to this page."""
        pass

    def on_show(self) -> None:
        """Called when page becomes visible."""
        pass

    def on_hide(self) -> None:
        """Called when page is hidden."""
        pass

    def on_destroy(self) -> None:
        """Called when page is destroyed."""
        pass
```

### Component Architecture

Components are self-contained widgets with:

- Clear public API
- Internal state management
- Style encapsulation
- Signal-based communication

```python
class MyComponent(BaseComponent):
    # Signals
    value_changed = Signal(str)

    def __init__(self, initial_value: str = ""):
        super().__init__()
        self._value = initial_value
        self._setup_ui()

    def _setup_ui(self) -> None:
        # Build internal widgets
        pass

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, new_value: str) -> None:
        if self._value != new_value:
            self._value = new_value
            self.value_changed.emit(new_value)
```

## Data Flow

```
User Action
    │
    ▼
View (Page/Component)
    │
    ▼
Controller (Business Logic)
    │
    ├──▶ Service (Config, Navigation, etc.)
    │
    └──▶ Repository (Data Access)
             │
             ▼
         Model (Data)
             │
             ▼
         Storage (JSON Files)
```

## File Organization

```
src/
├── core/           # Infrastructure, no dependencies on other src modules
├── services/       # Depends on core
├── models/         # Depends on core
├── controllers/    # Depends on services, models
├── views/          # Depends on controllers, services
├── factories/      # Depends on views, models
└── utils/          # Standalone utilities
```

## Testing Strategy

### Unit Tests

Test individual components in isolation.

```python
def test_config_get_default():
    config = ConfigService(config_path=temp_file)
    assert config.get("missing", "default") == "default"
```

### Integration Tests

Test component interactions.

```python
def test_navigation_flow():
    nav.navigate_to(PageId.HOME)
    nav.navigate_to(PageId.SETTINGS)
    nav.go_back()
    assert nav.current_page == PageId.HOME
```

### UI Tests

Test visual components with pytest-qt.

```python
def test_button_click(qtbot):
    button = PrimaryButton("Test")
    qtbot.addWidget(button)

    with qtbot.waitSignal(button.clicked):
        qtbot.mouseClick(button, Qt.LeftButton)
```
