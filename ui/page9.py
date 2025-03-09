from datetime import datetime
from PyQt6 import QtWidgets
from PyQt6.QtGui import QShortcut, QKeySequence, QPalette, QColor
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
    palette = self.request_le.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    self.request_le.setPalette(palette)
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
    # Создаём палитру
    line_edit = self.nositel_serial_cb.lineEdit()
    palette = line_edit.palette()
    # Цвет обычного текста (чёрный)
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    # Цвет placeholder-текста (зелёный)
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    # Применяем палитру к QLineEdit
    line_edit.setPalette(palette)
    for option in ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]:
        self.nositel_serial_cb.addItem(option)
    self.nositel_serial_cb.clearEditText()
    left_form.addRow(QLabel("Серийный номер:"), self.nositel_serial_cb)

    # Номер ключа
    self.key_number_le = QLineEdit(self)
    self.key_number_le.setPlaceholderText("Номер ключа:")
    palette = self.key_number_le.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    self.key_number_le.setPalette(palette)
    left_form.addRow(QLabel("Номер ключа:"), self.key_number_le)

    # Выдавший УЦ
    self.issuer_cb = QComboBox(self)
    self.issuer_cb.setEditable(True)
    line_edit = self.issuer_cb.lineEdit()
    line_edit.setPlaceholderText("Выдавший УЦ")
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

    # ---------- ПРАВЫЙ БЛОК ----------
    right_group = QGroupBox("Дополнительно")
    right_form = QFormLayout()
    right_form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
    right_group.setLayout(right_form)

    # Область действия / наименование ЭДО
    self.scope_cb = QComboBox(self)
    self.scope_cb.setEditable(True)
    self.scope_cb.setCurrentText("Область действия / наименование ЭДО")
    line_edit = self.scope_cb.lineEdit()
    line_edit.setPlaceholderText("Область действия / наименование ЭДО")
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
    right_form.addRow(QLabel("Область/ЭДО:"), self.scope_cb)

    # ФИО владельца
    self.owner_cb = QComboBox(self)
    self.owner_cb.setEditable(True)
    self.owner_cb.setCurrentText("ФИО владельца")
    # Создаём палитру
    line_edit = self.owner_cb.lineEdit()
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
    palette = self.additional1_le.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    self.additional1_le.setPalette(palette)
    right_form.addRow(QLabel("Дополнительно:"), self.additional1_le)

    # Дополнительно 2
    self.additional2_le = QLineEdit(self)
    self.additional2_le.setPlaceholderText("Дополнительно:")
    palette = self.additional2_le.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    self.additional2_le.setPalette(palette)
    right_form.addRow(QLabel("Дополнительно:"), self.additional2_le)

    h_layout.addWidget(right_group, 1)

    # Кнопка для сохранения/обработки данных
    self.save_button = QPushButton("Сохранить", self)
    right_form.addRow(self.save_button)
    self.save_button.clicked.connect(self.save_values7)

    # Шорткат для Enter
    enter_shortcut = QShortcut(QKeySequence("Return"), page)
    enter_shortcut.activated.connect(self.getandgo2)

    # Кнопка "Назад"
    btn_back = QPushButton("Назад")
    btn_back.clicked.connect(self.go_to_second_page)
    main_layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)

    return page
