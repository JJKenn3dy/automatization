import getpass
from datetime import datetime
from datetime import datetime
from PyQt6 import QtWidgets
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import (
    QWidget,
    QLabel, QPushButton, QVBoxLayout, QLineEdit, QSizePolicy,
    QRadioButton, QGridLayout, QHBoxLayout, QComboBox
)
from PyQt6.QtCore import Qt
from logic.db import enter_fio


def getandgo(self, text):
    enter_fio(text)
    self.go_to_license_2()


def create_page6(self) -> QWidget:
    page = QWidget()
    layout = QVBoxLayout(page)

    # Заголовок
    text_label = QLabel("Лицензии")
    text_label.setWordWrap(True)
    text_label.setStyleSheet("font-size: 20px; color: #76787A;")
    text_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    layout.addWidget(text_label, alignment=Qt.AlignmentFlag.AlignCenter)

    # --- ЛЕВЫЙ БЛОК ---
    left_layout = QVBoxLayout()

    # Номер заявки
    self.enter_number = QLineEdit(self)
    self.enter_number.setPlaceholderText("Номер заявки: ")
    self.enter_number.setMinimumSize(250, 40)
    self.enter_number.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    left_layout.addWidget(self.enter_number)

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

    # Дополнительное поле (например, ключ)
    self.enter_key = QLineEdit(self)
    self.enter_key.setPlaceholderText("Номер заявки: ")
    self.enter_key.setMinimumSize(250, 40)
    self.enter_key.setText('test')
    self.enter_key.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    left_layout.addWidget(self.enter_key)

    # Второй ComboBox
    scope = QComboBox(self)
    scope.setEditable(True)
    scope.setCurrentText("Наименование ПО СКЗИ")
    scope.addItem("Option 1")
    scope.addItem("Option 2")
    scope.addItem("Option 3")
    scope.setMinimumSize(400, 35)
    left_layout.addWidget(scope)

    # ФИО пользователя
    self.input_fio_user = QLineEdit(self)
    self.input_fio_user.setPlaceholderText("ФИО пользователя: ")
    self.input_fio_user.setMinimumSize(250, 40)
    self.input_fio_user.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    left_layout.addWidget(self.input_fio_user)

    left_layout.setContentsMargins(200, 0, 200, 0)

    # --- ПРАВЫЙ БЛОК ---
    right_layout = QVBoxLayout()

    # Календарь (дата)
    today = datetime.today()
    dateedit = QtWidgets.QDateEdit(calendarPopup=True)
    dateedit.setDateTime(today)
    right_layout.addWidget(dateedit)

    # ФИО сотрудника ИТ
    self.user = QLineEdit(self)
    self.user.setPlaceholderText("ФИО сотрудника ИТ")
    self.user.setMinimumSize(250, 40)
    self.user.setText(f"{getpass.getuser()}")
    self.user.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    right_layout.addWidget(self.user)

    # Радиокнопки
    style_sheet = """
        QRadioButton {
            font-size: 16px;
            color: rgb(118, 120, 122);  /* Серый */
            padding: 5px;
        }
        QRadioButton:checked {
            color: rgb(139, 197, 64);   /* Зеленый */
        }
        QRadioButton::indicator {
            width: 15px;
            height: 15px;
        }
    """
    rb1 = QRadioButton("Выдано")
    rb1.setStyleSheet(style_sheet)
    rb2 = QRadioButton("Установлено")
    rb2.setStyleSheet(style_sheet)
    rb3 = QRadioButton("Изьято")
    rb3.setStyleSheet(style_sheet)
    right_layout.addWidget(rb1)
    right_layout.addWidget(rb2)
    right_layout.addWidget(rb3)

    # Объединяем два вертикальных лэйаута (левый и правый) в горизонтальный
    h_layout = QHBoxLayout()
    h_layout.addLayout(left_layout)
    h_layout.addLayout(right_layout)

    # Добавляем горизонтальный лэйаут в основной вертикальный
    layout.addLayout(h_layout)

    # Поля для изъятия/уничтожения/вывода
    style_sheet2 = """
            QLineEdit {
                font-size: 16px;
                color: rgb(118, 120, 122);  /* Серый */
                padding: 5px;
            }
        """
    self.input_mark = QLineEdit(self)
    self.input_mark.setPlaceholderText("Отметка об изъятии/уничтожении/вывода из эксплуатации")
    self.input_mark.setMaximumSize(250, 40)
    self.input_mark.setStyleSheet(style_sheet2)
    layout.addWidget(self.input_mark, alignment=Qt.AlignmentFlag.AlignCenter)

    self.input_date = QLineEdit(self)
    self.input_date.setPlaceholderText("Дата, расписка, номер акта об уничтожении")
    self.input_date.setMaximumSize(250,40)
    self.input_date.setStyleSheet(style_sheet2)
    layout.addWidget(self.input_date, alignment=Qt.AlignmentFlag.AlignCenter)

    right_layout.setContentsMargins(200, 0, 200, 0)

    # Шорткат для Enter
    enter_shortcut = QShortcut(QKeySequence("Return"), page)
    enter_shortcut.activated.connect(self.getandgo2)

    # Кнопка "Назад"
    btn_back = QPushButton("Назад")
    btn_back.clicked.connect(self.go_to_second_page)
    layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)

    layout.setContentsMargins(0, 0, 0, 200)

    return page