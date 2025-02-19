from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from src.views.components.header import Header
from src.views.components.sidebar import Sidebar

class HomePage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout()

        # Componentes reutilizáveis
        self.header = Header("Página Inicial")
        self.sidebar = Sidebar(self)

        layout.addWidget(self.header)
        layout.addWidget(QLabel("Bem-vindo à Página Inicial!"))
        btn = QPushButton("Ir para Configurações")
        btn.clicked.connect(lambda: self.main_window.change_page("settings"))

        layout.addWidget(btn)
        layout.addWidget(self.sidebar)

        self.setLayout(layout)
