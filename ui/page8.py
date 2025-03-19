from datetime import datetime
from PyQt6 import QtWidgets
from PyQt6.QtGui import QShortcut, QKeySequence, QPalette, QColor
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout,
    QComboBox, QSizePolicy, QGroupBox, QFormLayout
)
from PyQt6.QtCore import Qt, QDate

from logic.db import enter_keys


def create_page8(self) -> QWidget:
    page = QWidget()
    main_layout = QVBoxLayout(page)
    main_layout.setContentsMargins(20, 20, 20, 20)
    main_layout.setSpacing(15)

    # Заголовок
    header_label = QLabel("Ключи УКЭП")
    header_label.setWordWrap(True)
    header_label.setStyleSheet("font-size: 20px; color: #76787A;")
    header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    main_layout.addWidget(header_label)

    # Горизонтальный лэйаут для левого и правого блоков
    h_layout = QHBoxLayout()
    h_layout.setSpacing(30)
    main_layout.addLayout(h_layout)

    # ---------- ЛЕВЫЙ БЛОК ----------
    left_group = QGroupBox("Основные данные")
    left_form = QFormLayout()
    left_form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
    left_group.setLayout(left_form)

    # Статус да/нет
    self.status_cb = QComboBox(self)
    self.status_cb.setEditable(False)
    self.status_cb.setCurrentText("Статус да/нет")
    self.status_cb.addItems(["Да", "Нет"])
    line_edit = self.status_cb.lineEdit()
    left_form.addRow(QLabel("Статус:"), self.status_cb)

    # Тип носителя
    self.nositel_type_cb_key = QComboBox(self)
    self.nositel_type_cb_key.setEditable(True)
    line_edit = self.nositel_type_cb_key.lineEdit()
    line_edit.setPlaceholderText("Тип носителя + его серийный номер")
    # Создаём палитру
    palette = line_edit.palette()
    # Цвет обычного текста (чёрный)
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    # Цвет placeholder-текста (зелёный)
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    # Применяем палитру к QLineEdit
    line_edit.setPalette(palette)
    for option in ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]:
        self.nositel_type_cb_key.addItem(option)
    self.nositel_type_cb_key.clearEditText()

    left_form.addRow(QLabel("Тип носителя + серийный номер"), self.nositel_type_cb_key)

    # Серийный номер
    self.serial_le_key = QLineEdit(self)
    self.serial_le_key.setPlaceholderText("Серийный номер:")
    # Создаём палитру
    palette = self.serial_le_key.palette()
    # Цвет обычного текста (белый)
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    # Цвет placeholder-текста (зелёный)
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    # Применяем палитру к QLineEdit
    self.serial_le_key.setPalette(palette)
    left_form.addRow(QLabel("Серийный номер:"), self.serial_le_key)

    # Выдавший УЦ
    self.issuer_cb_key = QComboBox(self)
    self.issuer_cb_key.setEditable(True)
    line_edit = self.issuer_cb_key.lineEdit()
    line_edit.setPlaceholderText("УЦ: ")
    # Создаём палитру
    palette = line_edit.palette()
    # Цвет обычного текста (чёрный)
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    # Цвет placeholder-текста (зелёный)
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    # Применяем палитру к QLineEdit
    line_edit.setPalette(palette)
    for option in ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]:
        self.issuer_cb_key.addItem(option)
    self.issuer_cb_key.clearEditText()
    left_form.addRow(QLabel("УЦ:"), self.issuer_cb_key)

    # Область действия / наименование ЭДО
    self.scope_cb_key = QComboBox(self)
    self.scope_cb_key.setEditable(True)
    line_edit = self.scope_cb_key.lineEdit()
    line_edit.setPlaceholderText("Область/ЭДО:")
    # Создаём палитру
    palette = line_edit.palette()
    # Цвет обычного текста (чёрный)
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    # Цвет placeholder-текста (зелёный)
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    # Применяем палитру к QLineEdit
    line_edit.setPalette(palette)
    for option in ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]:
        self.scope_cb_key.addItem(option)
    self.scope_cb_key.clearEditText()
    left_form.addRow(QLabel("Область/ЭДО:"), self.scope_cb_key)

    # ФИО владельца
    self.owner_cb_key = QComboBox(self)
    self.owner_cb_key.setEditable(True)
    line_edit = self.owner_cb_key.lineEdit()
    line_edit.setPlaceholderText("Версия СКЗИ")
    # Создаём палитру
    palette = line_edit.palette()
    # Цвет обычного текста (чёрный)
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    # Цвет placeholder-текста (зелёный)
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    # Применяем палитру к QLineEdit
    line_edit.setPalette(palette)
    for option in ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]:
        self.owner_cb_key.addItem(option)
    self.owner_cb_key.clearEditText()
    left_form.addRow(QLabel("Владелец:"), self.owner_cb_key)

    h_layout.addWidget(left_group, 1)

    # ---------- ПРАВЫЙ БЛОК ----------
    right_group = QGroupBox("Дополнительно")
    right_form = QFormLayout()
    right_form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
    right_group.setLayout(right_form)

    # VIP / Critical
    self.vip_cb = QComboBox(self)
    self.vip_cb.setEditable(False)
    self.vip_cb.setCurrentText("VIP/Critical")
    self.vip_cb.addItems(["VIP", "Critical"])
    right_form.addRow(QLabel("VIP/Critical:"), self.vip_cb)

    # Дата (1)
    self.dateedit1_key = QtWidgets.QDateEdit(calendarPopup=True)
    self.dateedit1_key.setDateTime(datetime.today())
    right_form.addRow(QLabel("Дата начала:"), self.dateedit1_key)

    # Дата (2)
    self.dateedit2 = QtWidgets.QDateEdit(calendarPopup=True)
    self.dateedit2.setDateTime(datetime.today())
    right_form.addRow(QLabel("Дата окончания:"), self.dateedit2)

    # Дополнительно
    self.additional_cb_key = QComboBox(self)
    self.additional_cb_key.setEditable(True)
    line_edit = self.additional_cb_key.lineEdit()
    line_edit.setPlaceholderText("Дополнительно:")
    # Создаём палитру
    palette = line_edit.palette()
    # Цвет обычного текста (чёрный)
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    # Цвет placeholder-текста (зелёный)
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    # Применяем палитру к QLineEdit
    line_edit.setPalette(palette)
    for option in ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]:
        self.additional_cb_key.addItem(option)
    self.additional_cb_key.clearEditText()
    right_form.addRow(QLabel("Дополнительно:"), self.additional_cb_key)

    # Заявка/номер обращения
    self.request_let_key = QLineEdit(self)
    self.request_let_key.setPlaceholderText("Заявка/номер обращения:")
    # Создаём палитру
    palette = self.request_let_key.palette()
    # Цвет обычного текста (белый)
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    # Цвет placeholder-текста (зелёный)
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    # Применяем палитру к QLineEdit
    self.request_let_key.setPalette(palette)
    right_form.addRow(QLabel("Номер обращения:"), self.request_let_key)

    # Примечание
    self.note_le_key = QLineEdit(self)
    self.note_le_key.setPlaceholderText("Примечание:")
    # Создаём палитру
    palette = self.note_le_key.palette()
    # Цвет обычного текста (белый)
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    # Цвет placeholder-текста (зелёный)
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    # Применяем палитру к QLineEdit
    self.note_le_key.setPalette(palette)
    right_form.addRow(QLabel("Примечание:"), self.note_le_key)

    h_layout.addWidget(right_group, 1)

    # Кнопка для сохранения/обработки данных
    self.save_button = QPushButton("Сохранить", self)
    right_form.addRow(self.save_button)
    self.save_button.clicked.connect(lambda: save_value8(self))

    # Шорткат для Enter
    enter_shortcut = QShortcut(QKeySequence("Return"), page)
    enter_shortcut.activated.connect(lambda: save_value8(self))

    # Кнопка "Назад"
    btn_back = QPushButton("Назад")
    btn_back.clicked.connect(self.go_to_second_page)
    main_layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)

    return page


def save_value8(self):
    status_cb = self.status_cb.currentText()
    nositel_type_cb = self.nositel_type_cb_key.currentText()
    cert_serial_le = self.cert_serial_le_key.text()
    issuer_cb = self.issuer_cb_key.currentText()
    scope_cb = self.scope_cb_key.currentText()
    owner_cb = self.owner_cb_key.currentText()
    vip_cb = self.vip_cb.currentText()
    dateedit1 = self.dateedit1_key.date()
    dateedit2 = self.dateedit2.date()
    additional_cb = self.additional_cb_key.currentText()
    request_let = self.request_let_key.text()
    note_le = self.note_le_key.text()

    dateedit_str = dateedit1.toPyDate().strftime('%Y-%m-%d')
    dateedit2_str = dateedit2.toPyDate().strftime('%Y-%m-%d')
    enter_keys(status_cb, nositel_type_cb, cert_serial_le, issuer_cb, scope_cb, owner_cb, vip_cb, dateedit_str, dateedit2_str, additional_cb, request_let, note_le)
    clear_fields(self)

def clear_fields(self):
    self.status_cb.clearEditText()
    self.nositel_type_cb_key.clearEditText()
    self.serial_le_key.clear()
    self.cert_serial_le_key.clear()
    self.issuer_cb_key.clearEditText()
    self.scope_cb_key.clearEditText()
    self.owner_cb_key.clearEditText()
    self.vip_cb.clearEditText()
    self.dateedit1.setDate(QDate.currentDate())
    self.dateedit2.setDate(QDate.currentDate())
    self.additional_cb_key.clearEditText()
    self.request_let_key.clear()
    self.note_le_key.clear()
