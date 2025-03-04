from datetime import datetime
from PyQt6 import QtWidgets
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout,
    QComboBox, QSizePolicy, QGroupBox, QFormLayout
)
from PyQt6.QtCore import Qt

def create_page9(self) -> QWidget:
    page = QWidget()
    main_layout = QVBoxLayout(page)
    main_layout.setContentsMargins(20, 20, 20, 20)
    main_layout.setSpacing(15)

    # Заголовок
    header_label = QLabel("КБР")
    header_label.setWordWrap(True)
    header_label.setStyleSheet("font-size: 20px; color: #76787A;")
    header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    main_layout.addWidget(header_label)

    # Горизонтальный лэйаут
    h_layout = QHBoxLayout()
    h_layout.setSpacing(30)
    main_layout.addLayout(h_layout)

    # ---------- ЛЕВЫЙ БЛОК ----------
    left_group = QGroupBox("Основные данные")
    left_form = QFormLayout()
    left_form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
    left_group.setLayout(left_form)

    # Заявка/номер обращения
    self.request_le = QLineEdit(self)
    self.request_le.setPlaceholderText("Заявка/номер обращения:")
    self.request_le.setMinimumSize(250, 40)
    self.request_le.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    left_form.addRow(QLabel("Обращение:"), self.request_le)

    # Тип носителя (Да/Нет?)
    self.nositel_cb = QComboBox(self)
    self.nositel_cb.setEditable(True)
    self.nositel_cb.setCurrentText("Тип носителя")
    self.nositel_cb.addItem("Да")
    self.nositel_cb.addItem("Нет")
    left_form.addRow(QLabel("Тип носителя:"), self.nositel_cb)

    # Носитель (Серийный номер)
    self.nositel_serial_cb = QComboBox(self)
    self.nositel_serial_cb.setEditable(True)
    self.nositel_serial_cb.setCurrentText("Носитель (Серийный номер)")
    for option in ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]:
        self.nositel_serial_cb.addItem(option)
    left_form.addRow(QLabel("Серийный номер:"), self.nositel_serial_cb)

    # Номер ключа
    self.key_number_le = QLineEdit(self)
    self.key_number_le.setPlaceholderText("Номер ключа:")
    self.key_number_le.setMinimumSize(250, 40)
    self.key_number_le.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    left_form.addRow(QLabel("Номер ключа:"), self.key_number_le)

    # Выдавший УЦ
    self.issuer_cb = QComboBox(self)
    self.issuer_cb.setEditable(True)
    self.issuer_cb.setCurrentText("Выдавший УЦ")
    for option in ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]:
        self.issuer_cb.addItem(option)
    left_form.addRow(QLabel("УЦ:"), self.issuer_cb)

    h_layout.addWidget(left_group, 1)

    # ---------- ПРАВЫЙ БЛОК ----------
    right_group = QGroupBox("Дополнительно")
    right_form = QFormLayout()
    right_form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
    right_group.setLayout(right_form)

    # Область действия / наименование ЭДО
    self.scope_cb = QComboBox(self)
    self.scope_cb.setEditable(True)
    self.scope_cb.setCurrentText("Область действия / наименование ЭДО")
    for option in ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]:
        self.scope_cb.addItem(option)
    right_form.addRow(QLabel("Область/ЭДО:"), self.scope_cb)

    # ФИО владельца
    self.owner_cb = QComboBox(self)
    self.owner_cb.setEditable(True)
    self.owner_cb.setCurrentText("ФИО владельца")
    for option in ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]:
        self.owner_cb.addItem(option)
    right_form.addRow(QLabel("Владелец:"), self.owner_cb)

    # Дата 1
    self.dateedit1 = QtWidgets.QDateEdit(calendarPopup=True)
    self.dateedit1.setDateTime(datetime.today())
    right_form.addRow(QLabel("Дата 1:"), self.dateedit1)

    # Дата 2
    self.dateedit2 = QtWidgets.QDateEdit(calendarPopup=True)
    self.dateedit2.setDateTime(datetime.today())
    right_form.addRow(QLabel("Дата 2:"), self.dateedit2)

    # Дополнительно 1
    self.additional1_le = QLineEdit(self)
    self.additional1_le.setPlaceholderText("Дополнительно:")
    self.additional1_le.setMinimumSize(250, 40)
    self.additional1_le.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    right_form.addRow(QLabel("Дополнительно:"), self.additional1_le)

    # Дополнительно 2
    self.additional2_le = QLineEdit(self)
    self.additional2_le.setPlaceholderText("Дополнительно:")
    self.additional2_le.setMinimumSize(250, 40)
    self.additional2_le.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    right_form.addRow(QLabel("Дополнительно:"), self.additional2_le)

    h_layout.addWidget(right_group, 1)

    # Шорткат для Enter
    enter_shortcut = QShortcut(QKeySequence("Return"), page)
    enter_shortcut.activated.connect(self.getandgo2)

    # Кнопка "Назад"
    btn_back = QPushButton("Назад")
    btn_back.clicked.connect(self.go_to_second_page)
    main_layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)

    return page
