from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

class Sidebar(QWidget):
    def __init__(self, parent):
        super().__init__()
        layout = QVBoxLayout()

        btn_home = QPushButton("Home")
        btn_settings = QPushButton("Configurações")

        btn_home.clicked.connect(lambda: parent.main_window.change_page("home"))
        btn_settings.clicked.connect(lambda: parent.main_window.change_page("settings"))

        layout.addWidget(btn_home)
        layout.addWidget(btn_settings)
        self.setLayout(layout)
