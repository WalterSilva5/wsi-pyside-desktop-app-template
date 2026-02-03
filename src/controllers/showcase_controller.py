"""
Component showcase controller.

Handles business logic for the component showcase page.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from PySide6.QtCore import Signal

from src.controllers.base import BaseController


@dataclass
class ComponentInfo:
    """Information about a component."""
    name: str
    category: str
    description: str
    props: list[dict[str, str]]
    example_code: str


class ShowcaseController(BaseController):
    """
    Controller for the component showcase page.

    Handles:
    - Component catalog management
    - Example data for demonstrations
    - Component search and filtering
    """

    # Signals
    components_loaded = Signal(list)
    component_selected = Signal(object)

    def __init__(self) -> None:
        """Initialize the showcase controller."""
        super().__init__()
        self._components: list[ComponentInfo] = []
        self._selected_component: ComponentInfo | None = None
        self._load_component_catalog()

    def _load_component_catalog(self) -> None:
        """Load the component catalog."""
        self._components = [
            ComponentInfo(
                name="PrimaryButton",
                category="buttons",
                description="Primary action button for main actions",
                props=[
                    {"name": "text", "type": "str", "description": "Button label"},
                    {"name": "size", "type": "ButtonSize", "description": "small, medium, large"},
                    {"name": "disabled", "type": "bool", "description": "Disable the button"},
                ],
                example_code='button = PrimaryButton(text="Click me")',
            ),
            ComponentInfo(
                name="SecondaryButton",
                category="buttons",
                description="Secondary button for less prominent actions",
                props=[
                    {"name": "text", "type": "str", "description": "Button label"},
                    {"name": "size", "type": "ButtonSize", "description": "small, medium, large"},
                ],
                example_code='button = SecondaryButton(text="Cancel")',
            ),
            ComponentInfo(
                name="IconButton",
                category="buttons",
                description="Button with icon only",
                props=[
                    {"name": "icon", "type": "QIcon", "description": "Button icon"},
                    {"name": "tooltip", "type": "str", "description": "Tooltip text"},
                ],
                example_code='button = IconButton(icon=my_icon, tooltip="Delete")',
            ),
            ComponentInfo(
                name="ToggleButton",
                category="buttons",
                description="Toggle button with on/off states",
                props=[
                    {"name": "text", "type": "str", "description": "Button label"},
                    {"name": "checked", "type": "bool", "description": "Initial state"},
                ],
                example_code='toggle = ToggleButton(text="Dark Mode")',
            ),
            ComponentInfo(
                name="BasicCard",
                category="cards",
                description="Basic card container for content grouping",
                props=[
                    {"name": "title", "type": "str", "description": "Card title"},
                    {"name": "subtitle", "type": "str", "description": "Optional subtitle"},
                    {"name": "elevation", "type": "int", "description": "Shadow level (0-4)"},
                ],
                example_code='card = BasicCard(title="Profile", elevation=2)',
            ),
            ComponentInfo(
                name="InfoCard",
                category="cards",
                description="Card for displaying information with icon",
                props=[
                    {"name": "title", "type": "str", "description": "Card title"},
                    {"name": "value", "type": "str", "description": "Main value"},
                    {"name": "color", "type": "str", "description": "Accent color"},
                ],
                example_code='card = InfoCard(title="Users", value="1,234")',
            ),
            ComponentInfo(
                name="ActionCard",
                category="cards",
                description="Card with action buttons",
                props=[
                    {"name": "title", "type": "str", "description": "Card title"},
                    {"name": "actions", "type": "list", "description": "Action buttons"},
                ],
                example_code='card = ActionCard(title="Settings", actions=[...])',
            ),
            ComponentInfo(
                name="TextInput",
                category="forms",
                description="Text input field with label and validation",
                props=[
                    {"name": "label", "type": "str", "description": "Field label"},
                    {"name": "placeholder", "type": "str", "description": "Placeholder"},
                    {"name": "required", "type": "bool", "description": "Required field"},
                ],
                example_code='input_field = TextInput(label="Email", required=True)',
            ),
            ComponentInfo(
                name="SelectInput",
                category="forms",
                description="Dropdown select input",
                props=[
                    {"name": "label", "type": "str", "description": "Field label"},
                    {"name": "options", "type": "list", "description": "Options list"},
                ],
                example_code='select = SelectInput(label="Country", options=[...])',
            ),
            ComponentInfo(
                name="Checkbox",
                category="forms",
                description="Checkbox input with label",
                props=[
                    {"name": "label", "type": "str", "description": "Checkbox label"},
                    {"name": "checked", "type": "bool", "description": "Checked state"},
                ],
                example_code='checkbox = Checkbox(label="I agree")',
            ),
            ComponentInfo(
                name="ConfirmDialog",
                category="dialogs",
                description="Confirmation dialog for important actions",
                props=[
                    {"name": "title", "type": "str", "description": "Dialog title"},
                    {"name": "message", "type": "str", "description": "Message"},
                ],
                example_code='dialog = ConfirmDialog(title="Delete?")',
            ),
            ComponentInfo(
                name="AlertDialog",
                category="dialogs",
                description="Alert dialog for notifications",
                props=[
                    {"name": "title", "type": "str", "description": "Dialog title"},
                    {"name": "alert_type", "type": "str", "description": "info/warning/error"},
                ],
                example_code='AlertDialog.show_error(title="Error", message="Failed")',
            ),
            ComponentInfo(
                name="Badge",
                category="feedback",
                description="Badge for status indicators",
                props=[
                    {"name": "text", "type": "str", "description": "Badge text"},
                    {"name": "variant", "type": "str", "description": "Variant style"},
                ],
                example_code='badge = Badge(text="New", variant="primary")',
            ),
            ComponentInfo(
                name="ProgressBar",
                category="feedback",
                description="Progress indicator",
                props=[
                    {"name": "value", "type": "int", "description": "Progress (0-100)"},
                    {"name": "show_text", "type": "bool", "description": "Show percentage"},
                ],
                example_code='progress = ProgressBar(value=75)',
            ),
            ComponentInfo(
                name="Spinner",
                category="feedback",
                description="Loading spinner",
                props=[
                    {"name": "size", "type": "int", "description": "Spinner size"},
                ],
                example_code='spinner = Spinner(size=32)',
            ),
            ComponentInfo(
                name="Toast",
                category="feedback",
                description="Toast notification",
                props=[
                    {"name": "message", "type": "str", "description": "Toast message"},
                    {"name": "toast_type", "type": "str", "description": "Notification type"},
                ],
                example_code='Toast.show(message="Saved!", toast_type="success")',
            ),
            ComponentInfo(
                name="DataTable",
                category="tables",
                description="Data table with sorting and pagination",
                props=[
                    {"name": "columns", "type": "list", "description": "Column definitions"},
                    {"name": "data", "type": "list", "description": "Table data"},
                    {"name": "sortable", "type": "bool", "description": "Enable sorting"},
                ],
                example_code='table = DataTable(columns=[...], data=[...], sortable=True)',
            ),
        ]

    def get_all_components(self) -> list[ComponentInfo]:
        """Get all components."""
        return self._components

    def get_categories(self) -> list[str]:
        """Get list of unique categories."""
        return list(set(c.category for c in self._components))

    def get_components_by_category(self, category: str) -> list[ComponentInfo]:
        """Get components filtered by category."""
        return [c for c in self._components if c.category == category]

    def search_components(self, query: str) -> list[ComponentInfo]:
        """Search components by name or description."""
        query_lower = query.lower()
        return [
            c for c in self._components
            if query_lower in c.name.lower() or query_lower in c.description.lower()
        ]

    def select_component(self, name: str) -> ComponentInfo | None:
        """Select a component by name."""
        for component in self._components:
            if component.name == name:
                self._selected_component = component
                self.component_selected.emit(component)
                return component
        return None

    def get_selected_component(self) -> ComponentInfo | None:
        """Get the currently selected component."""
        return self._selected_component

    def get_example_data(self, component_name: str) -> dict[str, Any]:
        """Get example data for a component."""
        examples = {
            "DataTable": {
                "columns": [{"key": "name", "label": "Name"}, {"key": "email", "label": "Email"}],
                "data": [{"name": "John Doe", "email": "john@example.com"}],
            },
            "SelectInput": {
                "options": [{"value": "opt1", "label": "Option 1"}, {"value": "opt2", "label": "Option 2"}],
            },
        }
        return examples.get(component_name, {})
