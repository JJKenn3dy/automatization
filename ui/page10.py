from datetime import datetime
from PyQt6 import QtWidgets
from PyQt6.QtGui import QShortcut, QKeySequence, QPalette, QColor
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout,
    QComboBox, QGroupBox, QFormLayout, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt, QDate, QTimer

from logic.db import enter_TLS
import pymysql  # Если ещё не импортирован

def create_page10(self) -> QWidget:
    page = QWidget()
    # Общий стиль страницы: тёмный фон и белый текст
    page.setStyleSheet("background-color: #121212; color: white;")
    main_layout = QVBoxLayout(page)
    main_layout.setContentsMargins(20, 20, 20, 20)
    main_layout.setSpacing(15)

    # Кнопка "Назад"
    btn_back = QPushButton("Назад")
    btn_back.setStyleSheet(
        "background-color: #333333; color: white; font-size: 15px; border: 1px solid #555; border-radius: 4px;")
    btn_back.clicked.connect(self.go_to_second_page)
    btn_back.setMinimumSize(150, 30)
    main_layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignLeft)

    # Заголовок
    header_label = QLabel("TLS")
    header_label.setWordWrap(True)
    header_label.setStyleSheet("font-size: 20px; color: white;")
    header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    main_layout.addWidget(header_label)

    # Горизонтальный лэйаут для левого и правого блоков
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

    # Номер заявки
    self.request_number_le = QLineEdit(self)
    self.request_number_le.setPlaceholderText("Номер заявки:")
    style_line = "background-color: #1e1e1e; border: 1px solid #444; border-radius: 4px; padding: 2px;"
    self.request_number_le.setStyleSheet(style_line)
    palette = self.request_number_le.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    self.request_number_le.setPalette(palette)
    left_form.addRow(QLabel("Заявка:"), self.request_number_le)

    # Дата
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
    left_form.addRow(QLabel("Дата:"), self.dateedit1)

    # Среда (тест/продуктив)
    self.env_cb = QComboBox(self)
    self.env_cb.setEditable(True)
    self.env_cb.setCurrentText("Среда (тест/продуктив)")
    line_edit = self.env_cb.lineEdit()
    line_edit.setPlaceholderText("Среда (тест/продуктив)")
    line_edit.setStyleSheet(style_line)
    palette = line_edit.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    line_edit.setPalette(palette)
    self.env_cb.addItems(["тест", "продуктив"])
    self.env_cb.clearEditText()
    left_form.addRow(QLabel("Среда:"), self.env_cb)

    # Доступ (внешний/внутренний)
    self.access_cb = QComboBox(self)
    self.access_cb.setEditable(True)
    self.access_cb.setCurrentText("Доступ (внешний/внутренний)")
    line_edit = self.access_cb.lineEdit()
    line_edit.setPlaceholderText("Доступ (внешний/внутренний)")
    line_edit.setStyleSheet(style_line)
    palette = line_edit.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    line_edit.setPalette(palette)
    self.access_cb.addItems(["внешний", "внутренний"])
    self.access_cb.clearEditText()
    left_form.addRow(QLabel("Доступ:"), self.access_cb)

    # Выдавший УЦ
    self.issuer_cb = QComboBox(self)
    self.issuer_cb.setEditable(True)
    self.issuer_cb.setCurrentText("Выдавший УЦ")
    line_edit = self.issuer_cb.lineEdit()
    line_edit.setPlaceholderText("Выдавший УЦ")
    line_edit.setStyleSheet(style_line)
    palette = line_edit.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    line_edit.setPalette(palette)
    self.issuer_cb.addItems(["Option 1", "Option 2", "Option 3"])
    self.issuer_cb.clearEditText()
    left_form.addRow(QLabel("УЦ:"), self.issuer_cb)

    # Инициатор
    self.initiator_cb = QComboBox(self)
    self.initiator_cb.setEditable(True)
    self.initiator_cb.setCurrentText("Инициатор")
    line_edit = self.initiator_cb.lineEdit()
    line_edit.setPlaceholderText("Инициатор")
    line_edit.setStyleSheet(style_line)
    palette = line_edit.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    line_edit.setPalette(palette)
    self.initiator_cb.addItems(["Option 1", "Option 2", "Option 3"])
    self.initiator_cb.clearEditText()
    left_form.addRow(QLabel("Инициатор:"), self.initiator_cb)

    h_layout.addWidget(left_group, 1)

    # ---------- ПРАВЫЙ БЛОК (Дополнительные сведения) ----------
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

    # Владелец АС
    self.owner_cb = QComboBox(self)
    self.owner_cb.setEditable(True)
    self.owner_cb.setCurrentText("Владелец АС")
    line_edit = self.owner_cb.lineEdit()
    line_edit.setPlaceholderText("Владелец АС")
    line_edit.setStyleSheet(style_line)
    palette = line_edit.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    line_edit.setPalette(palette)
    self.owner_cb.addItems(["Option 1", "Option 2", "Option 3"])
    self.owner_cb.clearEditText()
    right_form.addRow(QLabel("Владелец АС:"), self.owner_cb)

    # Алгоритм (RSA/ГОСТ)
    self.algo_cb = QComboBox(self)
    self.algo_cb.setEditable(True)
    self.algo_cb.setCurrentText("Алгоритм (RSA/ГОСТ)")
    line_edit = self.algo_cb.lineEdit()
    line_edit.setPlaceholderText("Алгоритм (RSA/ГОСТ)")
    line_edit.setStyleSheet(style_line)
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
    line_edit.setStyleSheet(style_line)
    palette = line_edit.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    line_edit.setPalette(palette)
    self.scope_cb.addItems(["Option 1", "Option 2", "Option 3"])
    self.scope_cb.clearEditText()
    right_form.addRow(QLabel("Область/ЭДО:"), self.scope_cb)

    # DNS
    self.dns_le = QLineEdit(self)
    self.dns_le.setPlaceholderText("DNS:")
    self.dns_le.setStyleSheet(style_line)
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
    line_edit.setStyleSheet(style_line)
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
    self.note_le.setStyleSheet(style_line)
    palette = self.note_le.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    self.note_le.setPalette(palette)
    right_form.addRow(QLabel("Примечание:"), self.note_le)

    h_layout.addWidget(right_group, 1)

    # Кнопка для сохранения данных
    self.save_button = QPushButton("Сохранить", self)
    self.save_button.setStyleSheet("background-color: #333333; color: white; font-size: 15px; border: 1px solid #555; border-radius: 4px;")
    right_form.addRow(self.save_button)
    self.save_button.clicked.connect(lambda: save_value10(self))

    # Шорткат для Enter
    enter_shortcut = QShortcut(QKeySequence("Return"), page)
    enter_shortcut.activated.connect(lambda: save_value10(self))
    escape_shortcut = QShortcut(QKeySequence("Escape"), page)
    escape_shortcut.activated.connect(self.go_to_second_page)



    # --- Добавляем виджет с таблицей и поиском для TLS ---
    data_table_widget = create_data_table10(self)
    main_layout.addWidget(data_table_widget)

    # --- Создаем таймер для периодического обновления таблицы ---
    self.refresh_timer = QTimer(self)
    self.refresh_timer.setInterval(60000)  # Обновление каждые 60 секунд
    self.refresh_timer.timeout.connect(lambda: load_data10(self))
    self.refresh_timer.start()

    return page

def create_data_table10(self) -> QWidget:
    """
    Создает виджет с поисковой строкой и таблицей для отображения последних записей из таблицы TLS.
    """
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setSpacing(5)

    # Поисковая строка
    search_layout = QHBoxLayout()
    search_label = QLabel("Поиск:")
    self.search_line10 = QLineEdit()
    self.search_line10.setPlaceholderText("Введите текст для поиска...")
    search_layout.addWidget(search_label)
    search_layout.addWidget(self.search_line10)
    layout.addLayout(search_layout)

    # Таблица для отображения данных TLS
    self.table_widget10 = QTableWidget()
    headers = [
        "ID", "Заявка", "Дата", "Среда", "Доступ",
        "УЦ", "Инициатор", "Владелец АС", "Алгоритм", "Область/ЭДО",
        "DNS", "Резолюция", "Примечание"
    ]
    self.table_widget10.setColumnCount(len(headers))
    self.table_widget10.setHorizontalHeaderLabels(headers)
    layout.addWidget(self.table_widget10)

    # Обновление таблицы при изменении текста поиска
    self.search_line10.textChanged.connect(lambda: load_data10(self))
    load_data10(self)

    return widget

def load_data10(self):
    """
    Загружает из базы данных последние 50 записей из таблицы TLS.
    При наличии поискового запроса выполняется фильтрация по нескольким полям.
    """
    search_text = self.search_line10.text().strip()
    try:
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
                SELECT * FROM TLS
                WHERE CAST(ID AS CHAR) LIKE %s 
                   OR number LIKE %s 
                   OR date LIKE %s 
                   OR environment LIKE %s 
                   OR access LIKE %s 
                   OR issuer LIKE %s 
                   OR initiator LIKE %s 
                   OR owner LIKE %s 
                   OR algorithm LIKE %s 
                   OR scope LIKE %s 
                   OR DNS LIKE %s 
                   OR resolution LIKE %s 
                   OR note LIKE %s
                ORDER BY ID DESC
                LIMIT 50
            """
            like_pattern = f"%{search_text}%"
            cursor.execute(query, (like_pattern, like_pattern, like_pattern, like_pattern,
                                     like_pattern, like_pattern, like_pattern, like_pattern,
                                     like_pattern, like_pattern, like_pattern, like_pattern, like_pattern))
        else:
            query = "SELECT * FROM TLS ORDER BY ID DESC LIMIT 500"
            cursor.execute(query)
        results = cursor.fetchall()
        connection.close()

        self.table_widget10.horizontalHeader().setStretchLastSection(True)
        self.table_widget10.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.table_widget10.setRowCount(len(results))
        for row_idx, row_data in enumerate(results):
            # Порядок колонок согласно структуре таблицы TLS:
            # ID, number, date, environment, access, issuer, initiator, owner,
            # algorithm, scope, DNS, resolution, note
            columns = [
                row_data.get("ID"),
                row_data.get("number"),
                row_data.get("date"),
                row_data.get("environment"),
                row_data.get("access"),
                row_data.get("issuer"),
                row_data.get("initiator"),
                row_data.get("owner"),
                row_data.get("algorithm"),
                row_data.get("scope"),
                row_data.get("DNS"),
                row_data.get("resolution"),
                row_data.get("note")
            ]
            for col_idx, value in enumerate(columns):
                item = QTableWidgetItem(str(value) if value is not None else "")
                self.table_widget10.setItem(row_idx, col_idx, item)
    except Exception as e:
        print("Ошибка загрузки данных для TLS:", e)

def save_value10(self):
    request_number_le = self.request_number_le.text()
    dateedit1 = self.dateedit1.date().toPyDate().strftime('%Y-%m-%d')
    env_cb = self.env_cb.currentText()
    access_cb = self.access_cb.currentText()
    issuer_cb = self.issuer_cb.currentText()
    initiator_cb = self.initiator_cb.currentText()
    owner_cb = self.owner_cb.currentText()
    algo_cb = self.algo_cb.currentText()
    scope_cb = self.scope_cb.currentText()
    dns_le = self.dns_le.text()
    resolution_cb = self.resolution_cb.currentText()
    note_le = self.note_le.text()

    enter_TLS(
        request_number_le,
        dateedit1,
        env_cb,
        access_cb,
        issuer_cb,
        initiator_cb,
        owner_cb,
        algo_cb,
        scope_cb,
        dns_le,
        resolution_cb,
        note_le
    )
    clear_fields(self)
    # Обновляем таблицу сразу после сохранения
    load_data10(self)

def clear_fields(self):
    self.request_number_le.clear()
    self.dateedit1.setDate(QDate.currentDate())
    self.env_cb.clearEditText()
    self.access_cb.clearEditText()
    self.issuer_cb.clearEditText()
    self.initiator_cb.clearEditText()
    self.owner_cb.clearEditText()
    self.algo_cb.clearEditText()
    self.scope_cb.clearEditText()
    self.dns_le.clear()
    self.resolution_cb.clearEditText()
    self.note_le.clear()
