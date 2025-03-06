from datetime import datetime
from PyQt6 import QtWidgets
from PyQt6.QtGui import QShortcut, QKeySequence, QPalette, QColor
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout,
    QComboBox, QSizePolicy, QGroupBox, QFormLayout
)
from PyQt6.QtCore import Qt

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
    self.nositel_type_cb = QComboBox(self)
    self.nositel_type_cb.setEditable(True)
    line_edit = self.nositel_type_cb.lineEdit()
    line_edit.setPlaceholderText("Тип носителя")
    # Создаём палитру
    palette = line_edit.palette()
    # Цвет обычного текста (чёрный)
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    # Цвет placeholder-текста (зелёный)
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    # Применяем палитру к QLineEdit
    line_edit.setPalette(palette)
    for option in ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]:
        self.nositel_type_cb.addItem(option)
    self.nositel_type_cb.clearEditText()

    left_form.addRow(QLabel("Тип носителя:"), self.nositel_type_cb)

    # Серийный номер
    self.serial_le = QLineEdit(self)
    self.serial_le.setPlaceholderText("Серийный номер:")
    # Создаём палитру
    palette = self.serial_le.palette()
    # Цвет обычного текста (белый)
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    # Цвет placeholder-текста (зелёный)
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    # Применяем палитру к QLineEdit
    self.serial_le.setPalette(palette)
    left_form.addRow(QLabel("Серийный номер:"), self.serial_le)

    # Серийный номер сертификата
    self.cert_serial_le = QLineEdit(self)
    self.cert_serial_le.setPlaceholderText("Серийный номер сертификата:")
    # Создаём палитру
    palette = self.cert_serial_le.palette()
    # Цвет обычного текста (белый)
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    # Цвет placeholder-текста (зелёный)
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    # Применяем палитру к QLineEdit
    self.cert_serial_le.setPalette(palette)
    left_form.addRow(QLabel("Сер. номер сертификата:"), self.cert_serial_le)

    # Выдавший УЦ
    self.issuer_cb = QComboBox(self)
    self.issuer_cb.setEditable(True)
    line_edit = self.issuer_cb.lineEdit()
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
        self.issuer_cb.addItem(option)
    self.issuer_cb.clearEditText()
    left_form.addRow(QLabel("УЦ:"), self.issuer_cb)

    # Область действия / наименование ЭДО
    self.scope_cb = QComboBox(self)
    self.scope_cb.setEditable(True)
    line_edit = self.scope_cb.lineEdit()
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
        self.scope_cb.addItem(option)
    self.scope_cb.clearEditText()
    left_form.addRow(QLabel("Область/ЭДО:"), self.scope_cb)

    # ФИО владельца
    self.owner_cb = QComboBox(self)
    self.owner_cb.setEditable(True)
    line_edit = self.owner_cb.lineEdit()
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
        self.owner_cb.addItem(option)
    self.owner_cb.clearEditText()
    left_form.addRow(QLabel("Владелец:"), self.owner_cb)

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
    self.dateedit1 = QtWidgets.QDateEdit(calendarPopup=True)
    self.dateedit1.setDateTime(datetime.today())
    right_form.addRow(QLabel("Дата начала:"), self.dateedit1)

    # Дата (2)
    self.dateedit2 = QtWidgets.QDateEdit(calendarPopup=True)
    self.dateedit2.setDateTime(datetime.today())
    right_form.addRow(QLabel("Дата окончания:"), self.dateedit2)

    # Дополнительно
    self.additional_cb = QComboBox(self)
    self.additional_cb.setEditable(True)
    line_edit = self.additional_cb.lineEdit()
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
        self.additional_cb.addItem(option)
    self.additional_cb.clearEditText()
    right_form.addRow(QLabel("Дополнительно:"), self.additional_cb)

    # Заявка/номер обращения
    self.request_let = QLineEdit(self)
    self.request_let.setPlaceholderText("Заявка/номер обращения:")
    # Создаём палитру
    palette = self.request_let.palette()
    # Цвет обычного текста (белый)
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    # Цвет placeholder-текста (зелёный)
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    # Применяем палитру к QLineEdit
    self.request_let.setPalette(palette)
    right_form.addRow(QLabel("Номер обращения:"), self.request_let)

    # Примечание
    self.note_le = QLineEdit(self)
    self.note_le.setPlaceholderText("Примечание:")
    # Создаём палитру
    palette = self.note_le.palette()
    # Цвет обычного текста (белый)
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    # Цвет placeholder-текста (зелёный)
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    # Применяем палитру к QLineEdit
    self.note_le.setPalette(palette)
    right_form.addRow(QLabel("Примечание:"), self.note_le)

    h_layout.addWidget(right_group, 1)

    # Кнопка для сохранения/обработки данных
    self.save_button = QPushButton("Сохранить", self)
    right_form.addRow(self.save_button)
    self.save_button.clicked.connect(self.save_values8)

    # Шорткат для Enter
    enter_shortcut = QShortcut(QKeySequence("Return"), page)
    enter_shortcut.activated.connect(self.save_values8)

    # Кнопка "Назад"
    btn_back = QPushButton("Назад")
    btn_back.clicked.connect(self.go_to_second_page)
    main_layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)

    return page
