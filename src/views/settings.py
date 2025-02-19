from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from src.views.components.header import Header
from src.views.components.sidebar import Sidebar

class SettingsPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout()

        self.header = Header("Configurações")
        self.sidebar = Sidebar(self)

        layout.addWidget(self.header)
        layout.addWidget(QLabel("Página de Configurações"))
        btn = QPushButton("Voltar para Home")
        btn.clicked.connect(lambda: self.main_window.change_page("home"))

        layout.addWidget(btn)
        layout.addWidget(self.sidebar)

        self.setLayout(layout)
