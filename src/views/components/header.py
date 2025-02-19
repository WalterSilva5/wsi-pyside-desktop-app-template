from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout

class Header(QWidget):
    def __init__(self, title):
        super().__init__()
        layout = QHBoxLayout()
        layout.addWidget(QLabel(f"<h2>{title}</h2>"))
        self.setLayout(layout)
