from PyQt6.QtWidgets import (
    QWidget,
    QLabel, QPushButton, QCalendarWidget, QVBoxLayout, QInputDialog
)
from PyQt6.QtCore import Qt, QTimer, QDate
from PyQt6 import QtWidgets


def create_page3(self) -> QWidget:
    """Страница с календарем для выбора даты."""
    page = QWidget()

    layout = QVBoxLayout(page)
    btn_back = QPushButton("Назад на главную")
    btn_back.clicked.connect(self.go_to_first_page)
    layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)

    title = QLabel("СКЗИ")
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(title)

    # Создаем календарь
    calendar = QCalendarWidget()
    calendar.setGridVisible(True)
    layout.addWidget(calendar)

    # Кнопка для вызова диалога


    # Метка для отображения выбранной даты
    self.cal_label = QLabel()
    self.cal_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.cal_label.setText(calendar.selectedDate().toString())
    layout.addWidget(self.cal_label)

    # При клике обновляем метку
    calendar.clicked.connect(lambda date: self.cal_label.setText(date.toString()))



    return page

