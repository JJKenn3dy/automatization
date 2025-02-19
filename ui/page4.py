
from PyQt6.QtWidgets import (
    QWidget,
    QLabel, QPushButton, QVBoxLayout
)
from PyQt6.QtCore import Qt

def create_page4(self) -> QWidget:
    page = QWidget()
    layout = QVBoxLayout(page)

    btn_input = QPushButton("Ввести имя")
    btn_input.clicked.connect(self.show_name_dialog)
    layout.addWidget(btn_input)

    btn_back = QPushButton("Назад на главную.")
    btn_back.clicked.connect(self.go_to_first_page)
    layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)
    return page