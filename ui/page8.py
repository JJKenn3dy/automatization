from datetime import datetime
from PyQt6 import QtWidgets
from PyQt6.QtGui import QShortcut, QKeySequence, QPalette, QColor
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout,
    QComboBox, QSizePolicy, QGroupBox, QFormLayout, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
)
from PyQt6.QtCore import Qt, QDate, QTimer

from logic.db import enter_keys

def create_page8(self) -> QWidget:
    page = QWidget()
    # Устанавливаем общий тёмный фон и белый текст для страницы
    page.setStyleSheet("background-color: #121212; color: white;")
    main_layout = QVBoxLayout(page)
    main_layout.setContentsMargins(20, 20, 20, 20)
    main_layout.setSpacing(15)

    # Кнопка "Назад"
    btn_back = QPushButton("Назад")
    btn_back.setStyleSheet("background-color: #333333; color: white; font-size: 15px; border: 1px solid #555; border-radius: 4px;")
    btn_back.clicked.connect(self.go_to_second_page)
    btn_back.setMinimumSize(150, 30)
    main_layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignLeft)

    # Заголовок
    header_label = QLabel("Ключи УКЭП")
    header_label.setWordWrap(True)
    header_label.setStyleSheet("font-size: 20px; color: white;")
    header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    main_layout.addWidget(header_label)

    # Горизонтальный лэйаут для левого и правого блоков
    h_layout = QHBoxLayout()
    h_layout.setSpacing(30)
    main_layout.addLayout(h_layout)

    # ---------- ЛЕВЫЙ БЛОК ----------
    left_group = QGroupBox("Основные данные")
    left_group.setStyleSheet("""
        QGroupBox {
            background-color: #1e1e1e;
            border: 1px solid #444;
            border-radius: 5px;
            margin-top: 10px;
            padding: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 3px;
            color: white;
        }
        QLabel {
            color: white;
        }
    """)
    left_form = QFormLayout()
    left_form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
    left_group.setLayout(left_form)

    # Статус да/нет
    self.status_cb = QComboBox(self)
    self.status_cb.setEditable(False)
    self.status_cb.setCurrentText("Статус да/нет")
    self.status_cb.addItems(["Да", "Нет"])
    self.status_cb.setStyleSheet("""
        QComboBox {
            background-color: #1e1e1e;
            color: white;
            border: 1px solid #444;
            border-radius: 4px;
            padding: 2px;
        }
        QComboBox QAbstractItemView {
            background-color: #121212;
            color: white;
            selection-background-color: #444;
            selection-color: white;
        }
    """)
    left_form.addRow(QLabel("Статус:"), self.status_cb)

    # Тип носителя + его серийный номер
    self.nositel_type_cb_key = QComboBox(self)
    self.nositel_type_cb_key.setEditable(True)
    line_edit = self.nositel_type_cb_key.lineEdit()
    line_edit.setPlaceholderText("Тип носителя + его серийный номер")
    palette = line_edit.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    line_edit.setPalette(palette)
    self.nositel_type_cb_key.setStyleSheet("""
        QComboBox {
            background-color: #1e1e1e;
            color: white;
            border: 1px solid #444;
            border-radius: 4px;
            padding: 2px;
        }
        QComboBox QAbstractItemView {
            background-color: #121212;
            color: white;
            selection-background-color: #444;
            selection-color: white;
        }
    """)
    for option in ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]:
        self.nositel_type_cb_key.addItem(option)
    self.nositel_type_cb_key.clearEditText()
    left_form.addRow(QLabel("Тип носителя + серийный номер:"), self.nositel_type_cb_key)

    # Серийный номер
    self.serial_le_key = QLineEdit(self)
    self.serial_le_key.setPlaceholderText("Серийный номер сертификата:")
    palette = self.serial_le_key.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    self.serial_le_key.setPalette(palette)
    self.serial_le_key.setStyleSheet("background-color: #1e1e1e; border: 1px solid #444; border-radius: 4px; padding: 2px;")
    left_form.addRow(QLabel("Серийный номер сертификата:"), self.serial_le_key)

    # Выдавший УЦ
    self.issuer_cb_key = QComboBox(self)
    self.issuer_cb_key.setEditable(True)
    line_edit = self.issuer_cb_key.lineEdit()
    line_edit.setPlaceholderText("УЦ:")
    palette = line_edit.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    line_edit.setPalette(palette)
    self.issuer_cb_key.setStyleSheet("""
        QComboBox {
            background-color: #1e1e1e;
            color: white;
            border: 1px solid #444;
            border-radius: 4px;
            padding: 2px;
        }
        QComboBox QAbstractItemView {
            background-color: #121212;
            color: white;
            selection-background-color: #444;
            selection-color: white;
        }
    """)
    for option in ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]:
        self.issuer_cb_key.addItem(option)
    self.issuer_cb_key.clearEditText()
    left_form.addRow(QLabel("УЦ:"), self.issuer_cb_key)

    # Область действия / наименование ЭДО
    self.scope_cb_key = QComboBox(self)
    self.scope_cb_key.setEditable(True)
    line_edit = self.scope_cb_key.lineEdit()
    line_edit.setPlaceholderText("Область/ЭДО:")
    palette = line_edit.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    line_edit.setPalette(palette)
    self.scope_cb_key.setStyleSheet("""
        QComboBox {
            background-color: #1e1e1e;
            color: white;
            border: 1px solid #444;
            border-radius: 4px;
            padding: 2px;
        }
        QComboBox QAbstractItemView {
            background-color: #121212;
            color: white;
            selection-background-color: #444;
            selection-color: white;
        }
    """)
    for option in ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]:
        self.scope_cb_key.addItem(option)
    self.scope_cb_key.clearEditText()
    left_form.addRow(QLabel("Область/ЭДО:"), self.scope_cb_key)

    # ФИО владельца
    self.owner_cb_key = QComboBox(self)
    self.owner_cb_key.setEditable(True)
    line_edit = self.owner_cb_key.lineEdit()
    line_edit.setPlaceholderText("Владелец:")
    palette = line_edit.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    line_edit.setPalette(palette)
    self.owner_cb_key.setStyleSheet("""
        QComboBox {
            background-color: #1e1e1e;
            color: white;
            border: 1px solid #444;
            border-radius: 4px;
            padding: 2px;
        }
        QComboBox QAbstractItemView {
            background-color: #121212;
            color: white;
            selection-background-color: #444;
            selection-color: white;
        }
    """)
    for option in ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]:
        self.owner_cb_key.addItem(option)
    self.owner_cb_key.clearEditText()
    left_form.addRow(QLabel("Владелец:"), self.owner_cb_key)

    h_layout.addWidget(left_group, 1)

    # ---------- ПРАВЫЙ БЛОК ----------
    right_group = QGroupBox("Дополнительно")
    right_group.setStyleSheet("""
        QGroupBox {
            background-color: #1e1e1e;
            border: 1px solid #444;
            border-radius: 5px;
            margin-top: 10px;
            padding: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 3px;
            color: white;
        }
    """)
    right_form = QFormLayout()
    right_form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
    right_group.setLayout(right_form)

    # VIP / Critical
    self.vip_cb = QComboBox(self)
    self.vip_cb.setEditable(False)
    self.vip_cb.setCurrentText("VIP/Critical")
    self.vip_cb.addItems(["VIP", "Critical"])
    self.vip_cb.setStyleSheet("""
        QComboBox {
            background-color: #1e1e1e;
            color: white;
            border: 1px solid #444;
            border-radius: 4px;
            padding: 2px;
        }
        QComboBox QAbstractItemView {
            background-color: #121212;
            color: white;
            selection-background-color: #444;
            selection-color: white;
        }
    """)
    right_form.addRow(QLabel("VIP/Critical:"), self.vip_cb)

    # Дата (1)
    self.dateedit1_key = QtWidgets.QDateEdit(calendarPopup=True)
    self.dateedit1_key.setDateTime(datetime.today())
    self.dateedit1_key.setStyleSheet("""
        QDateEdit {
            background-color: #1e1e1e;
            color: white;
            border: 1px solid #444;
            border-radius: 4px;
            padding: 2px;
        }
        QDateEdit::drop-down { background-color: #1e1e1e; }
        QCalendarWidget {
            background-color: #1e1e1e;
            color: white;
            border: 1px solid #444;
        }
        QCalendarWidget QAbstractItemView:enabled {
            background-color: #121212;
            color: #e0e0e0;
            selection-background-color: #444;
            selection-color: white;
        }
    """)
    right_form.addRow(QLabel("Дата начала:"), self.dateedit1_key)

    # Дата (2)
    self.dateedit2 = QtWidgets.QDateEdit(calendarPopup=True)
    self.dateedit2.setDateTime(datetime.today())
    self.dateedit2.setStyleSheet("""
        QDateEdit {
            background-color: #1e1e1e;
            color: white;
            border: 1px solid #444;
            border-radius: 4px;
            padding: 2px;
        }
        QDateEdit::drop-down { background-color: #1e1e1e; }
        QCalendarWidget {
            background-color: #1e1e1e;
            color: white;
            border: 1px solid #444;
        }
        QCalendarWidget QAbstractItemView:enabled {
            background-color: #121212;
            color: #e0e0e0;
            selection-background-color: #444;
            selection-color: white;
        }
    """)
    right_form.addRow(QLabel("Дата окончания:"), self.dateedit2)

    # Дополнительно
    self.additional_cb_key = QComboBox(self)
    self.additional_cb_key.setEditable(True)
    line_edit = self.additional_cb_key.lineEdit()
    line_edit.setPlaceholderText("Дополнительно:")
    palette = line_edit.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    line_edit.setPalette(palette)
    self.additional_cb_key.setStyleSheet("""
        QComboBox {
            background-color: #1e1e1e;
            color: white;
            border: 1px solid #444;
            border-radius: 4px;
            padding: 2px;
        }
        QComboBox QAbstractItemView {
            background-color: #121212;
            color: white;
            selection-background-color: #444;
            selection-color: white;
        }
    """)
    for option in ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]:
        self.additional_cb_key.addItem(option)
    self.additional_cb_key.clearEditText()
    right_form.addRow(QLabel("Дополнительно:"), self.additional_cb_key)

    # Заявка/номер обращения
    self.request_let_key = QLineEdit(self)
    self.request_let_key.setPlaceholderText("Заявка/номер обращения:")
    palette = self.request_let_key.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    self.request_let_key.setPalette(palette)
    self.request_let_key.setStyleSheet("background-color: #1e1e1e; border: 1px solid #444; border-radius: 4px; padding: 2px;")
    right_form.addRow(QLabel("Номер обращения:"), self.request_let_key)

    # Примечание
    self.note_le_key = QLineEdit(self)
    self.note_le_key.setPlaceholderText("Примечание:")
    palette = self.note_le_key.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    self.note_le_key.setPalette(palette)
    self.note_le_key.setStyleSheet("background-color: #1e1e1e; border: 1px solid #444; border-radius: 4px; padding: 2px;")
    right_form.addRow(QLabel("Примечание:"), self.note_le_key)

    h_layout.addWidget(right_group, 1)

    # Кнопка для сохранения/обработки данных
    self.save_button = QPushButton("Сохранить", self)
    self.save_button.setStyleSheet("background-color: #333333; color: white; font-size: 15px; border: 1px solid #555; border-radius: 4px;")
    right_form.addRow(self.save_button)
    self.save_button.clicked.connect(lambda: save_value8(self))

    # Шорткат для Enter
    enter_shortcut = QShortcut(QKeySequence("Return"), page)
    enter_shortcut.activated.connect(lambda: save_value8(self))

    escape_shortcut = QShortcut(QKeySequence("Escape"), page)
    escape_shortcut.activated.connect(self.go_to_second_page)



    # --- Добавляем виджет с таблицей и поиском для KeysTable ---
    data_table_widget = create_data_table8(self)
    main_layout.addWidget(data_table_widget)

    # --- Создаем таймер для периодического обновления таблицы ---
    self.refresh_timer = QTimer(self)
    self.refresh_timer.setInterval(60000)  # Обновление каждые 60 секунд
    self.refresh_timer.timeout.connect(lambda: load_data8(self))
    self.refresh_timer.start()

    return page


def create_data_table8(self) -> QWidget:
    """
    Создает виджет с поисковой строкой и таблицей для отображения последних записей из таблицы KeysTable.
    """
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setSpacing(5)

    # Поисковая строка
    search_layout = QHBoxLayout()
    search_label = QLabel("Поиск:")
    self.search_line8 = QLineEdit()
    self.search_line8.setPlaceholderText("Введите текст для поиска...")
    search_layout.addWidget(search_label)
    search_layout.addWidget(self.search_line8)
    layout.addLayout(search_layout)


    # Таблица для отображения данных из KeysTable
    self.table_widget8 = QTableWidget()
    headers = [
        "ID", "Статус", "Тип", "Серийный номер", "УЦ",
        "Область", "Владелец", "VIP/Critical",
        "Дата начала", "Дата окончания", "Дополнительно", "Номер обращения", "Примечание"
    ]
    self.table_widget8.setColumnCount(len(headers))
    self.table_widget8.setHorizontalHeaderLabels(headers)

    self.table_widget8.horizontalHeader().setStretchLastSection(True)
    self.table_widget8.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    layout.addWidget(self.table_widget8)

    # Обновление таблицы при изменении текста поиска
    self.search_line8.textChanged.connect(lambda: load_data8(self))
    # Первоначальная загрузка данных
    load_data8(self)

    return widget


def load_data8(self):
    """
    Загружает из базы данных последние 500 записей из таблицы KeysTable.
    При наличии текста в поиске выполняется фильтрация по нескольким полям.
    """
    search_text = self.search_line8.text().strip()
    try:
        import pymysql
        connection = pymysql.connect(
            host="localhost",
            port=3306,
            user="newuser",
            password="852456qaz",
            database="IB",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = connection.cursor()
        if search_text:
            query = """
                SELECT * FROM KeysTable
                WHERE CAST(ID AS CHAR) LIKE %s 
                   OR status LIKE %s 
                   OR type LIKE %s 
                   OR cert_serial_le LIKE %s 
                   OR owner LIKE %s 
                   OR scope_using LIKE %s 
                   OR owner_fullname LIKE %s 
                   OR VIP_Critical LIKE %s
                ORDER BY ID DESC
                LIMIT 1500
            """
            like_pattern = f"%{search_text}%"
            cursor.execute(query, (like_pattern, like_pattern, like_pattern, like_pattern,
                                     like_pattern, like_pattern, like_pattern, like_pattern))
        else:
            query = "SELECT * FROM KeysTable ORDER BY ID DESC LIMIT 1500"
            cursor.execute(query)
        results = cursor.fetchall()
        connection.close()

        self.table_widget8.setRowCount(len(results))
        for row_idx, row_data in enumerate(results):
            # Порядок колонок согласно структуре KeysTable:
            # ID, status, type, cert_serial_le, owner, scope_using, owner_fullname,
            # VIP_Critical, start_date, date_end, additional, number_request, note
            columns = [
                row_data.get("ID"),
                row_data.get("status"),
                row_data.get("type"),
                row_data.get("cert_serial_le"),
                row_data.get("owner"),
                row_data.get("scope_using"),
                row_data.get("owner_fullname"),
                row_data.get("VIP_Critical"),
                row_data.get("start_date"),
                row_data.get("date_end"),
                row_data.get("additional"),
                row_data.get("number_request"),
                row_data.get("note"),
            ]
            for col_idx, value in enumerate(columns):
                item = QTableWidgetItem(str(value) if value is not None else "")
                self.table_widget8.setItem(row_idx, col_idx, item)
    except Exception as e:
        print("Ошибка загрузки данных для KeysTable:", e)


def save_value8(self):
    errors = []

    status_cb = self.status_cb.currentText()
    nositel_type_cb = self.nositel_type_cb_key.currentText()
    if len(nositel_type_cb) == 0:
        errors.append("Поле 'Номер' должен не быть пустым")
    cert_serial_le = self.serial_le_key.text()
    if len(cert_serial_le) == 0:
        errors.append("Поле 'cert_serial_le' должен не быть пустым")
    issuer_cb = self.issuer_cb_key.currentText()
    if len(issuer_cb) == 0:
        errors.append("Поле 'issuer_cb' должен не быть пустым")
    scope_cb = self.scope_cb_key.currentText()
    if len(scope_cb) == 0:
        errors.append("Поле 'scope_cb' должен не быть пустым")
    owner_cb = self.owner_cb_key.currentText()
    if len(owner_cb) == 0:
        errors.append("Поле 'owner_cb' должен не быть пустым")
    vip_cb = self.vip_cb.currentText()
    if len(vip_cb) == 0:
        errors.append("Поле 'vip_cb' должен не быть пустым")
    dateedit1 = self.dateedit1_key.date()
    dateedit2 = self.dateedit2.date()
    additional_cb = self.additional_cb_key.currentText()
    if len(additional_cb) == 0:
        errors.append("Поле 'additional_cb' должен не быть пустым")
    request_let = self.request_let_key.text()
    if len(request_let) == 0:
        errors.append("Поле 'request_let' должен не быть пустым")
    note_le = self.note_le_key.text()
    if len(note_le) == 0:
        errors.append("Поле 'note_le' должен не быть пустым")
    dateedit_str = dateedit1.toPyDate().strftime('%Y-%m-%d')
    dateedit2_str = dateedit2.toPyDate().strftime('%Y-%m-%d')

    if errors:
        error_message = "Обнаружены ошибки:\n\n" + "\n".join(f"• {error}" for error in errors)
        QMessageBox.critical(self, "Ошибка заполнения", error_message)
        return

    enter_keys(status_cb, nositel_type_cb, cert_serial_le, issuer_cb, scope_cb, owner_cb, vip_cb,
               dateedit_str, dateedit2_str, additional_cb, request_let, note_le)
    clear_fields(self)
    # Обновляем таблицу сразу после сохранения
    load_data8(self)


def clear_fields(self):
    self.status_cb.clearEditText()
    self.nositel_type_cb_key.clearEditText()
    self.serial_le_key.clear()
    self.issuer_cb_key.clearEditText()
    self.scope_cb_key.clearEditText()
    self.owner_cb_key.clearEditText()
    self.vip_cb.clearEditText()
    self.dateedit1_key.setDate(QDate.currentDate())
    self.dateedit2.setDate(QDate.currentDate())
    self.additional_cb_key.clearEditText()
    self.request_let_key.clear()
    self.note_le_key.clear()
