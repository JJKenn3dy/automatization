from datetime import datetime
import getpass

from PyQt6 import QtWidgets
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtWidgets import (
    QWidget,
    QLabel, QPushButton, QVBoxLayout, QRadioButton, QLineEdit, QHBoxLayout, QComboBox, QSizePolicy
)

from PyQt6.QtCore import Qt

def create_page9(self) -> QWidget:
    page = QWidget()
    layout = QVBoxLayout(page)

    # Заголовок
    text_label = QLabel("КБР")
    text_label.setWordWrap(True)
    text_label.setStyleSheet("font-size: 20px; color: #76787A;")
    text_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    layout.addWidget(text_label, alignment=Qt.AlignmentFlag.AlignCenter)

    # --- ЛЕВЫЙ БЛОК ---
    left_layout = QVBoxLayout()

    # ФИО пользователя
    self.input_fio_user = QLineEdit(self)
    self.input_fio_user.setPlaceholderText("Заявка/номер обращения: ")
    self.input_fio_user.setMinimumSize(250, 40)
    self.input_fio_user.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    left_layout.addWidget(self.input_fio_user)

    # Наименование ПО СКЗИ
    combobox = QComboBox(self)
    combobox.setEditable(True)
    combobox.setCurrentText("Тип носителя")
    combobox.addItem("Да")
    combobox.addItem("Нет")
    left_layout.addWidget(combobox)

    # Наименование ПО СКЗИ
    combobox = QComboBox(self)
    combobox.setEditable(True)
    combobox.setCurrentText("Носитель (Серийный номер)")
    combobox.addItem("Option 1")
    combobox.addItem("Option 2")
    combobox.addItem("Option 3")
    combobox.addItem("Option 4")
    combobox.addItem("Option 5")
    combobox.setMinimumSize(250, 35)
    left_layout.addWidget(combobox)

    # ФИО пользователя
    self.input_fio_user = QLineEdit(self)
    self.input_fio_user.setPlaceholderText("Номер ключа: ")
    self.input_fio_user.setMinimumSize(250, 40)
    self.input_fio_user.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    left_layout.addWidget(self.input_fio_user)

    # Наименование ПО СКЗИ
    combobox = QComboBox(self)
    combobox.setEditable(True)
    combobox.setCurrentText("Выдавший УЦ")
    combobox.addItem("Option 1")
    combobox.addItem("Option 2")
    combobox.addItem("Option 3")
    combobox.addItem("Option 4")
    combobox.addItem("Option 5")
    combobox.setMinimumSize(250, 35)
    left_layout.addWidget(combobox)


    left_layout.setContentsMargins(200, 0, 200, 0)

    # --- ПРАВЫЙ БЛОК ---
    right_layout = QVBoxLayout()

    # Наименование ПО СКЗИ
    combobox = QComboBox(self)
    combobox.setEditable(True)
    combobox.setCurrentText("Область действия / наименование ЭДО")
    combobox.addItem("Option 1")
    combobox.addItem("Option 2")
    combobox.addItem("Option 3")
    combobox.addItem("Option 4")
    combobox.addItem("Option 5")
    combobox.setMinimumSize(250, 35)
    left_layout.addWidget(combobox)

    right_layout.setContentsMargins(200, 0, 200, 0)

    # Наименование ПО СКЗИ
    combobox = QComboBox(self)
    combobox.setEditable(True)
    combobox.setCurrentText("ФИО владельца")
    combobox.addItem("Option 1")
    combobox.addItem("Option 2")
    combobox.addItem("Option 3")
    combobox.addItem("Option 4")
    combobox.addItem("Option 5")
    combobox.setMinimumSize(250, 35)
    left_layout.addWidget(combobox)

    # Календарь (дата)
    today = datetime.today()
    dateedit = QtWidgets.QDateEdit(calendarPopup=True)
    dateedit.setDateTime(today)
    right_layout.addWidget(dateedit)

    # Календарь (дата)
    today = datetime.today()
    dateedit = QtWidgets.QDateEdit(calendarPopup=True)
    dateedit.setDateTime(today)
    right_layout.addWidget(dateedit)

    self.input_fio_user = QLineEdit(self)
    self.input_fio_user.setPlaceholderText("Дополнительно: ")
    self.input_fio_user.setMinimumSize(250, 40)
    self.input_fio_user.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    right_layout.addWidget(self.input_fio_user)

    self.input_fio_user = QLineEdit(self)
    self.input_fio_user.setPlaceholderText("Дополнительно: ")
    self.input_fio_user.setMinimumSize(250, 40)
    self.input_fio_user.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    right_layout.addWidget(self.input_fio_user)

    # Объединяем два вертикальных лэйаута (левый и правый) в горизонтальный
    h_layout = QHBoxLayout()
    h_layout.addLayout(left_layout)
    h_layout.addLayout(right_layout)

    # Добавляем горизонтальный лэйаут в основной вертикальный
    layout.addLayout(h_layout)

    # Шорткат для Enter
    enter_shortcut = QShortcut(QKeySequence("Return"), page)
    enter_shortcut.activated.connect(self.getandgo2)

    # Кнопка "Назад"
    btn_back = QPushButton("Назад")
    btn_back.clicked.connect(self.go_to_second_page)
    layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)

    layout.setContentsMargins(0, 0, 0, 200)

    return page