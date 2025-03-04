from datetime import datetime
from PyQt6 import QtWidgets
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout,
    QComboBox, QSizePolicy, QGroupBox, QFormLayout
)
from PyQt6.QtCore import Qt

def create_page10(self) -> QWidget:
    page = QWidget()
    main_layout = QVBoxLayout(page)
    main_layout.setContentsMargins(20, 20, 20, 20)
    main_layout.setSpacing(15)

    # Заголовок
    header_label = QLabel("TLS")
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

    # Номер заявки
    self.request_number_le = QLineEdit(self)
    self.request_number_le.setPlaceholderText("Номер заявки:")
    self.request_number_le.setMinimumSize(250, 40)
    self.request_number_le.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    left_form.addRow(QLabel("Заявка:"), self.request_number_le)

    # Дата
    self.dateedit1 = QtWidgets.QDateEdit(calendarPopup=True)
    self.dateedit1.setDateTime(datetime.today())
    left_form.addRow(QLabel("Дата:"), self.dateedit1)

    # Среда (тест/продуктив)
    self.env_cb = QComboBox(self)
    self.env_cb.setEditable(True)
    self.env_cb.setCurrentText("Среда (тест/продуктив)")
    self.env_cb.addItems(["тест", "продуктив"])
    left_form.addRow(QLabel("Среда:"), self.env_cb)

    # Доступ (внешний/внутренний)
    self.access_cb = QComboBox(self)
    self.access_cb.setEditable(True)
    self.access_cb.setCurrentText("Доступ (внешний/внутренний)")
    self.access_cb.addItems(["внешний", "внутренний"])
    left_form.addRow(QLabel("Доступ:"), self.access_cb)

    # Выдавший УЦ
    self.issuer_cb = QComboBox(self)
    self.issuer_cb.setEditable(True)
    self.issuer_cb.setCurrentText("Выдавший УЦ")
    for option in ["Option 1", "Option 2", "Option 3"]:
        self.issuer_cb.addItem(option)
    left_form.addRow(QLabel("УЦ:"), self.issuer_cb)

    # Инициатор
    self.initiator_cb = QComboBox(self)
    self.initiator_cb.setEditable(True)
    self.initiator_cb.setCurrentText("Инициатор")
    for option in ["Option 1", "Option 2", "Option 3"]:
        self.initiator_cb.addItem(option)
    left_form.addRow(QLabel("Инициатор:"), self.initiator_cb)

    h_layout.addWidget(left_group, 1)

    # ---------- ПРАВЫЙ БЛОК ----------
    right_group = QGroupBox("Дополнительные сведения")
    right_form = QFormLayout()
    right_form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
    right_group.setLayout(right_form)

    # Владелец АС
    self.owner_cb = QComboBox(self)
    self.owner_cb.setEditable(True)
    self.owner_cb.setCurrentText("Владелец АС")
    for option in ["Option 1", "Option 2", "Option 3"]:
        self.owner_cb.addItem(option)
    right_form.addRow(QLabel("Владелец АС:"), self.owner_cb)

    # Алгоритм (RSA/ГОСТ)
    self.algo_cb = QComboBox(self)
    self.algo_cb.setEditable(True)
    self.algo_cb.setCurrentText("Алгоритм (RSA/ГОСТ)")
    self.algo_cb.addItems(["RSA", "ГОСТ"])
    right_form.addRow(QLabel("Алгоритм:"), self.algo_cb)

    # Область действия / наименование ЭДО
    self.scope_cb = QComboBox(self)
    self.scope_cb.setEditable(True)
    self.scope_cb.setCurrentText("Область действия / наименование ЭДО")
    for option in ["Option 1", "Option 2", "Option 3"]:
        self.scope_cb.addItem(option)
    right_form.addRow(QLabel("Область/ЭДО:"), self.scope_cb)

    # DNS
    self.dns_le = QLineEdit(self)
    self.dns_le.setPlaceholderText("DNS:")
    self.dns_le.setMinimumSize(250, 40)
    self.dns_le.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    right_form.addRow(QLabel("DNS:"), self.dns_le)

    # Резолюция ИБ
    self.resolution_cb = QComboBox(self)
    self.resolution_cb.setEditable(True)
    self.resolution_cb.setCurrentText("резолюция ИБ (уточнение/согласовано/отказано)")
    self.resolution_cb.addItems(["уточнение", "согласовано", "отказано"])
    right_form.addRow(QLabel("Резолюция ИБ:"), self.resolution_cb)

    # Примечание
    self.note_le = QLineEdit(self)
    self.note_le.setPlaceholderText("Примечание:")
    self.note_le.setMinimumSize(250, 40)
    self.note_le.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    right_form.addRow(QLabel("Примечание:"), self.note_le)

    h_layout.addWidget(right_group, 1)

    # Шорткат для Enter
    enter_shortcut = QShortcut(QKeySequence("Return"), page)
    enter_shortcut.activated.connect(self.getandgo2)

    # Кнопка "Назад"
    btn_back = QPushButton("Назад")
    btn_back.clicked.connect(self.go_to_second_page)
    main_layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)

    return page
