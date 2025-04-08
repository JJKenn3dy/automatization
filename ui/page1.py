import getpass
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QSizePolicy,
    QLabel, QPushButton, QVBoxLayout
)
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import sys, os


def create_page1(self) -> QWidget:
    """Создаём первую страницу: текст, несколько кнопок, SVG справа (тёмная тема)."""
    page = QWidget()
    # Задаём общий тёмный фон и белый текст для страницы
    page.setStyleSheet("background-color: #121212; color: white;")
    main_layout = QHBoxLayout(page)
    main_layout.setContentsMargins(50, 40, 50, 40)
    main_layout.setSpacing(15)

    # Левая колонка (текст + несколько кнопок)
    left_layout = QVBoxLayout()

    # Текст приветствия
    welcome_label = QLabel(f"Добро пожаловать {getpass.getuser()}!")
    welcome_label.setWordWrap(True)
    # Можно оставить акцентный цвет, либо поменять на белый/серый
    welcome_label.setStyleSheet("font-size: 30px; color: #c0c0c0;")
    welcome_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    left_layout.addWidget(welcome_label, alignment=Qt.AlignmentFlag.AlignTop)

    # Текст описания программы
    desc_label = QLabel("Програма для автоматизации\nпроцессов ИБ")
    desc_label.setWordWrap(True)
    desc_label.setStyleSheet("font-size: 25px; color: #a0a0a0;")
    desc_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    left_layout.addWidget(desc_label, alignment=Qt.AlignmentFlag.AlignTop)

    # Функция для формирования стиля кнопки в тёмном стиле
    def dark_button_style():
        return ("background-color: #333333; color: white; "
                "font-size: 15px; border: 1px solid #555; border-radius: 4px;")

    # Кнопка "Регистрация"
    btn_to_second = QPushButton("Регистрация")
    btn_to_second.setFixedSize(150, 50)
    btn_to_second.setStyleSheet(dark_button_style())
    btn_to_second.clicked.connect(self.on_toggle)
    btn_to_second.clicked.connect(self.go_to_second_page)
    left_layout.addWidget(btn_to_second, alignment=Qt.AlignmentFlag.AlignLeft)

    # Кнопка "Импорт"
    btn_to_third = QPushButton("Импорт")
    btn_to_third.setFixedSize(150, 50)
    btn_to_third.setStyleSheet(dark_button_style())
    btn_to_third.clicked.connect(self.on_toggle)
    btn_to_third.clicked.connect(self.go_to_11_page)
    left_layout.addWidget(btn_to_third, alignment=Qt.AlignmentFlag.AlignLeft)

    # Кнопка "UNWORK" (четвёртая страница)
    btn_to_fourth = QPushButton("UNWORK")
    btn_to_fourth.setFixedSize(150, 50)
    btn_to_fourth.setStyleSheet(dark_button_style())
    btn_to_fourth.clicked.connect(self.on_toggle)
    btn_to_fourth.clicked.connect(self.go_to_fourth_page)
    left_layout.addWidget(btn_to_fourth, alignment=Qt.AlignmentFlag.AlignLeft)

    # Кнопка "UNWORK" (пятая страница)
    btn_to_five = QPushButton("UNWORK")
    btn_to_five.setFixedSize(150, 50)
    btn_to_five.setStyleSheet(dark_button_style())
    btn_to_five.clicked.connect(self.on_toggle)
    btn_to_five.clicked.connect(self.go_to_five_page)
    left_layout.addWidget(btn_to_five, alignment=Qt.AlignmentFlag.AlignLeft)

    main_layout.addLayout(left_layout)

    # Справа – SVG (например, логотип)
    self.svg_widget = QSvgWidget("logo.svg")
    self.svg_widget.setFixedSize(300, 300)
    self.svg_widget.setAutoFillBackground(True)
    # Можно задать фон для SVG-виджета (если требуется)
    self.svg_widget.setStyleSheet("background-color: transparent;")

    # Обёртка для SVG
    container = QWidget()
    container.setStyleSheet("background-color: transparent;")
    container_layout = QVBoxLayout(container)
    container_layout.setContentsMargins(20, 20, 20, 20)
    container_layout.addWidget(self.svg_widget, alignment=Qt.AlignmentFlag.AlignCenter)
    main_layout.addWidget(container, alignment=Qt.AlignmentFlag.AlignRight)

    return page


def resource_path(relative_path):
    """Возвращает абсолютный путь к ресурсу, работает как в режиме разработки, так и в PyInstaller."""
    try:
        base_path = sys._MEIPASS  # PyInstaller
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
