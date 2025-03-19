from datetime import datetime
from PyQt6 import QtWidgets
from PyQt6.QtGui import QShortcut, QKeySequence, QPalette, QColor
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout,
    QComboBox, QSizePolicy, QGroupBox, QFormLayout
)
from PyQt6.QtCore import Qt

from logic.db import enter_sczy


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

    self.skzi_name_cb = QComboBox(self)
    self.skzi_name_cb.setEditable(True)
    # Получаем встроенный QLineEdit
    line_edit = self.skzi_name_cb.lineEdit()
    line_edit.setPlaceholderText("Наименование ПО")
    # Создаём палитру
    palette = line_edit.palette()
    # Цвет обычного текста
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    # Цвет placeholder-текста (зелёный)
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(70, 130, 20))
    # Применяем палитру к QLineEdit
    line_edit.setPalette(palette)
    # Добавляем варианты
    for option in ["Option 2", "Option 3", "Option 4", "Option 5"]:
        self.skzi_name_cb.addItem(option)
    # Сбрасываем текущий текст, чтобы поле было пустым
    self.skzi_name_cb.clearEditText()
    left_form.addRow(QLabel("Наименование ПО:"), self.skzi_name_cb)

    # Создаём редактируемый QComboBox
    self.skzi_type = QComboBox(self)
    self.skzi_type.setEditable(False)
    # Создаём палитру
    palette = line_edit.palette()
    # Цвет обычного текста
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    # Цвет placeholder-текста (зелёный)
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    # Применяем палитру к QLineEdit
    line_edit.setPalette(palette)
    # Добавляем варианты в QComboBox
    for option in ["ПО", "ПАК"]:
        self.skzi_type.addItem(option)
    # Очищаем поле, чтобы placeholder-текст был виден сразу
    self.skzi_type.clearEditText()
    left_form.addRow(QLabel("Тип СКЗИ:"), self.skzi_type)

    # Версия СКЗИ
    self.skzi_version_cb = QComboBox(self)
    self.skzi_version_cb.setEditable(True)
    self.skzi_version_cb.setCurrentText("Версия СКЗИ")
    line_edit = self.skzi_version_cb.lineEdit()
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
        self.skzi_version_cb.addItem(option)
    self.skzi_version_cb.clearEditText()
    left_form.addRow(QLabel("Версия СКЗИ:"), self.skzi_version_cb)

    # Календарь (дата)
    self.dateedit = QtWidgets.QDateEdit(calendarPopup=True)
    self.dateedit.setDateTime(datetime.today())
    left_form.addRow(QLabel("Дата:"), self.dateedit)

    # Местанохождение ПО
    self.location = QLineEdit(self)
    # Устанавливаем placeholder
    self.location.setPlaceholderText("Местанохождение (ТОМ)")
    # Создаём палитру
    palette = self.location.palette()
    # Цвет обычного текста (белый)
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    # Цвет placeholder-текста (зелёный)
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    # Применяем палитру к QLineEdit
    self.location.setPalette(palette)
    # Добавляем в форму
    left_form.addRow(QLabel("ТОМ:"), self.location)


    # Дата и номер документа, сопроводительного письма
    self.doc_info_le = QLineEdit(self)
    # Устанавливаем placeholder
    self.doc_info_le.setPlaceholderText("Дата и номер документа, сопроводительного письма")
    # Создаём палитру
    palette = self.doc_info_le.palette()
    # Цвет обычного текста (белый)
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    # Цвет placeholder-текста (зелёный)
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    # Применяем палитру к QLineEdit
    self.doc_info_le.setPalette(palette)
    # Добавляем в форму
    left_form.addRow(QLabel("Документ:"), self.doc_info_le)

    # Договор
    self.contract = QLineEdit(self)
    # Устанавливаем placeholder
    self.contract.setPlaceholderText("Договор")
    # Создаём палитру
    palette = self.contract.palette()
    # Цвет обычного текста (белый)
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    # Цвет placeholder-текста (зелёный)
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    # Применяем палитру к QLineEdit
    self.contract.setPalette(palette)
    # Добавляем в форму
    left_form.addRow(QLabel("Договор:"), self.contract)

    # ФИО владельца, бизнес-процесс
    self.owner_fio_le = QLineEdit(self)
    self.owner_fio_le.setPlaceholderText("ФИО владельца, бизнес-процесс")
    palette = self.owner_fio_le.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    self.owner_fio_le.setPalette(palette)
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
    palette = self.reg_number_le.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    self.reg_number_le.setPalette(palette)
    right_form.addRow(QLabel("Рег. номер:"), self.reg_number_le)

    # От кого получены
    self.from_whom_cb = QComboBox(self)
    self.from_whom_cb.setEditable(True)
    line_edit = self.from_whom_cb.lineEdit()
    line_edit.setPlaceholderText("От кого получены:")
    # Создаём палитру
    palette = line_edit.palette()
    # Цвет обычного текста
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    # Цвет placeholder-текста (зелёный)
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(70, 130, 20))
    # Применяем палитру к QLineEdit
    line_edit.setPalette(palette)
    for option in ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]:
        self.from_whom_cb.addItem(option)
    # Сбрасываем текущий текст, чтобы поле было пустым
    self.from_whom_cb.clearEditText()
    right_form.addRow(QLabel("От кого получены:"), self.from_whom_cb)

    # Владельцы
    self.owners = QComboBox(self)
    self.owners.setEditable(True)
    line_edit = self.owners.lineEdit()
    line_edit.setPlaceholderText("Владельцы")
    # Создаём палитру
    palette = line_edit.palette()
    # Цвет обычного текста
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    # Цвет placeholder-текста (зелёный)
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(70, 130, 20))
    # Применяем палитру к QLineEdit
    line_edit.setPalette(palette)
    for option in ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]:
        self.owners.addItem(option)
    # Сбрасываем текущий текст, чтобы поле было пустым
    self.owners.clearEditText()
    right_form.addRow(QLabel("Владельцы"), self.owners)

    # От кого получены
    self.buss_proc = QComboBox(self)
    self.buss_proc.setEditable(True)
    line_edit = self.buss_proc.lineEdit()
    line_edit.setPlaceholderText("Бизнес процессы")
    # Создаём палитру
    palette = line_edit.palette()
    # Цвет обычного текста
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    # Цвет placeholder-текста (зелёный)
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(70, 130, 20))
    # Применяем палитру к QLineEdit
    line_edit.setPalette(palette)
    for option in ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]:
        self.buss_proc.addItem(option)
    # Сбрасываем текущий текст, чтобы поле было пустым
    self.buss_proc.clearEditText()
    right_form.addRow(QLabel("Бизнес процессы"), self.buss_proc)

     # Примечание
    self.note_cb = QComboBox(self)
    self.note_cb.setEditable(True)
    line_edit = self.note_cb.lineEdit()
    line_edit.setPlaceholderText("Примечание:")
    # Создаём палитру
    palette = line_edit.palette()
    # Цвет обычного текста
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    # Цвет placeholder-текста (зелёный)
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(70, 130, 20))
    # Применяем палитру к QLineEdit
    line_edit.setPalette(palette)
    for option in ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]:
        self.note_cb.addItem(option)
    # Сбрасываем текущий текст, чтобы поле было пустым
    self.note_cb.clearEditText()
    right_form.addRow(QLabel("Примечание:"), self.note_cb)


    # Дополнительно
    self.additional_le = QLineEdit(self)
    self.additional_le.setPlaceholderText("Дополнительно")
    palette = self.additional_le.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    self.additional_le.setPalette(palette)
    right_form.addRow(QLabel("Дополнительно:"), self.additional_le)

    # Номер сертификата соответствия
    self.certnum_le = QLineEdit(self)
    self.certnum_le.setPlaceholderText("Номер сертификата соответствия")
    palette = self.certnum_le.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    self.certnum_le.setPalette(palette)
    right_form.addRow(QLabel("Сертификат:"), self.certnum_le)

    # Дополнительная дата (если нужно)
    self.dateedit2 = QtWidgets.QDateEdit(calendarPopup=True)
    self.dateedit2.setDateTime(datetime.today())
    right_form.addRow(QLabel("Доп. дата:"), self.dateedit2)

    h_layout.addWidget(right_group, 1)

    # Шорткат для Enter
    enter_shortcut = QShortcut(QKeySequence("Return"), page)
    enter_shortcut.activated.connect(lambda: save_value7(self))

    # Кнопка для сохранения/обработки данных
    self.save_button = QPushButton("Сохранить", self)
    right_form.addRow(self.save_button)
    self.save_button.clicked.connect(lambda: save_value7(self))

    # Кнопка "Назад"
    btn_back = QPushButton("Назад")
    btn_back.clicked.connect(self.go_to_second_page)
    main_layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)

    return page


def save_value7(self):
    # Сбор данных из виджетов
    skzi_name = self.skzi_name_cb.currentText()               # Наименование ПО
    skzi_type = self.skzi_type.currentText()                    # Тип СКЗИ
    skzi_version = self.skzi_version_cb.currentText()           # Версия СКЗИ
    date_str = self.dateedit.date().toPyDate().strftime('%Y-%m-%d')  # Дата
    reg_number = self.reg_number_le.text()                      # Рег. номер
    location_text = self.location.text()                        # Местонахождение (ТОМ)
    from_whom = self.from_whom_cb.currentText()                 # От кого получены
    doc_info = self.doc_info_le.text()                          # Документ
    contract = self.contract.text()                             # Договор
    owner_fio = self.owner_fio_le.text()                        # Владелец/процесс
    owners = self.owners.currentText()                          # Владельцы (новое поле)
    buss_proc = self.buss_proc.currentText()                    # Бизнес процессы
    additional = self.additional_le.text()                      # Дополнительно
    note = self.note_cb.currentText()                           # Примечание
    certnum = self.certnum_le.text()                            # Сертификат
    dateedit2_str = self.dateedit2.date().toPyDate().strftime('%Y-%m-%d')  # Доп. дата

    enter_sczy(
        skzi_name,
        skzi_type,
        skzi_version,
        date_str,
        reg_number,
        location_text,
        from_whom,
        doc_info,
        contract,
        owner_fio,
        owners,
        buss_proc,
        additional,
        note,
        certnum,
        dateedit2_str
    )
    clear_fields(self)

def clear_fields(self):
    self.skzi_name_cb.clear()
    # version of SCZY
    self.skzi_version_cb.clear()
    # date give
    self.dateedit.date()
    # docs
    self.doc_info_le.clear()
    # owner
    self.owner_fio_le.clear()
    # reg number
    self.reg_number_le.clear()
    # from who
    self.from_whom_cb.clear()
    # note
    self.note_cb.clear()
    # addit
    self.additional_le.clear()
    #sertification
    self.certnum_le.clear()
    # dop date
    self.dateedit2.clear()
    # owners
    self.owners.clearEditText()
    # location
    self.location.clear()
    # contract
    self.contract.clear()
    # buss proc
    self.buss_proc.clearEditText()