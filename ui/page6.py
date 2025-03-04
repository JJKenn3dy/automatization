import getpass
from datetime import datetime
from PyQt6 import QtWidgets
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit,
    QRadioButton, QHBoxLayout, QComboBox, QGroupBox, QFormLayout
)
from PyQt6.QtCore import Qt
from logic.db import enter_fio

def getandgo(self, text):
    enter_fio(text)
    self.go_to_license_2()

def create_page6(self) -> QWidget:
    page = QWidget()
    main_layout = QVBoxLayout(page)
    main_layout.setContentsMargins(20, 20, 20, 20)
    main_layout.setSpacing(15)

    # Заголовок
    header_label = QLabel("Лицензии")
    header_label.setWordWrap(True)
    header_label.setStyleSheet("font-size: 20px; color: #76787A;")
    header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    main_layout.addWidget(header_label)

    # Основной горизонтальный лэйаут (для левого и правого блоков)
    h_layout = QHBoxLayout()
    h_layout.setSpacing(30)
    main_layout.addLayout(h_layout)

    # ---------- ЛЕВЫЙ БЛОК (Данные заявки) ----------
    left_group = QGroupBox("Данные заявки")
    left_group_layout = QFormLayout()
    left_group_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
    left_group.setLayout(left_group_layout)

    # Номер заявки
    self.enter_number = QLineEdit(self)
    self.enter_number.setPlaceholderText("Введите номер заявки")
    self.enter_number.setMinimumSize(250, 40)
    self.enter_number.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    left_group_layout.addRow(QLabel("Номер заявки:"), self.enter_number)

    # Наименование ПО СКЗИ
    self.combobox = QComboBox(self)
    self.combobox.setEditable(True)
    self.combobox.setCurrentText("Наименование ПО СКЗИ")
    for option in ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]:
        self.combobox.addItem(option)
    self.combobox.setMinimumSize(250, 35)
    left_group_layout.addRow(QLabel("Выберите ПО СКЗИ:"), self.combobox)

    # Ключ (доп. поле)
    self.enter_key = QLineEdit(self)
    self.enter_key.setPlaceholderText("Введите ключ (например, test)")
    self.enter_key.setMinimumSize(250, 40)
    self.enter_key.setText('test')
    self.enter_key.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    left_group_layout.addRow(QLabel("Ключ:"), self.enter_key)

    # Второй ComboBox (область)
    self.scope = QComboBox(self)
    self.scope.setEditable(True)
    self.scope.setCurrentText("Область применения")
    for option in ["Option 1", "Option 2", "Option 3"]:
        self.scope.addItem(option)
    self.scope.setMinimumSize(250, 35)
    left_group_layout.addRow(QLabel("Область/сфера:"), self.scope)

    # ФИО пользователя
    self.input_fio_user = QLineEdit(self)
    self.input_fio_user.setPlaceholderText("Введите ФИО пользователя")
    self.input_fio_user.setMinimumSize(250, 40)
    self.input_fio_user.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    left_group_layout.addRow(QLabel("ФИО пользователя:"), self.input_fio_user)

    h_layout.addWidget(left_group, 1)  # Пропорционально занимает часть

    # ---------- ПРАВЫЙ БЛОК (Информация ИТ) ----------
    right_group = QGroupBox("Информация об установке")
    right_group_layout = QFormLayout()
    right_group_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
    right_group.setLayout(right_group_layout)

    # Календарь (дата)
    self.dateedit = QtWidgets.QDateEdit(calendarPopup=True)
    self.dateedit.setDateTime(datetime.today())
    right_group_layout.addRow(QLabel("Дата:"), self.dateedit)

    # ФИО сотрудника ИТ
    self.user = QLineEdit(self)
    self.user.setPlaceholderText("Введите ФИО сотрудника ИТ")
    self.user.setMinimumSize(250, 40)
    self.user.setText(getpass.getuser())
    self.user.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    right_group_layout.addRow(QLabel("Сотрудник ИТ:"), self.user)

    # Статус лицензии (радиокнопки) - отдельный QGroupBox
    status_group = QGroupBox("Статус лицензии")
    status_layout = QVBoxLayout()
    status_group.setLayout(status_layout)

    radio_style = """
        QRadioButton {
            font-size: 16px;
            color: rgb(118, 120, 122);
            padding: 5px;
        }
        QRadioButton:checked {
            color: rgb(139, 197, 64);
        }
        QRadioButton::indicator {
            width: 15px;
            height: 15px;
        }
    """
    self.rb_issued = QRadioButton("Выдано")
    self.rb_issued.setStyleSheet(radio_style)
    self.rb_installed = QRadioButton("Установлено")
    self.rb_installed.setStyleSheet(radio_style)
    self.rb_taken = QRadioButton("Изьято")
    self.rb_taken.setStyleSheet(radio_style)

    status_layout.addWidget(self.rb_issued)
    status_layout.addWidget(self.rb_installed)
    status_layout.addWidget(self.rb_taken)

    right_group_layout.addRow(status_group)

    h_layout.addWidget(right_group, 1)

    # ---------- Дополнительные поля (изъятие/уничтожение) ----------
    # Группа, которая будет показываться/скрываться
    self.extra_group = QGroupBox("Дополнительные сведения")
    extra_layout = QFormLayout()
    self.extra_group.setLayout(extra_layout)
    self.extra_group.setVisible(False)  # Изначально скрываем

    style_sheet2 = """
        QLineEdit {
            font-size: 16px;
            color: rgb(118, 120, 122);
            padding: 5px;
        }
    """
    self.input_mark = QLineEdit(self)
    self.input_mark.setPlaceholderText("Введите отметку об изъятии/уничтожении...")
    self.input_mark.setStyleSheet(style_sheet2)
    extra_layout.addRow(QLabel("Отметка:"), self.input_mark)

    self.input_date = QLineEdit(self)
    self.input_date.setPlaceholderText("Дата, расписка, номер акта об уничтожении...")
    self.input_date.setStyleSheet(style_sheet2)
    extra_layout.addRow(QLabel("Документ/дата:"), self.input_date)

    main_layout.addWidget(self.extra_group)

    # Кнопка "Назад"
    btn_back = QPushButton("Назад")
    btn_back.clicked.connect(self.go_to_second_page)
    main_layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)

    # Шорткат для Enter
    enter_shortcut = QShortcut(QKeySequence("Return"), page)
    enter_shortcut.activated.connect(self.getandgo2)

    # Подключаем сигналы радиокнопок к функции переключения видимости
    self.rb_issued.toggled.connect(self.update_extra_fields_visibility)
    self.rb_installed.toggled.connect(self.update_extra_fields_visibility)
    self.rb_taken.toggled.connect(self.update_extra_fields_visibility)

    return page

def update_extra_fields_visibility(self):
    """
    Если нажата радиокнопка "Изьято", то показываем блок
    'Дополнительные сведения'. Иначе скрываем.
    """
    self.extra_group.setVisible(self.rb_taken.isChecked())
