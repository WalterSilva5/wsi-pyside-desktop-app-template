"""Component Factory."""
from __future__ import annotations
from typing import Type, Any
from PySide6.QtWidgets import QWidget


class ComponentFactory:
    """Factory for creating UI components."""

    _components: dict[str, Type[QWidget]] = {}

    @classmethod
    def register(cls, name: str, component_class: Type[QWidget]) -> None:
        """Register a component class."""
        cls._components[name] = component_class

    @classmethod
    def create(cls, name: str, **kwargs: Any) -> QWidget:
        """Create a component by name."""
        if name not in cls._components:
            raise ValueError(f"Component '{name}' not registered")
        return cls._components[name](**kwargs)

    @classmethod
    def get_registered(cls) -> list[str]:
        """Get list of registered components."""
        return list(cls._components.keys())

    @classmethod
    def is_registered(cls, name: str) -> bool:
        """Check if a component is registered."""
        return name in cls._components


def register_default_components() -> None:
    """Register all default components."""
    from src.views.components.buttons.primary_button import PrimaryButton
    from src.views.components.buttons.secondary_button import SecondaryButton
    from src.views.components.buttons.icon_button import IconButton
    from src.views.components.buttons.toggle_button import ToggleButton
    from src.views.components.cards.basic_card import BasicCard
    from src.views.components.cards.info_card import InfoCard
    from src.views.components.cards.action_card import ActionCard
    from src.views.components.forms.text_input import TextInput
    from src.views.components.forms.select_input import SelectInput
    from src.views.components.forms.checkbox import Checkbox
    from src.views.components.feedback.badge import Badge
    from src.views.components.feedback.progress_bar import ProgressBar

    ComponentFactory.register("primary_button", PrimaryButton)
    ComponentFactory.register("secondary_button", SecondaryButton)
    ComponentFactory.register("icon_button", IconButton)
    ComponentFactory.register("toggle_button", ToggleButton)
    ComponentFactory.register("basic_card", BasicCard)
    ComponentFactory.register("info_card", InfoCard)
    ComponentFactory.register("action_card", ActionCard)
    ComponentFactory.register("text_input", TextInput)
    ComponentFactory.register("select_input", SelectInput)
    ComponentFactory.register("checkbox", Checkbox)
    ComponentFactory.register("badge", Badge)
    ComponentFactory.register("progress_bar", ProgressBar)
