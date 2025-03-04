from datetime import datetime
from PyQt6 import QtWidgets
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout,
    QComboBox, QSizePolicy, QGroupBox, QFormLayout
)
from PyQt6.QtCore import Qt

def create_page7(self) -> QWidget:
    page = QWidget()
    main_layout = QVBoxLayout(page)
    main_layout.setContentsMargins(20, 20, 20, 20)
    main_layout.setSpacing(15)

    # Заголовок
    header_label = QLabel("СКЗИ")
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

    # Наименование ПО СКЗИ
    self.skzi_name_cb = QComboBox(self)
    self.skzi_name_cb.setEditable(True)
    self.skzi_name_cb.setCurrentText("Наименование ПО СКЗИ")
    for option in ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]:
        self.skzi_name_cb.addItem(option)
    left_form.addRow(QLabel("Наименование ПО СКЗИ:"), self.skzi_name_cb)

    # Версия СКЗИ
    self.skzi_version_cb = QComboBox(self)
    self.skzi_version_cb.setEditable(True)
    self.skzi_version_cb.setCurrentText("Версия СКЗИ")
    for option in ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]:
        self.skzi_version_cb.addItem(option)
    left_form.addRow(QLabel("Версия СКЗИ:"), self.skzi_version_cb)

    # Календарь (дата)
    self.dateedit = QtWidgets.QDateEdit(calendarPopup=True)
    self.dateedit.setDateTime(datetime.today())
    left_form.addRow(QLabel("Дата:"), self.dateedit)

    # Дата и номер документа, сопроводительного письма
    self.doc_info_le = QLineEdit(self)
    self.doc_info_le.setPlaceholderText("Дата и номер документа, сопроводительного письма")
    self.doc_info_le.setMinimumSize(250, 40)
    self.doc_info_le.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    left_form.addRow(QLabel("Документ:"), self.doc_info_le)

    # ФИО владельца, бизнес-процесс
    self.owner_fio_le = QLineEdit(self)
    self.owner_fio_le.setPlaceholderText("ФИО владельца, бизнес-процесс")
    self.owner_fio_le.setMinimumSize(250, 40)
    self.owner_fio_le.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    left_form.addRow(QLabel("Владелец/процесс:"), self.owner_fio_le)

    h_layout.addWidget(left_group, 1)

    # ---------- ПРАВЫЙ БЛОК ----------
    right_group = QGroupBox("Дополнительные сведения")
    right_form = QFormLayout()
    right_form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
    right_group.setLayout(right_form)

    # Регистрационный (серийный) номер
    self.reg_number_le = QLineEdit(self)
    self.reg_number_le.setPlaceholderText("Регистрационный (серийный) номер")
    self.reg_number_le.setMinimumSize(250, 40)
    self.reg_number_le.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    right_form.addRow(QLabel("Рег. номер:"), self.reg_number_le)

    # От кого получены
    self.from_whom_cb = QComboBox(self)
    self.from_whom_cb.setEditable(True)
    self.from_whom_cb.setCurrentText("От кого получены")
    for option in ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]:
        self.from_whom_cb.addItem(option)
    right_form.addRow(QLabel("От кого получены:"), self.from_whom_cb)

    # Примечание
    self.note_cb = QComboBox(self)
    self.note_cb.setEditable(True)
    self.note_cb.setCurrentText("Примечание:")
    for option in ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]:
        self.note_cb.addItem(option)
    right_form.addRow(QLabel("Примечание:"), self.note_cb)

    # Дополнительно
    self.additional_le = QLineEdit(self)
    self.additional_le.setPlaceholderText("Дополнительно")
    self.additional_le.setStyleSheet("""
        QLineEdit {
            font-size: 16px;
            color: rgb(118, 120, 122);
            padding: 5px;
        }
    """)
    right_form.addRow(QLabel("Дополнительно:"), self.additional_le)

    # Номер сертификата соответствия
    self.certnum_le = QLineEdit(self)
    self.certnum_le.setPlaceholderText("Номер сертификата соответствия")
    self.certnum_le.setStyleSheet("""
        QLineEdit {
            font-size: 16px;
            color: rgb(118, 120, 122);
            padding: 5px;
        }
    """)
    right_form.addRow(QLabel("Сертификат:"), self.certnum_le)

    # Дополнительная дата (если нужно)
    self.dateedit2 = QtWidgets.QDateEdit(calendarPopup=True)
    self.dateedit2.setDateTime(datetime.today())
    right_form.addRow(QLabel("Доп. дата:"), self.dateedit2)

    h_layout.addWidget(right_group, 1)

    # Шорткат для Enter
    enter_shortcut = QShortcut(QKeySequence("Return"), page)
    enter_shortcut.activated.connect(self.getandgo2)

    # Кнопка "Назад"
    btn_back = QPushButton("Назад")
    btn_back.clicked.connect(self.go_to_second_page)
    main_layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)

    return page
