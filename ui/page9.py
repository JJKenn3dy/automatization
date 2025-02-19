
from PyQt6.QtWidgets import (
    QWidget,
    QLabel, QPushButton, QVBoxLayout
)

from PyQt6.QtCore import Qt

def create_page9(self) -> QWidget:
    page = QWidget()
    layout = QVBoxLayout(page)
    label = QLabel("Это 9 страница")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    btn_back = QPushButton("Назад")
    btn_back.clicked.connect(self.go_to_second_page)
    layout.addWidget(label)
    layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)
    return page