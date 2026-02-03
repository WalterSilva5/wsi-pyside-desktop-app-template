# Component Library

This document provides detailed documentation for all reusable components in the template.

## Buttons

### PrimaryButton

Main action button with prominent styling.

```python
from src.views.components.buttons import PrimaryButton

button = PrimaryButton("Save Changes")
button.clicked.connect(self._on_save)

# With icon
button = PrimaryButton("Save", icon="save.svg")

# Disabled state
button.setEnabled(False)
```

### SecondaryButton

Secondary action button with subtle styling.

```python
from src.views.components.buttons import SecondaryButton

button = SecondaryButton("Cancel")
button.clicked.connect(self._on_cancel)
```

### IconButton

Button displaying only an icon.

```python
from src.views.components.buttons import IconButton

button = IconButton("settings.svg", tooltip="Settings")
button.clicked.connect(self._open_settings)

# Different sizes
button = IconButton("icon.svg", size=ButtonSize.SMALL)
button = IconButton("icon.svg", size=ButtonSize.LARGE)
```

### ToggleButton

On/off toggle button.

```python
from src.views.components.buttons import ToggleButton

toggle = ToggleButton("Dark Mode", checked=False)
toggle.toggled.connect(self._on_toggle)

# Check state
is_on = toggle.isChecked()
toggle.setChecked(True)
```

## Cards

### BasicCard

Simple card container for content.

```python
from src.views.components.cards import BasicCard

card = BasicCard(title="User Profile")
card.set_content(profile_widget)

# Without title
card = BasicCard()
card.set_content(content_widget)
```

### InfoCard

Card displaying a metric or statistic.

```python
from src.views.components.cards import InfoCard

card = InfoCard(
    title="Total Users",
    value="1,234",
    description="Active this month",
    icon="users.svg"
)

# Update value
card.set_value("1,456")
```

### ActionCard

Card with action buttons.

```python
from src.views.components.cards import ActionCard

card = ActionCard(
    title="Export Data",
    description="Download your data in various formats",
    actions=[
        ("CSV", self._export_csv),
        ("JSON", self._export_json),
        ("Excel", self._export_excel)
    ]
)
```

## Forms

### TextInput

Text input field with validation.

```python
from src.views.components.forms import TextInput

# Basic input
input_field = TextInput(
    label="Username",
    placeholder="Enter username"
)

# With validation
email_input = TextInput(
    label="Email",
    placeholder="email@example.com",
    validator=lambda x: "@" in x,
    error_message="Invalid email format"
)

# Password input
password_input = TextInput(
    label="Password",
    placeholder="Enter password",
    password=True
)

# Get/set value
value = input_field.value
input_field.value = "new value"

# Signals
input_field.value_changed.connect(self._on_change)
input_field.validation_changed.connect(self._on_validation)
```

### SelectInput

Dropdown selection component.

```python
from src.views.components.forms import SelectInput

select = SelectInput(
    label="Country",
    options=[
        ("us", "United States"),
        ("uk", "United Kingdom"),
        ("br", "Brazil")
    ],
    placeholder="Select a country"
)

# Get selected value
value = select.value  # Returns "us", "uk", etc.

# Set value
select.value = "br"

# Signal
select.value_changed.connect(self._on_country_change)
```

### Checkbox

Checkbox with label.

```python
from src.views.components.forms import Checkbox

checkbox = Checkbox(
    label="I agree to the terms",
    checked=False
)

# Get/set state
is_checked = checkbox.checked
checkbox.checked = True

# Signal
checkbox.toggled.connect(self._on_agree)
```

### RadioGroup

Group of radio buttons.

```python
from src.views.components.forms import RadioGroup

radio_group = RadioGroup(
    label="Payment Method",
    options=[
        ("card", "Credit Card"),
        ("paypal", "PayPal"),
        ("bank", "Bank Transfer")
    ],
    selected="card"
)

# Get selected
selected = radio_group.value

# Signal
radio_group.value_changed.connect(self._on_payment_change)
```

### FormField

Generic form field wrapper for custom content.

```python
from src.views.components.forms import FormField

field = FormField(
    label="Custom Field",
    widget=my_custom_widget,
    required=True,
    help_text="Enter your custom value"
)

# Show error
field.set_error("This field is required")

# Clear error
field.clear_error()
```

## Dialogs

### ConfirmDialog

Yes/No confirmation dialog.

```python
from src.views.components.dialogs import ConfirmDialog

dialog = ConfirmDialog(
    title="Delete Item",
    message="Are you sure you want to delete this item?",
    confirm_text="Delete",
    cancel_text="Cancel"
)

if dialog.exec() == ConfirmDialog.Accepted:
    self._delete_item()
```

### AlertDialog

Information alert dialog.

```python
from src.views.components.dialogs import AlertDialog

# Info alert
AlertDialog.info(
    title="Success",
    message="Your changes have been saved."
)

# Warning alert
AlertDialog.warning(
    title="Warning",
    message="This action cannot be undone."
)

# Error alert
AlertDialog.error(
    title="Error",
    message="An error occurred while saving."
)
```

### FormDialog

Dialog containing a form.

```python
from src.views.components.dialogs import FormDialog

dialog = FormDialog(
    title="Add User",
    fields=[
        {"name": "username", "label": "Username", "type": "text", "required": True},
        {"name": "email", "label": "Email", "type": "email", "required": True},
        {"name": "role", "label": "Role", "type": "select", "options": [
            ("admin", "Administrator"),
            ("user", "User")
        ]}
    ]
)

if dialog.exec() == FormDialog.Accepted:
    data = dialog.get_data()
    # {"username": "john", "email": "john@example.com", "role": "user"}
```

## Feedback

### Badge

Status badge for labels and counts.

```python
from src.views.components.feedback import Badge

# Status badge
badge = Badge(text="Active", variant="success")
badge = Badge(text="Pending", variant="warning")
badge = Badge(text="Error", variant="error")
badge = Badge(text="Info", variant="info")

# Count badge
badge = Badge(text="5", variant="primary")
```

### ProgressBar

Progress indicator.

```python
from src.views.components.feedback import ProgressBar

progress = ProgressBar(value=0, maximum=100)

# Update progress
progress.set_value(50)

# Indeterminate mode
progress.set_indeterminate(True)

# With label
progress = ProgressBar(value=75, show_label=True)
# Shows "75%"
```

### Spinner

Loading spinner.

```python
from src.views.components.feedback import Spinner

spinner = Spinner(size=32)

# Show/hide
spinner.start()
spinner.stop()

# With text
spinner = Spinner(text="Loading...")
```

### Toast

Notification toast message.

```python
from src.views.components.feedback import Toast

# Show toast (auto-dismisses)
Toast.show(
    message="Item saved successfully",
    variant="success",
    duration=3000  # milliseconds
)

# Variants
Toast.show("Info message", variant="info")
Toast.show("Warning message", variant="warning")
Toast.show("Error message", variant="error")
```

### Tooltip

Hover tooltip.

```python
from src.views.components.feedback import Tooltip

# Add tooltip to any widget
Tooltip.set(button, "Click to save changes")

# Custom position
Tooltip.set(widget, "Help text", position="bottom")
```

## Tables

### DataTable

Full-featured data table.

```python
from src.views.components.tables import DataTable

table = DataTable(
    columns=[
        {"key": "name", "label": "Name", "sortable": True},
        {"key": "email", "label": "Email", "sortable": True},
        {"key": "status", "label": "Status", "width": 100}
    ]
)

# Set data
table.set_data([
    {"name": "John", "email": "john@example.com", "status": "Active"},
    {"name": "Jane", "email": "jane@example.com", "status": "Inactive"}
])

# Signals
table.row_clicked.connect(self._on_row_click)
table.row_double_clicked.connect(self._on_row_double_click)
table.selection_changed.connect(self._on_selection_change)

# Selection
selected = table.get_selected_rows()
table.select_row(0)
table.clear_selection()

# Pagination
table.set_page_size(25)
table.next_page()
table.previous_page()
```

### ListView

Vertical list view.

```python
from src.views.components.tables import ListView

list_view = ListView()

# Add items
list_view.add_item("Item 1", data={"id": 1})
list_view.add_item("Item 2", data={"id": 2})

# With custom widget
list_view.add_item(custom_widget)

# Signals
list_view.item_clicked.connect(self._on_item_click)
list_view.item_selected.connect(self._on_item_select)
```

### TreeView

Hierarchical tree view.

```python
from src.views.components.tables import TreeView

tree = TreeView()

# Build tree
root = tree.add_item("Root")
child1 = tree.add_item("Child 1", parent=root)
child2 = tree.add_item("Child 2", parent=root)
grandchild = tree.add_item("Grandchild", parent=child1)

# Expand/collapse
tree.expand_all()
tree.collapse_all()
tree.expand_item(root)

# Signals
tree.item_clicked.connect(self._on_tree_click)
tree.item_expanded.connect(self._on_expand)
```

## Layout

### Header

Application header component.

```python
from src.views.components.layout import Header

header = Header(
    title="My Application",
    show_back_button=True,
    actions=[
        ("Settings", "settings.svg", self._open_settings),
        ("Help", "help.svg", self._open_help)
    ]
)

# Update title
header.set_title("New Title")

# Show/hide back button
header.set_back_visible(False)
```

### Sidebar

Navigation sidebar.

```python
from src.views.components.layout import Sidebar

sidebar = Sidebar(
    items=[
        {"id": PageId.HOME, "label": "Home", "icon": "home.svg"},
        {"id": PageId.SETTINGS, "label": "Settings", "icon": "settings.svg"},
        {"id": PageId.SHOWCASE, "label": "Components", "icon": "components.svg"}
    ]
)

# Signals
sidebar.item_clicked.connect(self._on_nav_item_click)

# Set active
sidebar.set_active(PageId.HOME)

# Collapse/expand
sidebar.collapse()
sidebar.expand()
```

### Footer

Application footer.

```python
from src.views.components.layout import Footer

footer = Footer(
    text="Version 1.0.0",
    links=[
        ("Documentation", self._open_docs),
        ("Support", self._open_support)
    ]
)
```

### ContentArea

Main content wrapper with optional padding and scroll.

```python
from src.views.components.layout import ContentArea

content = ContentArea(
    padding=20,
    scrollable=True
)

content.set_content(page_widget)
```

## Creating Custom Components

Extend `BaseComponent` for consistent behavior:

```python
from src.views.components.base import BaseComponent
from PySide6.QtCore import Signal

class MyCustomComponent(BaseComponent):
    # Define signals
    value_changed = Signal(str)

    def __init__(self, initial_value: str = "", parent=None):
        super().__init__(parent)
        self._value = initial_value
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Build the component UI."""
        layout = QVBoxLayout(self)
        # Add widgets...

    @property
    def value(self) -> str:
        """Get current value."""
        return self._value

    @value.setter
    def value(self, new_value: str) -> None:
        """Set current value."""
        if self._value != new_value:
            self._value = new_value
            self._update_ui()
            self.value_changed.emit(new_value)

    def _update_ui(self) -> None:
        """Update UI to reflect current state."""
        pass
```
