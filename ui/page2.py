import os

from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit,
    QRadioButton, QHBoxLayout, QComboBox, QGroupBox, QFormLayout
)
from PyQt6.QtCore import Qt, QTimer, QDate
from openpyxl import Workbook, load_workbook  # Excel
import getpass


def create_page2(self) -> QWidget:
    page = QWidget()
    # Устанавливаем тёмный фон и белый цвет текста для всей страницы
    page.setStyleSheet("background-color: #121212; color: white;")
    layout = QVBoxLayout(page)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(15)

    def dark_button_style():
        return ("background-color: #333333; color: white; "
                "font-size: 15px; border: 1px solid #555; border-radius: 4px;")

    # Кнопка "Назад"
    btn_back = QPushButton("Назад")
    btn_back.clicked.connect(self.go_to_first_page)
    btn_back.setStyleSheet(dark_button_style())
    btn_back.setMinimumSize(150, 30)
    layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignLeft)

    enter_shortcut = QShortcut(QKeySequence("Escape"), page)
    enter_shortcut.activated.connect(self.go_to_first_page)

    # Текст
    text_label = QLabel("Програма для автоматизации процессов ИБ")
    text_label.setWordWrap(True)
    text_label.setStyleSheet("font-size: 25px; color: white;")
    text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(text_label)


    # Горизонтальный лэйаут для групп
    h_layout = QHBoxLayout()
    h_layout.setSpacing(60)
    layout.addLayout(h_layout)


    # Левая группа (Группа 1)
    left_group = QGroupBox("Группа 1")
    left_group.setStyleSheet("""
        QGroupBox {
            background-color: #1e1e1e;
            border: 1px solid #444;
            border-radius: 5px;
            margin-top: 10px;
            padding: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 3px;
            color: white;
        }
    """)
    left_form = QFormLayout()
    left_form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
    left_group.setLayout(left_form)
    left_form.setContentsMargins(40, 40, 40, 40)
    left_form.setSpacing(30)

    # Кнопка "Лицензии"
    btn_input = QPushButton("Лицензии")
    btn_input.clicked.connect(self.go_to_six_page)
    btn_input.setFixedSize(300, 100)
    btn_input.setStyleSheet(dark_button_style())
    left_form.addRow(btn_input)
    left_form.setAlignment(btn_input, Qt.AlignmentFlag.AlignCenter)

    # Кнопка "СКЗИ"
    btn_input2 = QPushButton("СКЗИ")
    btn_input2.clicked.connect(self.go_to_seven_page)
    btn_input2.setFixedSize(300, 100)
    btn_input2.setStyleSheet(dark_button_style())
    left_form.addRow(btn_input2)
    left_form.setAlignment(btn_input2, Qt.AlignmentFlag.AlignCenter)

    h_layout.addWidget(left_group, 1)

    # Правая группа (Группа 2)
    right_group = QGroupBox("Группа 2")
    right_group.setStyleSheet("""
        QGroupBox {
            background-color: #1e1e1e;
            border: 1px solid #444;
            border-radius: 5px;
            margin-top: 10px;
            padding: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 3px;
            color: white;
        }
    """)
    right_group_layout = QFormLayout()
    right_group_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
    right_group.setLayout(right_group_layout)
    right_group.setContentsMargins(40, 40, 40, 40)
    right_group_layout.setSpacing(30)

    # Кнопка "Ключи УКЭП"
    btn_input3 = QPushButton("Ключи УКЭП")
    btn_input3.clicked.connect(self.go_to_eight_page)
    btn_input3.setFixedSize(300, 100)
    btn_input3.setStyleSheet(dark_button_style())
    right_group_layout.addRow(btn_input3)
    right_group_layout.setAlignment(btn_input3, Qt.AlignmentFlag.AlignCenter)

    # Кнопка "КБР"
    btn_input4 = QPushButton("КБР")
    btn_input4.clicked.connect(self.go_to_nine_page)
    btn_input4.setFixedSize(300, 100)
    btn_input4.setStyleSheet(dark_button_style())
    right_group_layout.addRow(btn_input4)
    right_group_layout.setAlignment(btn_input4, Qt.AlignmentFlag.AlignCenter)

    h_layout.addWidget(right_group, 1)

    # Дополнительная группа (Группа 3)
    extra_group = QGroupBox("Группа 3")
    extra_group.setStyleSheet("""
        QGroupBox {
            background-color: #1e1e1e;
            border: 1px solid #444;
            border-radius: 5px;
            margin-top: 10px;
            padding: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 3px;
            color: white;
        }
    """)
    extra_layout = QFormLayout()
    extra_group.setLayout(extra_layout)
    extra_group.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # Кнопка "TLS"
    btn_input5 = QPushButton("TLS")
    btn_input5.clicked.connect(self.go_to_ten_page)
    btn_input5.setFixedSize(300, 100)
    btn_input5.setStyleSheet(dark_button_style())
    extra_layout.addRow(btn_input5)
    extra_layout.setAlignment(btn_input5, Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(extra_group)



    return page
