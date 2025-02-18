import getpass
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QSizePolicy,
    QLabel, QPushButton, QVBoxLayout
)
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtCore import Qt


def create_page1(self) -> QWidget:
    """Создаём первую страницу: текст, несколько кнопок, SVG справа."""
    page = QWidget()
    main_layout = QHBoxLayout(page)
    main_layout.setContentsMargins(50, 40, 50, 40)

    # Левая колонка (текст + несколько кнопок)
    left_layout = QVBoxLayout()

    # Текст
    text_label = QLabel(f"Добро пожаловать {getpass.getuser()}!")
    text_label.setWordWrap(True)
    text_label.setStyleSheet("font-size: 30px; color: #62961e;")
    # Растягиваем текст по вертикали при необходимости
    text_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    left_layout.addWidget(text_label, alignment=Qt.AlignmentFlag.AlignTop)

    # Текст
    text_label = QLabel("Програма для автоматизации\nпроцессов ИБ")
    text_label.setWordWrap(True)
    text_label.setStyleSheet("font-size: 25px; color: #76787A;")
    # Растягиваем текст по вертикали при необходимости
    text_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    left_layout.addWidget(text_label, alignment=Qt.AlignmentFlag.AlignTop)

    # Добавим несколько кнопок
    btn_to_second = QPushButton(f"Регистрация")
    btn_to_second.clicked.connect(self.on_toggle)
    btn_to_second.setFixedSize(150, 50)
    btn_to_second.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    btn_to_second.clicked.connect(self.go_to_second_page)
    left_layout.addWidget(btn_to_second, alignment=Qt.AlignmentFlag.AlignLeft)

    btn_to_third = QPushButton(f"СКЗИ")
    btn_to_third.clicked.connect(self.on_toggle)
    btn_to_third.setFixedSize(150, 50)
    btn_to_third.clicked.connect(self.go_to_third_page)
    btn_to_third.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    left_layout.addWidget(btn_to_third, alignment=Qt.AlignmentFlag.AlignLeft)

    btn_to_fourth = QPushButton(f"Страница 3")
    btn_to_fourth.clicked.connect(self.on_toggle)
    btn_to_fourth.setFixedSize(150, 50)
    btn_to_fourth.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    btn_to_fourth.clicked.connect(self.go_to_fourth_page)
    left_layout.addWidget(btn_to_fourth, alignment=Qt.AlignmentFlag.AlignLeft)

    btn_to_five = QPushButton(f"Страница 4")
    btn_to_five.clicked.connect(self.on_toggle)
    btn_to_five.setFixedSize(150, 50)
    btn_to_five.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    btn_to_five.clicked.connect(self.go_to_five_page)
    left_layout.addWidget(btn_to_five, alignment=Qt.AlignmentFlag.AlignLeft)
    main_layout.addLayout(left_layout)

    # Справа – SVG
    self.svg_widget = QSvgWidget("logo.svg")
    self.svg_widget.setFixedSize(300, 300)
    self.svg_widget.setAutoFillBackground(True)

    # Обёртка для SVG
    container = QWidget()
    container_layout = QVBoxLayout(container)
    container_layout.setContentsMargins(20, 20, 20, 20)
    container_layout.addWidget(self.svg_widget, alignment=Qt.AlignmentFlag.AlignCenter)
    main_layout.addWidget(container, alignment=Qt.AlignmentFlag.AlignRight)

    return page