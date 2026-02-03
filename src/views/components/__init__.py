"""
Reusable UI components module.

Contains all reusable UI components organized by category:
- layout: Header, Sidebar, Footer, ContentArea
- buttons: Primary, Secondary, Icon, Toggle
- cards: Basic, Info, Action
- forms: TextInput, Select, Checkbox, RadioGroup
- dialogs: Confirm, Alert, Form
- tables: DataTable, ListView, TreeView
- feedback: Badge, Toast, Progress, Spinner
- icons: Icon wrapper
"""

from src.views.components.base import BaseComponent

__all__ = [
    "BaseComponent",
]
