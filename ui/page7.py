from datetime import datetime
import getpass

from PyQt6 import QtWidgets
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtWidgets import (
    QWidget,
    QLabel, QPushButton, QVBoxLayout, QRadioButton, QLineEdit, QHBoxLayout, QComboBox, QSizePolicy
)

from PyQt6.QtCore import Qt

def create_page7(self) -> QWidget:
    page = QWidget()
    layout = QVBoxLayout(page)

    # Заголовок
    text_label = QLabel("СКЗИ")
    text_label.setWordWrap(True)
    text_label.setStyleSheet("font-size: 20px; color: #76787A;")
    text_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    layout.addWidget(text_label, alignment=Qt.AlignmentFlag.AlignCenter)

    # --- ЛЕВЫЙ БЛОК ---
    left_layout = QVBoxLayout()

    # Наименование ПО СКЗИ
    combobox = QComboBox(self)
    combobox.setEditable(True)
    combobox.setCurrentText("Наименование ПО СКЗИ")
    combobox.addItem("Option 1")
    combobox.addItem("Option 2")
    combobox.addItem("Option 3")
    combobox.addItem("Option 4")
    combobox.addItem("Option 5")
    combobox.setMinimumSize(250, 35)
    left_layout.addWidget(combobox)

    # Наименование ПО СКЗИ
    combobox = QComboBox(self)
    combobox.setEditable(True)
    combobox.setCurrentText("Версия СКЗИ")
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
    left_layout.addWidget(dateedit)

    left_layout.setContentsMargins(200, 0, 200, 0)

    # --- ПРАВЫЙ БЛОК ---
    right_layout = QVBoxLayout()

    # ФИО пользователя
    self.input_fio_user = QLineEdit(self)
    self.input_fio_user.setPlaceholderText("Регистрационный (серийный) номер: ")
    self.input_fio_user.setMinimumSize(250, 40)
    self.input_fio_user.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    right_layout.addWidget(self.input_fio_user)

    right_layout.setContentsMargins(200, 0, 200, 0)


    # Наименование ПО СКЗИ
    combobox = QComboBox(self)
    combobox.setEditable(True)
    combobox.setCurrentText("От кого получены")
    combobox.addItem("Option 1")
    combobox.addItem("Option 2")
    combobox.addItem("Option 3")
    combobox.addItem("Option 4")
    combobox.addItem("Option 5")
    combobox.setMinimumSize(250, 35)
    right_layout.addWidget(combobox)

    # ФИО пользователя
    self.input_fio_user = QLineEdit(self)
    self.input_fio_user.setPlaceholderText("Дата и номер документа, сопроводительного письма: ")
    self.input_fio_user.setMinimumSize(250, 40)
    self.input_fio_user.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    left_layout.addWidget(self.input_fio_user)

    # ФИО пользователя
    self.input_fio_user = QLineEdit(self)
    self.input_fio_user.setPlaceholderText("ФИО владельца, бизнес процесс в рамках которого используется: ")
    self.input_fio_user.setMinimumSize(250, 40)
    self.input_fio_user.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    left_layout.addWidget(self.input_fio_user)

    # Объединяем два вертикальных лэйаута (левый и правый) в горизонтальный
    h_layout = QHBoxLayout()
    h_layout.addLayout(left_layout)
    h_layout.addLayout(right_layout)

    # Добавляем горизонтальный лэйаут в основной вертикальный
    layout.addLayout(h_layout)

    # Наименование ПО СКЗИ
    combobox = QComboBox(self)
    combobox.setEditable(True)
    combobox.setCurrentText("Примечание: ")
    combobox.addItem("Option 1")
    combobox.addItem("Option 2")
    combobox.addItem("Option 3")
    combobox.addItem("Option 4")
    combobox.addItem("Option 5")
    combobox.setMinimumSize(250, 35)
    right_layout.addWidget(combobox)

    # Поля для изъятия/уничтожения/вывода
    style_sheet2 = """
                QLineEdit {
                    font-size: 16px;
                    color: rgb(118, 120, 122);  /* Серый */
                    padding: 5px;
                }
            """
    self.input_mark = QLineEdit(self)
    self.input_mark.setPlaceholderText("Дополнительно: ")
    self.input_mark.setMaximumSize(250, 40)
    self.input_mark.setStyleSheet(style_sheet2)
    layout.addWidget(self.input_mark, alignment=Qt.AlignmentFlag.AlignCenter)

    self.input_date = QLineEdit(self)
    self.input_date.setPlaceholderText("Номер сертификата соответствия: ")
    self.input_date.setMaximumSize(250, 40)
    self.input_date.setStyleSheet(style_sheet2)
    right_layout.addWidget(self.input_date)


    # Календарь (дата)
    today = datetime.today()
    dateedit = QtWidgets.QDateEdit(calendarPopup=True)
    dateedit.setDateTime(today)
    right_layout.addWidget(dateedit)

    # Шорткат для Enter
    enter_shortcut = QShortcut(QKeySequence("Return"), page)
    enter_shortcut.activated.connect(self.getandgo2)

    # Кнопка "Назад"
    btn_back = QPushButton("Назад")
    btn_back.clicked.connect(self.go_to_second_page)
    layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)

    layout.setContentsMargins(0, 0, 0, 200)

    return page