from datetime import datetime
from PyQt6 import QtWidgets
from PyQt6.QtGui import QShortcut, QKeySequence, QPalette, QColor
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout,
    QComboBox, QGroupBox, QFormLayout
)
from PyQt6.QtCore import Qt, QDate

from logic.db import enter_TLS


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
    palette = self.request_number_le.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    self.request_number_le.setPalette(palette)
    left_form.addRow(QLabel("Заявка:"), self.request_number_le)

    # Дата
    self.dateedit1 = QtWidgets.QDateEdit(calendarPopup=True)
    self.dateedit1.setDateTime(datetime.today())
    left_form.addRow(QLabel("Дата:"), self.dateedit1)

    # Среда (тест/продуктив)
    self.env_cb = QComboBox(self)
    self.env_cb.setEditable(True)
    self.env_cb.setCurrentText("Среда (тест/продуктив)")
    line_edit = self.env_cb.lineEdit()
    line_edit.setPlaceholderText("Среда (тест/продуктив)")
    palette = line_edit.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    line_edit.setPalette(palette)
    for option in ["тест", "продуктив"]:
        self.env_cb.addItem(option)
    self.env_cb.clearEditText()
    left_form.addRow(QLabel("Среда:"), self.env_cb)

    # Доступ (внешний/внутренний)
    self.access_cb = QComboBox(self)
    self.access_cb.setEditable(True)
    self.access_cb.setCurrentText("Доступ (внешний/внутренний)")
    line_edit = self.access_cb.lineEdit()
    line_edit.setPlaceholderText("Доступ (внешний/внутренний)")
    palette = line_edit.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    line_edit.setPalette(palette)
    for option in ["внешний", "внутренний"]:
        self.access_cb.addItem(option)
    self.access_cb.clearEditText()
    left_form.addRow(QLabel("Доступ:"), self.access_cb)

    # Выдавший УЦ
    self.issuer_cb = QComboBox(self)
    self.issuer_cb.setEditable(True)
    self.issuer_cb.setCurrentText("Выдавший УЦ")
    line_edit = self.issuer_cb.lineEdit()
    line_edit.setPlaceholderText("Выдавший УЦ")
    palette = line_edit.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    line_edit.setPalette(palette)
    for option in ["Option 1", "Option 2", "Option 3"]:
        self.issuer_cb.addItem(option)
    self.issuer_cb.clearEditText()
    left_form.addRow(QLabel("УЦ:"), self.issuer_cb)

    # Инициатор
    self.initiator_cb = QComboBox(self)
    self.initiator_cb.setEditable(True)
    self.initiator_cb.setCurrentText("Инициатор")
    line_edit = self.initiator_cb.lineEdit()
    line_edit.setPlaceholderText("Инициатор")
    palette = line_edit.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    line_edit.setPalette(palette)
    for option in ["Option 1", "Option 2", "Option 3"]:
        self.initiator_cb.addItem(option)
    self.initiator_cb.clearEditText()
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
    line_edit = self.owner_cb.lineEdit()
    line_edit.setPlaceholderText("Владелец АС")
    palette = line_edit.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    line_edit.setPalette(palette)
    for option in ["Option 1", "Option 2", "Option 3"]:
        self.owner_cb.addItem(option)
    self.owner_cb.clearEditText()
    right_form.addRow(QLabel("Владелец АС:"), self.owner_cb)

    # Алгоритм (RSA/ГОСТ)
    self.algo_cb = QComboBox(self)
    self.algo_cb.setEditable(True)
    self.algo_cb.setCurrentText("Алгоритм (RSA/ГОСТ)")
    line_edit = self.algo_cb.lineEdit()
    line_edit.setPlaceholderText("Алгоритм (RSA/ГОСТ)")
    palette = line_edit.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    line_edit.setPalette(palette)
    self.algo_cb.addItems(["RSA", "ГОСТ"])
    self.algo_cb.clearEditText()
    right_form.addRow(QLabel("Алгоритм:"), self.algo_cb)

    # Область действия / наименование ЭДО
    self.scope_cb = QComboBox(self)
    self.scope_cb.setEditable(True)
    self.scope_cb.setCurrentText("Область действия / наименование ЭДО")
    line_edit = self.scope_cb.lineEdit()
    line_edit.setPlaceholderText("Область действия / наименование ЭДО")
    palette = line_edit.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    line_edit.setPalette(palette)
    for option in ["Option 1", "Option 2", "Option 3"]:
        self.scope_cb.addItem(option)
    self.scope_cb.clearEditText()
    right_form.addRow(QLabel("Область/ЭДО:"), self.scope_cb)

    # DNS
    self.dns_le = QLineEdit(self)
    self.dns_le.setPlaceholderText("DNS:")
    palette = self.dns_le.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    self.dns_le.setPalette(palette)
    right_form.addRow(QLabel("DNS:"), self.dns_le)

    # Резолюция ИБ
    self.resolution_cb = QComboBox(self)
    self.resolution_cb.setEditable(True)
    self.resolution_cb.setCurrentText("Резолюция ИБ (уточнение/согласовано/отказано)")
    line_edit = self.resolution_cb.lineEdit()
    line_edit.setPlaceholderText("Резолюция ИБ")
    palette = line_edit.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    line_edit.setPalette(palette)
    self.resolution_cb.addItems(["уточнение", "согласовано", "отказано"])
    self.resolution_cb.clearEditText()
    right_form.addRow(QLabel("Резолюция ИБ:"), self.resolution_cb)

    # Примечание
    self.note_le = QLineEdit(self)
    self.note_le.setPlaceholderText("Примечание:")
    palette = self.note_le.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    self.note_le.setPalette(palette)
    right_form.addRow(QLabel("Примечание:"), self.note_le)

    # Кнопка для сохранения/обработки данных
    self.save_button = QPushButton("Сохранить", self)
    right_form.addRow(self.save_button)
    self.save_button.clicked.connect(lambda: save_value10(self))

    h_layout.addWidget(right_group, 1)

    # Шорткат для Enter
    enter_shortcut = QShortcut(QKeySequence("Return"), page)
    enter_shortcut.activated.connect(lambda: save_value10(self))

    # Кнопка "Назад"
    btn_back = QPushButton("Назад")
    btn_back.clicked.connect(self.go_to_second_page)
    main_layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)

    return page


def save_value10(self):
    request_number = self.request_number_le.text()
    date_str = self.dateedit1.date().toPyDate().strftime('%Y-%m-%d')
    env = self.env_cb.currentText()
    access = self.access_cb.currentText()
    issuer = self.issuer_cb.currentText()
    initiator = self.initiator_cb.currentText()
    owner = self.owner_cb.currentText()
    algo = self.algo_cb.currentText()
    scope = self.scope_cb.currentText()
    dns = self.dns_le.text()
    resolution = self.resolution_cb.currentText()
    note = self.note_le.text()

    enter_TLS(request_number, date_str, env, access, issuer, initiator,
              owner, algo, scope, dns, resolution, note)

    clear_fields_tls(self)


def clear_fields_tls(self):
    self.request_number_le.clear()
    self.env_cb.clearEditText()
    self.access_cb.clearEditText()
    self.issuer_cb.clearEditText()
    self.initiator_cb.clearEditText()
    self.dateedit1.setDate(QDate.currentDate())
    self.owner_cb.clearEditText()
    self.algo_cb.clearEditText()
    self.scope_cb.clearEditText()
    self.dns_le.clear()
    self.resolution_cb.clearEditText()
    self.note_le.clear()
