from datetime import datetime
import getpass

from PyQt6 import QtWidgets
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtWidgets import (
    QWidget,
    QLabel, QPushButton, QVBoxLayout, QRadioButton, QLineEdit, QHBoxLayout, QComboBox, QSizePolicy
)

from PyQt6.QtCore import Qt

def create_page10(self) -> QWidget:
    page = QWidget()
    layout = QVBoxLayout(page)

    # Заголовок
    text_label = QLabel("TLS")
    text_label.setWordWrap(True)
    text_label.setStyleSheet("font-size: 20px; color: #76787A;")
    text_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    layout.addWidget(text_label, alignment=Qt.AlignmentFlag.AlignCenter)

    # --- ЛЕВЫЙ БЛОК ---
    left_layout = QVBoxLayout()

    # Наименование ПО СКЗИ
    self.input_fio_user = QLineEdit(self)
    self.input_fio_user.setPlaceholderText("Номер заявки: ")
    self.input_fio_user.setMinimumSize(250, 40)
    self.input_fio_user.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    left_layout.addWidget(self.input_fio_user)

    # Календарь (дата)
    today = datetime.today()
    dateedit = QtWidgets.QDateEdit(calendarPopup=True)
    dateedit.setDateTime(today)
    left_layout.addWidget(dateedit)

    # Наименование ПО СКЗИ
    combobox = QComboBox(self)
    combobox.setEditable(True)
    combobox.setCurrentText("Среда (тест/продуктив)")
    combobox.addItem("тест")
    combobox.addItem("продуктив")
    combobox.setMinimumSize(250, 35)
    left_layout.addWidget(combobox)

    # Наименование ПО СКЗИ
    combobox = QComboBox(self)
    combobox.setEditable(True)
    combobox.setCurrentText("Доступ (внешний/внутренний)")
    combobox.addItem("внешний")
    combobox.addItem("внутренний")
    combobox.setMinimumSize(250, 35)
    left_layout.addWidget(combobox)

    # Второй ComboBox
    scope = QComboBox(self)
    scope.setEditable(True)
    scope.setCurrentText("Выдавший УЦ")
    scope.addItem("Option 1")
    scope.addItem("Option 2")
    scope.addItem("Option 3")
    scope.setMinimumSize(400, 35)
    left_layout.addWidget(scope)

    # Второй ComboBox
    scope = QComboBox(self)
    scope.setEditable(True)
    scope.setCurrentText("Инициатор")
    scope.addItem("Option 1")
    scope.addItem("Option 2")
    scope.addItem("Option 3")
    scope.setMinimumSize(400, 35)
    left_layout.addWidget(scope)

    left_layout.setContentsMargins(200, 0, 200, 0)

    # --- ПРАВЫЙ БЛОК ---
    right_layout = QVBoxLayout()

    # Второй ComboBox
    scope = QComboBox(self)
    scope.setEditable(True)
    scope.setCurrentText("Владелец АС")
    scope.addItem("Option 1")
    scope.addItem("Option 2")
    scope.addItem("Option 3")
    scope.setMinimumSize(400, 35)
    right_layout.addWidget(scope)

    right_layout.setContentsMargins(200, 0, 200, 0)

    # Наименование ПО СКЗИ
    combobox = QComboBox(self)
    combobox.setEditable(True)
    combobox.setCurrentText("Алгоритм (RSA/ГОСТ)")
    combobox.addItem("RSA")
    combobox.addItem("ГОСТ")
    combobox.setMinimumSize(250, 35)
    right_layout.addWidget(combobox)

    # Второй ComboBox
    scope = QComboBox(self)
    scope.setEditable(True)
    scope.setCurrentText("Область действия / наименование ЭДО")
    scope.addItem("Option 1")
    scope.addItem("Option 2")
    scope.addItem("Option 3")
    scope.setMinimumSize(400, 35)
    right_layout.addWidget(scope)

    # Наименование ПО СКЗИ
    self.input_fio_user = QLineEdit(self)
    self.input_fio_user.setPlaceholderText("DNS: ")
    self.input_fio_user.setMinimumSize(250, 40)
    self.input_fio_user.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    right_layout.addWidget(self.input_fio_user)

    # Второй ComboBox
    scope = QComboBox(self)
    scope.setEditable(True)
    scope.setCurrentText("резолюция ИБ (уточнение/согласовано/отказано)")
    scope.addItem("уточнение")
    scope.addItem("согласовано")
    scope.addItem("отказано")
    scope.setMinimumSize(400, 35)
    right_layout.addWidget(scope)

    self.input_fio_user = QLineEdit(self)
    self.input_fio_user.setPlaceholderText("Примечание: ")
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