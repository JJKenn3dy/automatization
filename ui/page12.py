from PyQt6.QtWidgets import (
    QWidget,
    QLabel, QPushButton, QVBoxLayout
)

from PyQt6.QtCore import Qt

def create_page12(self) -> QWidget:
    page = QWidget()
    layout = QVBoxLayout(page)
    label = QLabel("Это 12 страница")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    btn_back = QPushButton("Назад на главную.")
    btn_back.clicked.connect(self.go_to_first_page)
    layout.addWidget(label)
    layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)
    return page