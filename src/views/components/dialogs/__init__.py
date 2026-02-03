"""
Dialog components module.

Contains modal/dialog components:
- BaseDialog
- ConfirmDialog
- AlertDialog
- FormDialog
"""

from src.views.components.dialogs.base_dialog import BaseDialog
from src.views.components.dialogs.confirm_dialog import ConfirmDialog
from src.views.components.dialogs.alert_dialog import AlertDialog
from src.views.components.dialogs.form_dialog import FormDialog

__all__ = [
    "BaseDialog",
    "ConfirmDialog",
    "AlertDialog",
    "FormDialog",
]
