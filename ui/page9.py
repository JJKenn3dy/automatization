from datetime import datetime
from PyQt6 import QtWidgets
from PyQt6.QtGui import QShortcut, QKeySequence, QPalette, QColor
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout,
    QComboBox, QSizePolicy, QGroupBox, QFormLayout, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt, QDate, QTimer

from logic.db import enter_CBR
from ui.page8 import clear_fields  # Либо определить локальную функцию

def create_page9(self) -> QWidget:
    page = QWidget()
    # Устанавливаем общий тёмный фон и белый цвет текста для всей страницы
    page.setStyleSheet("background-color: #121212; color: white;")
    main_layout = QVBoxLayout(page)
    main_layout.setContentsMargins(20, 20, 20, 20)
    main_layout.setSpacing(15)

    # Кнопка "Назад"
    btn_back = QPushButton("Назад")
    btn_back.setStyleSheet(
        "background-color: #333333; color: white; font-size: 15px; border: 1px solid #555; border-radius: 4px;")
    btn_back.clicked.connect(self.go_to_second_page)
    main_layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignLeft)

    # Заголовок
    header_label = QLabel("КБР")
    header_label.setWordWrap(True)
    header_label.setStyleSheet("font-size: 20px; color: white;")
    header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    main_layout.addWidget(header_label)

    # Горизонтальный лэйаут для групп
    h_layout = QHBoxLayout()
    h_layout.setSpacing(30)
    main_layout.addLayout(h_layout)

    # ---------- ЛЕВЫЙ БЛОК (Основные данные) ----------
    left_group = QGroupBox("Основные данные")
    left_group.setStyleSheet("""
        QGroupBox {
            background-color: #1e1e1e;
            border: 1px solid #444;
            border-radius: 5px;
            padding: 10px;
            margin-top: 10px;
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

    # Заявка/номер обращения
    self.request_le = QLineEdit(self)
    self.request_le.setPlaceholderText("Заявка/номер обращения:")
    palette = self.request_le.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    self.request_le.setPalette(palette)
    self.request_le.setStyleSheet("background-color: #1e1e1e; border: 1px solid #444; border-radius: 4px; padding: 2px;")
    left_form.addRow(QLabel("Обращение:"), self.request_le)

    # Тип носителя (Да/Нет)
    self.nositel_cb = QComboBox(self)
    self.nositel_cb.setEditable(False)
    self.nositel_cb.setStyleSheet("""
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
    self.nositel_cb.addItem("Да")
    self.nositel_cb.addItem("Нет")
    left_form.addRow(QLabel("Тип носителя:"), self.nositel_cb)

    # Носитель (Серийный номер)
    self.nositel_serial_cb = QComboBox(self)
    self.nositel_serial_cb.setEditable(True)
    line_edit = self.nositel_serial_cb.lineEdit()
    line_edit.setPlaceholderText("Носитель (Серийный номер)")
    palette = line_edit.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    line_edit.setPalette(palette)
    self.nositel_serial_cb.setStyleSheet("""
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
    self.key_number_le.setStyleSheet("background-color: #1e1e1e; border: 1px solid #444; border-radius: 4px; padding: 2px;")
    left_form.addRow(QLabel("Номер ключа:"), self.key_number_le)

    # Выдавший УЦ
    self.issuer_cb_cbr = QComboBox(self)
    self.issuer_cb_cbr.setEditable(True)
    line_edit = self.issuer_cb_cbr.lineEdit()
    line_edit.setPlaceholderText("Выдавший УЦ")
    palette = line_edit.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    line_edit.setPalette(palette)
    self.issuer_cb_cbr.setStyleSheet("""
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
        self.issuer_cb_cbr.addItem(option)
    self.issuer_cb_cbr.clearEditText()
    left_form.addRow(QLabel("УЦ:"), self.issuer_cb_cbr)

    h_layout.addWidget(left_group, 1)

    # ---------- ПРАВЫЙ БЛОК (Дополнительно) ----------
    right_group = QGroupBox("Дополнительно")
    right_group.setStyleSheet("""
        QGroupBox {
            background-color: #1e1e1e;
            border: 1px solid #444;
            border-radius: 5px;
            padding: 10px;
            margin-top: 10px;
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
    right_form = QFormLayout()
    right_form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
    right_group.setLayout(right_form)

    # Область действия / наименование ЭДО
    self.scope_cb_cbr = QComboBox(self)
    self.scope_cb_cbr.setEditable(True)
    self.scope_cb_cbr.setCurrentText("Область действия / наименование ЭДО")
    line_edit = self.scope_cb_cbr.lineEdit()
    line_edit.setPlaceholderText("Область действия / наименование ЭДО")
    palette = line_edit.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    line_edit.setPalette(palette)
    self.scope_cb_cbr.setStyleSheet("""
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
        self.scope_cb_cbr.addItem(option)
    self.scope_cb_cbr.clearEditText()
    right_form.addRow(QLabel("Область/ЭДО:"), self.scope_cb_cbr)

    # ФИО владельца
    self.owner_cb_cbr = QComboBox(self)
    self.owner_cb_cbr.setEditable(True)
    line_edit = self.owner_cb_cbr.lineEdit()
    line_edit.setPlaceholderText("Владелец:")
    palette = line_edit.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    line_edit.setPalette(palette)
    self.owner_cb_cbr.setStyleSheet("""
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
        self.owner_cb_cbr.addItem(option)
    self.owner_cb_cbr.clearEditText()
    right_form.addRow(QLabel("Владелец:"), self.owner_cb_cbr)

    # Дата 1
    self.dateedit1 = QtWidgets.QDateEdit(calendarPopup=True)
    self.dateedit1.setDateTime(datetime.today())
    self.dateedit1.setStyleSheet("""
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
    right_form.addRow(QLabel("Дата 1:"), self.dateedit1)

    # Дата 2
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
    right_form.addRow(QLabel("Дата 2:"), self.dateedit2)

    # Дополнительно 1
    self.additional1_le = QLineEdit(self)
    self.additional1_le.setPlaceholderText("Дополнительно:")
    palette = self.additional1_le.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    self.additional1_le.setPalette(palette)
    self.additional1_le.setStyleSheet("background-color: #1e1e1e; border: 1px solid #444; border-radius: 4px; padding: 2px;")
    right_form.addRow(QLabel("Дополнительно:"), self.additional1_le)

    # Дополнительно 2
    self.additional2_le = QLineEdit(self)
    self.additional2_le.setPlaceholderText("Дополнительно:")
    palette = self.additional2_le.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    self.additional2_le.setPalette(palette)
    self.additional2_le.setStyleSheet("background-color: #1e1e1e; border: 1px solid #444; border-radius: 4px; padding: 2px;")
    right_form.addRow(QLabel("Дополнительно:"), self.additional2_le)

    h_layout.addWidget(right_group, 1)

    # Кнопка для сохранения данных
    self.save_button = QPushButton("Сохранить", self)
    self.save_button.setStyleSheet("background-color: #333333; color: white; font-size: 15px; border: 1px solid #555; border-radius: 4px;")
    right_form.addRow(self.save_button)
    self.save_button.clicked.connect(lambda: save_value9(self))

    # Шорткат для Enter
    enter_shortcut = QShortcut(QKeySequence("Return"), page)
    enter_shortcut.activated.connect(lambda: save_value9(self))
    escape_shortcut = QShortcut(QKeySequence("Escape"), page)
    escape_shortcut.activated.connect(self.go_to_second_page)



    # --- Добавляем виджет с таблицей и поиском для таблицы CBR ---
    data_table_widget = create_data_table9(self)
    main_layout.addWidget(data_table_widget)

    # --- Создаем таймер для периодического обновления таблицы ---
    self.refresh_timer = QTimer(self)
    self.refresh_timer.setInterval(5000)  # Обновление каждые 5 секунд
    self.refresh_timer.timeout.connect(lambda: load_data9(self))
    self.refresh_timer.start()

    return page

def create_data_table9(self) -> QWidget:
    """
    Создает виджет с поисковой строкой и таблицей для отображения последних записей из таблицы CBR.
    """
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setSpacing(5)

    # Поисковая строка
    search_layout = QHBoxLayout()
    search_label = QLabel("Поиск:")
    self.search_line9 = QLineEdit()
    self.search_line9.setPlaceholderText("Введите текст для поиска...")
    search_layout.addWidget(search_label)
    search_layout.addWidget(self.search_line9)
    layout.addLayout(search_layout)

    # Таблица для отображения данных из CBR
    self.table_widget9 = QTableWidget()
    headers = [
        "ID", "Заявка", "Статус", "Серийный номер", "Номер ключа",
        "УЦ", "Область/ЭДО", "Владелец", "Дата начала", "Дата окончания",
        "Дополнительно", "Примечание"
    ]
    self.table_widget9.setColumnCount(len(headers))
    self.table_widget9.setHorizontalHeaderLabels(headers)
    layout.addWidget(self.table_widget9)

    # Обновление таблицы при изменении текста поиска
    self.search_line9.textChanged.connect(lambda: load_data9(self))
    load_data9(self)

    return widget

def load_data9(self):
    """
    Загружает из базы данных последние 50 записей из таблицы CBR.
    Если введён поисковый запрос, выполняется фильтрация по нескольким полям.
    """
    search_text = self.search_line9.text().strip()
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
                SELECT * FROM CBR
                WHERE CAST(ID AS CHAR) LIKE %s 
                   OR number LIKE %s 
                   OR status LIKE %s 
                   OR number_serial LIKE %s 
                   OR number_key LIKE %s 
                   OR owner LIKE %s 
                   OR scope_using LIKE %s 
                   OR fullname_owner LIKE %s
                ORDER BY ID DESC
                LIMIT 50
            """
            like_pattern = f"%{search_text}%"
            cursor.execute(query, (like_pattern, like_pattern, like_pattern, like_pattern,
                                     like_pattern, like_pattern, like_pattern, like_pattern))
        else:
            query = "SELECT * FROM CBR ORDER BY ID DESC LIMIT 50"
            cursor.execute(query)
        results = cursor.fetchall()
        connection.close()

        self.table_widget9.horizontalHeader().setStretchLastSection(True)
        self.table_widget9.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.table_widget9.setRowCount(len(results))
        for row_idx, row_data in enumerate(results):
            # Структура CBR: ID, number, status, number_serial, number_key, owner,
            # scope_using, fullname_owner, date_start, date_end, additional, note
            columns = [
                row_data.get("ID"),
                row_data.get("number"),
                row_data.get("status"),
                row_data.get("number_serial"),
                row_data.get("number_key"),
                row_data.get("owner"),
                row_data.get("scope_using"),
                row_data.get("fullname_owner"),
                row_data.get("date_start"),
                row_data.get("date_end"),
                row_data.get("additional"),
                row_data.get("note")
            ]
            for col_idx, value in enumerate(columns):
                item = QTableWidgetItem(str(value) if value is not None else "")
                self.table_widget9.setItem(row_idx, col_idx, item)
    except Exception as e:
        print("Ошибка загрузки данных для CBR:", e)

def save_value9(self):
    request_le = self.request_le.text()
    nositel_cb = self.nositel_cb.currentText()
    nositel_serial_cb = self.nositel_serial_cb.currentText()
    key_number_le = self.key_number_le.text()
    issuer_cb = self.issuer_cb_cbr.currentText()
    scope_cb = self.scope_cb_cbr.currentText()
    owner_cb = self.owner_cb_cbr.currentText()
    dateedit1 = self.dateedit1.date()
    dateedit2 = self.dateedit2.date()
    additional1_le = self.additional1_le.text()
    additional2_le = self.additional2_le.text()

    dateedit_str = dateedit1.toPyDate().strftime('%Y-%m-%d')
    dateedit2_str = dateedit2.toPyDate().strftime('%Y-%m-%d')

    enter_CBR(request_le, nositel_cb, nositel_serial_cb, key_number_le,
              issuer_cb, scope_cb, owner_cb, dateedit_str, dateedit2_str,
              additional1_le, additional2_le)
    clear_fields(self)
    # Обновляем таблицу сразу после сохранения
    load_data9(self)

def clear_fields(self):
    self.request_le.clear()
    self.nositel_cb.clearEditText()
    self.nositel_serial_cb.clearEditText()
    self.key_number_le.clear()
    self.issuer_cb_cbr.clearEditText()
    self.scope_cb_cbr.clearEditText()
    self.owner_cb_cbr.clearEditText()
    self.dateedit1.setDate(QDate.currentDate())
    self.dateedit2.setDate(QDate.currentDate())
    self.additional1_le.clear()
    self.additional2_le.clear()
