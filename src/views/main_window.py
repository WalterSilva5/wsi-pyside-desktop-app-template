from PySide6.QtWidgets import QMainWindow, QStackedWidget
from src.views.home import HomePage
from src.views.settings import SettingsPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Meu Aplicativo PySide6")
        self.setGeometry(100, 100, 800, 600)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Instância das telas
        self.home_page = HomePage(self)
        self.settings_page = SettingsPage(self)

        # Adicionando telas ao Stack
        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.settings_page)

        # Definindo tela inicial
        self.stack.setCurrentWidget(self.home_page)

    def change_page(self, page):
        if page == "settings":
            self.stack.setCurrentWidget(self.settings_page)
        else:
            self.stack.setCurrentWidget(self.home_page)
