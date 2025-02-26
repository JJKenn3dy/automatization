from PyQt6.QtWidgets import (
    QWidget,
    QLabel, QPushButton, QVBoxLayout, QLineEdit, QSizePolicy, QRadioButton, QGridLayout, QHBoxLayout, QStyleOption
)

from PyQt6.QtCore import Qt, QRect
from PyQt6.uic.properties import QtCore


def create_page6(self) -> QWidget:
    page = QWidget()
    layout = QVBoxLayout(page)
    layout.setContentsMargins(150, 140, 150, 140)
    text_label = QLabel("Лицензии")
    text_label.setWordWrap(True)
    text_label.setStyleSheet("font-size: 25px; color: #76787A;")
    # Растягиваем текст по вертикали при необходимости
    text_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    layout.addWidget(text_label, alignment=Qt.AlignmentFlag.AlignCenter)
    layout.setContentsMargins(150, 140, 150, 140)
    text_label = QLabel("Введите ФИО:")
    text_label.setWordWrap(True)
    text_label.setStyleSheet("font-size: 20px;")
    # Растягиваем текст по вертикали при необходимости
    text_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    layout.addWidget(text_label, alignment=Qt.AlignmentFlag.AlignCenter)

    self.input_field = QLineEdit(self)

    self.input_field.setPlaceholderText("Введите ФИО: ")
    self.input_field.setFixedSize(550, 50)
    self.input_field.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    layout.addWidget(self.input_field, alignment=Qt.AlignmentFlag.AlignCenter)
    layout.setContentsMargins(250, 240, 250, 240)
    self.submit_button = QPushButton("ОК")
    self.submit_button.setFixedSize(110, 40)
    self.submit_button.clicked.connect(self.getandgo)
    self.label = QLabel("")
    layout.addWidget(self.submit_button, alignment=Qt.AlignmentFlag.AlignCenter)
    btn_back = QPushButton("Назад")
    btn_back.clicked.connect(self.go_to_license_2)
    layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)
    return page


def license2(self) -> QWidget:
    page = QWidget()
    layout = QVBoxLayout(page)
    layout.setContentsMargins(150, 140, 150, 140)

    text_label = QLabel(f"Лицензии")
    text_label.setWordWrap(True)
    text_label.setStyleSheet("font-size: 25px; color: #76787A;")
    text_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    layout.addWidget(text_label, alignment=Qt.AlignmentFlag.AlignCenter)

    # Создаем два вертикальных лэйаута для двух колонок
    left_layout = QVBoxLayout()
    right_layout = QVBoxLayout()

    style_sheet = """
    QRadioButton {
        font-size: 18px;
        color: rgb(118, 120, 122);  /* Серый */
        padding: 10px;
    }
    QRadioButton:checked {
        color: rgb(139, 197, 64);   /* Зеленый */
    }
    QRadioButton::indicator {
        width: 25px;
        height: 25px;
    }
    """
    # Кнопки для левой колонки
    rb1 = QRadioButton("1. Вариант")
    rb1.setStyleSheet(style_sheet)
    rb2 = QRadioButton("2. Вариант")
    rb2.setStyleSheet(style_sheet)
    rb3 = QRadioButton("3. Вариант")
    rb3.setStyleSheet(style_sheet)

    left_layout.addWidget(rb1)
    left_layout.addWidget(rb2)
    left_layout.addWidget(rb3)
    left_layout.setContentsMargins(200, 0, 200, 0)

    # Кнопки для правой колонки
    rb4 = QRadioButton("4. Вариант")
    rb4.setStyleSheet(style_sheet)
    rb5 = QRadioButton("5. Вариант")
    rb5.setStyleSheet(style_sheet)
    rb6 = QRadioButton("6. Вариант")
    rb6.setStyleSheet(style_sheet)
    right_layout.addWidget(rb4)
    right_layout.addWidget(rb5)
    right_layout.addWidget(rb6)
    right_layout.setContentsMargins(200, 0, 200, 0)
    self.result_label = QLabel('', self)

    self.selected_option = None  # Переменная для хранения выбора
    rb1.toggled.connect(self.on_radio_selected)
    rb2.toggled.connect(self.on_radio_selected)
    rb3.toggled.connect(self.on_radio_selected)
    rb4.toggled.connect(self.on_radio_selected)
    rb5.toggled.connect(self.on_radio_selected)
    rb6.toggled.connect(self.on_radio_selected)


    # Объединяем два вертикальных лэйаута в горизонтальный
    h_layout = QHBoxLayout()
    h_layout.addLayout(left_layout)
    h_layout.addLayout(right_layout)

    # Добавляем горизонтальный лэйаут в основной вертикальный лэйаут
    layout.addLayout(h_layout)

    # Кнопка подтверждения выбора
    ok_button = QPushButton("OK")
    ok_button.clicked.connect(self.getandgo2)
    layout.addWidget(ok_button, alignment=Qt.AlignmentFlag.AlignCenter)

    btn_back = QPushButton("Назад")
    btn_back.clicked.connect(self.go_to_six_page)
    layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)

    return page

def license3(self) -> QWidget:
    page = QWidget()
    layout = QVBoxLayout(page)
    layout.setContentsMargins(150, 140, 150, 140)
    text_label = QLabel("Лицензии")
    text_label.setWordWrap(True)
    text_label.setStyleSheet("font-size: 25px; color: #76787A;")
    text_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    layout.addWidget(text_label, alignment=Qt.AlignmentFlag.AlignCenter)

    self.pdf_check()

    btn_back = QPushButton("Назад")
    btn_back.clicked.connect(self.go_to_license_2)
    layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)
    return page


def create_page11(self) -> QWidget:
    page = QWidget()
    layout = QVBoxLayout(page)
    layout.setContentsMargins(150, 140, 150, 140)
    text_label = QLabel("Лицензии")
    text_label.setWordWrap(True)
    text_label.setStyleSheet("font-size: 25px; color: #76787A;")
    text_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    layout.addWidget(text_label, alignment=Qt.AlignmentFlag.AlignCenter)

    btn_back = QPushButton("Назад")
    btn_back.clicked.connect(self.go_to_second_page)
    layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)
    return page