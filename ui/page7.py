from datetime import datetime
from PyQt6 import QtWidgets
from PyQt6.QtGui import QShortcut, QKeySequence, QPalette, QColor
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout,
    QComboBox, QSizePolicy, QGroupBox, QFormLayout, QTableWidget, QHeaderView, QCompleter, QMessageBox
)
from PyQt6.QtCore import Qt
from logic.db import enter_sczy
import pymysql  # Добавляем импорт, если ещё не импортирован
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtCore import QTimer

def update_line_edit_style(line_edit, condition_error: bool):
    if line_edit.hasFocus():
        # Применяем валидацию, если поле в фокусе
        if condition_error:
            style = (
                "background-color: #1e1e1e; border: 1px solid red; border-radius: 4px; padding: 2px; color: white;"
            )
        else:
            style = (
                "background-color: #1e1e1e; border: 1px solid #444; border-radius: 4px; padding: 2px; color: white;"
            )
    else:
        # Если поле не в фокусе, возвращаем стандартное оформление
        style = (
            "background-color: #1e1e1e; border: 1px solid #444; border-radius: 4px; padding: 2px; color: white;"
        )
    line_edit.setStyleSheet(style)


def update_combobox_style(combo_box, condition_error: bool):
    """
    Устанавливает стиль для QComboBox:
      - если поле в фокусе и condition_error == True, рамка красная
      - иначе (либо поле не в фокусе, либо condition_error == False), стандартная рамка.
    """
    # Стандартный стиль комбобокса (без ошибки)
    default_style = """
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
    """
    # Стиль при ошибке
    error_style = """
        QComboBox {
            background-color: #1e1e1e;
            color: white;
            border: 1px solid red;
            border-radius: 4px;
            padding: 2px;
        }
        QComboBox QAbstractItemView {
            background-color: #121212;
            color: white;
            selection-background-color: #444;
            selection-color: white;
        }
    """
    # Если комбобокс находится в фокусе, используем проверку состояния,
    # иначе всегда отображаем стандартный стиль.
    if combo_box.hasFocus():
        if condition_error:
            style = error_style
        else:
            style = default_style
    else:
        style = default_style

    combo_box.setStyleSheet(style)


def create_page7(self) -> QWidget:
    page = QWidget()
    # Устанавливаем общий тёмный фон и белый текст для страницы
    page.setStyleSheet("background-color: #121212; color: white;")
    main_layout = QVBoxLayout(page)
    main_layout.setContentsMargins(20, 20, 20, 20)
    main_layout.setSpacing(15)

    btn_back = QPushButton("Назад")
    btn_back.setStyleSheet(
        "background-color: #333333; color: white; font-size: 15px; border: 1px solid #555; border-radius: 4px;")
    btn_back.clicked.connect(self.go_to_second_page)
    btn_back.setMinimumSize(150, 30)

    main_layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignLeft)

    # Заголовок
    header_label = QLabel("СКЗИ")
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
    left_form = QFormLayout()
    left_form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
    left_group.setLayout(left_form)

    # Для поля "Наименование СКЗИ" (используем столбец "name_of_SCZY")
    self.skzi_name_cb = QComboBox(self)
    self.skzi_name_cb.setEditable(True)
    line_edit = self.skzi_name_cb.lineEdit()
    line_edit.setPlaceholderText("Наименование СКЗИ")
    # Настройка палитры (оставляем как есть)
    palette = line_edit.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(70, 130, 20))
    line_edit.setPalette(palette)
    # Загрузка данных из БД:
    populate_combobox_with_db(self.skzi_name_cb, "name_of_SCZY")
    self.skzi_name_cb.clearEditText()
    left_form.addRow(QLabel("Наименование СКЗИ:"), self.skzi_name_cb)
    self.skzi_name_cb.lineEdit().textChanged.connect(
        lambda: update_combobox_style(
            self.skzi_name_cb,
            len(self.skzi_name_cb.currentText().strip()) == 0
        )
    )

    # Тип СКЗИ (не редактируемый)
    self.skzi_type = QComboBox(self)
    self.skzi_type.setEditable(False)
    # Переиспользуем палитру из предыдущего line_edit
    palette = line_edit.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    line_edit.setPalette(palette)
    for option in ["ПО", "ПАК"]:
        self.skzi_type.addItem(option)
    self.skzi_type.clearEditText()
    left_form.addRow(QLabel("Тип СКЗИ:"), self.skzi_type)
    # Подключаем проверку комбобокса
    self.skzi_type.currentTextChanged.connect(
        lambda text: update_combobox_style(
            self.skzi_type,
            len(text.strip()) == 0
        )
    )

    # Аналогично для "Версия СКЗИ" (например, используя столбец "number_SCZY")
    self.skzi_version_cb = QComboBox(self)
    self.skzi_version_cb.setEditable(True)
    self.skzi_version_cb.setCurrentText("Версия СКЗИ")
    line_edit = self.skzi_version_cb.lineEdit()
    line_edit.setPlaceholderText("Версия СКЗИ")
    palette = line_edit.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    line_edit.setPalette(palette)
    populate_combobox_with_db(self.skzi_version_cb, "number_SCZY")
    self.skzi_version_cb.clearEditText()
    left_form.addRow(QLabel("Версия СКЗИ:"), self.skzi_version_cb)
    self.skzi_version_cb.lineEdit().textChanged.connect(
        lambda: update_combobox_style(
            self.skzi_version_cb,
            len(self.skzi_version_cb.currentText().strip()) == 0
        )
    )

    # Календарь (Дата)
    self.dateedit7 = QtWidgets.QDateEdit(calendarPopup=True)
    self.dateedit7.setDateTime(datetime.today())
    self.dateedit7.setStyleSheet("""
    QDateEdit {
        background-color: #1e1e1e;
        color: white;
        border: 1px solid #444;
        border-radius: 4px;
        padding: 2px;
    }
    QDateEdit::drop-down {
        background-color: #1e1e1e;
    }
    QDateEdit::down-arrow {
        width: 8px;
        height: 8px;
    }
    QCalendarWidget {
        background-color: #1e1e1e;
        color: white;
        border: 1px solid #444;
    }
    QCalendarWidget QToolButton {
        background-color: #333;
        color: white;
        margin: 5px;
        border-radius: 3px;
    }
    QCalendarWidget QToolButton:hover {
        background-color: #444;
    }
    QCalendarWidget QToolButton:disabled {
        background-color: #777;
    }
    QCalendarWidget QSpinBox {
        background-color: #333;
        color: white;
        selection-background-color: #444;
        selection-color: white;
    }
    QCalendarWidget QSpinBox:hover {
        background-color: #444;
    }
    QCalendarWidget QAbstractItemView:enabled {
        background-color: #121212;
        color: #e0e0e0;
        selection-background-color: #444;
        selection-color: white;
    }
    QCalendarWidget QAbstractItemView:disabled {
        color: #666;
    }
    """)
    left_form.addRow(QLabel("Дата:"), self.dateedit7)

    # Подключаем проверку изменения даты
    self.dateedit7.dateChanged.connect(
        lambda date: self.dateedit7.setStyleSheet(
            "background-color: #1e1e1e; border: 1px solid red; border-radius: 4px; padding: 2px; color: white;"
            if not date.isValid()
            else "background-color: #1e1e1e; border: 1px solid #444; border-radius: 4px; padding: 2px; color: white;"
        )
    )

    # Местонахождение ПО
    self.location = QLineEdit(self)
    self.location.setPlaceholderText("Местонахождение СКЗИ")
    palette = self.location.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    self.location.setPalette(palette)
    left_form.addRow(QLabel("Местонахождение:"), self.location)
    self.location.textChanged.connect(
        lambda: update_line_edit_style(self.location, len(self.location.text().strip()) <= 3)
    )

    # ТОМ
    self.location_TOM = QLineEdit(self)
    self.location_TOM.setPlaceholderText("ТОМ")
    palette = self.location_TOM.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    self.location_TOM.setPalette(palette)
    left_form.addRow(QLabel("ТОМ:"), self.location_TOM)
    self.location_TOM.textChanged.connect(
        lambda: update_line_edit_style(self.location_TOM, len(self.location_TOM.text().strip()) <= 3)
    )

    # Документ (дата и номер)
    self.doc_info_skzi = QLineEdit(self)
    self.doc_info_skzi.setPlaceholderText("Дата и номер документа")
    palette = self.doc_info_skzi.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    self.doc_info_skzi.setPalette(palette)
    left_form.addRow(QLabel("Документ:"), self.doc_info_skzi)
    self.doc_info_skzi.textChanged.connect(
        lambda: update_line_edit_style(self.doc_info_skzi, len(self.doc_info_skzi.text().strip()) <= 3)
    )

    # Договор
    self.contract_skzi = QLineEdit(self)
    self.contract_skzi.setPlaceholderText("Договор")
    palette = self.contract_skzi.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    self.contract_skzi.setPalette(palette)
    left_form.addRow(QLabel("Договор:"), self.contract_skzi)
    self.contract_skzi.textChanged.connect(
        lambda: update_line_edit_style(self.contract_skzi, len(self.contract_skzi.text().strip()) <= 3)
    )

    # Владелец (fullname_owner)
    self.fullname_owner = QLineEdit(self)
    self.fullname_owner.setPlaceholderText("Владелец")
    palette = self.fullname_owner.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    self.fullname_owner.setPalette(palette)
    left_form.addRow(QLabel("Владелец:"), self.fullname_owner)
    self.fullname_owner.textChanged.connect(
        lambda: update_line_edit_style(self.fullname_owner, len(self.fullname_owner.text().strip()) <= 3)
    )

    left_form.setSpacing(10)
    h_layout.addWidget(left_group, 1)

    # ---------- ПРАВЫЙ БЛОК (Дополнительные сведения) ----------
    right_group = QGroupBox("Дополнительные сведения")
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

    # Регистрационный номер
    self.reg_number_le = QLineEdit(self)
    self.reg_number_le.setPlaceholderText("Регистрационный номер")
    palette = self.reg_number_le.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    self.reg_number_le.setPalette(palette)
    right_form.addRow(QLabel("Рег. номер:"), self.reg_number_le)
    self.reg_number_le.textChanged.connect(
        lambda: update_line_edit_style(self.reg_number_le, len(self.reg_number_le.text().strip()) <= 3)
    )

    # От кого получены
    self.from_whom_cb = QComboBox(self)
    self.from_whom_cb.setEditable(True)
    line_edit = self.from_whom_cb.lineEdit()
    line_edit.setPlaceholderText("От кого получены")
    palette = line_edit.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(70, 130, 20))
    line_edit.setPalette(palette)
    populate_combobox_with_db(self.from_whom_cb, "owner")
    self.from_whom_cb.clearEditText()
    right_form.addRow(QLabel("От кого получены:"), self.from_whom_cb)
    self.from_whom_cb.lineEdit().textChanged.connect(
        lambda: update_combobox_style(
            self.from_whom_cb,
            len(self.from_whom_cb.currentText().strip()) == 0
        )
    )

    # Владельцы
    self.owners = QComboBox(self)
    self.owners.setEditable(True)
    line_edit = self.owners.lineEdit()
    line_edit.setPlaceholderText("Владельцы")
    palette = line_edit.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(70, 130, 20))
    line_edit.setPalette(palette)
    populate_combobox_with_db(self.owners, "owners")
    self.owners.clearEditText()
    right_form.addRow(QLabel("Владельцы:"), self.owners)
    self.owners.lineEdit().textChanged.connect(
        lambda: update_combobox_style(
            self.owners,
            len(self.owners.currentText().strip()) == 0
        )
    )

    # Бизнес процессы
    self.buss_proc = QComboBox(self)
    self.buss_proc.setEditable(True)
    line_edit = self.buss_proc.lineEdit()
    line_edit.setPlaceholderText("Бизнес процессы")
    palette = line_edit.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(70, 130, 20))
    line_edit.setPalette(palette)
    populate_combobox_with_db(self.buss_proc, "buss_proc")
    self.buss_proc.clearEditText()
    right_form.addRow(QLabel("Бизнес процессы:"), self.buss_proc)
    self.buss_proc.lineEdit().textChanged.connect(
        lambda: update_combobox_style(
            self.buss_proc,
            len(self.buss_proc.currentText().strip()) == 0
        )
    )

    # Дополнительно
    self.additional_le = QLineEdit(self)
    self.additional_le.setPlaceholderText("Дополнительно")
    palette = self.additional_le.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    self.additional_le.setPalette(palette)
    right_form.addRow(QLabel("Дополнительно:"), self.additional_le)
    self.additional_le.textChanged.connect(
        lambda: update_line_edit_style(self.additional_le, len(self.additional_le.text().strip()) <= 3)
    )

    # Примечание
    self.note_cb = QComboBox(self)
    self.note_cb.setEditable(True)
    line_edit = self.note_cb.lineEdit()
    line_edit.setPlaceholderText("Примечание")
    palette = line_edit.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(70, 130, 20))
    line_edit.setPalette(palette)
    populate_combobox_with_db(self.note_cb, "note")
    self.note_cb.clearEditText()
    right_form.addRow(QLabel("Примечание:"), self.note_cb)
    self.note_cb.lineEdit().textChanged.connect(
        lambda: update_combobox_style(
            self.note_cb,
            len(self.note_cb.currentText().strip()) == 0
        )
    )

    # Сертификат
    self.certnum_le = QLineEdit(self)
    self.certnum_le.setPlaceholderText("Номер сертификата соответствия")
    palette = self.certnum_le.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    self.certnum_le.setPalette(palette)
    right_form.addRow(QLabel("Сертификат:"), self.certnum_le)
    self.certnum_le.textChanged.connect(
        lambda: update_line_edit_style(self.certnum_le, len(self.certnum_le.text().strip()) <= 3)
    )

    # Дополнительная дата
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
        QDateEdit::drop-down {
            background-color: #1e1e1e;
        }
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
    right_form.addRow(QLabel("Доп. дата:"), self.dateedit2)
    # Подключаем проверку изменения даты
    self.dateedit2.dateChanged.connect(
        lambda date: self.dateedit2.setStyleSheet(
            "background-color: #1e1e1e; border: 1px solid red; border-radius: 4px; padding: 2px; color: white;"
            if not date.isValid()
            else "background-color: #1e1e1e; border: 1px solid #444; border-radius: 4px; padding: 2px; color: white;"
        )
    )

    right_form.setSpacing(10)
    h_layout.addWidget(right_group, 1)

    # --- Добавляем виджет с таблицей (SCZY) ---
    data_table_widget = create_data_table7(self)
    main_layout.addWidget(data_table_widget)

    # --- Создаем таймер для периодического обновления таблицы ---
    self.refresh_timer = QTimer(self)
    self.refresh_timer.setInterval(5000)  # Интервал в мс, например, 60000 = 60 секунд
    self.refresh_timer.timeout.connect(lambda: load_data7(self))
    self.refresh_timer.start()

    # --- Кнопки ---
    enter_shortcut = QShortcut(QKeySequence("Return"), page)
    enter_shortcut.activated.connect(lambda: save_value7(self))
    self.save_button = QPushButton("Сохранить", self)
    self.save_button.setStyleSheet("background-color: #333333; color: white; font-size: 15px; border: 1px solid #555; border-radius: 4px;")
    right_form.addRow(self.save_button)
    self.save_button.clicked.connect(lambda: save_value7(self))

    escape_shortcut = QShortcut(QKeySequence("Escape"), page)
    escape_shortcut.activated.connect(self.go_to_second_page)


    return page


def create_data_table7(self) -> QWidget:
    """
    Создает виджет с поисковой строкой и таблицей для отображения последних записей из таблицы SCZY.
    """
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setSpacing(5)


    # Поисковая строка
    search_layout = QHBoxLayout()
    search_label = QLabel("Поиск:")
    self.search_line7 = QLineEdit()
    self.search_line7.setPlaceholderText("Введите текст для поиска...")
    search_layout.addWidget(search_label)
    search_layout.addWidget(self.search_line7)
    layout.addLayout(search_layout)

    # Таблица для отображения данных SCZY
    self.table_widget7 = QTableWidget()
    headers = [
        "ID", "Наименование СКЗИ", "Тип СКЗИ", "Версия", "Дата", "Рег. номер",
        "Местонахождение", "ТОМ", "От кого получены", "Документ", "Договор",
        "Владелец", "Владельцы", "Бизнес процессы", "Дополнительно",
        "Примечание", "Сертификат", "Доп. дата"
    ]

    self.table_widget7.setColumnCount(len(headers))
    self.table_widget7.setHorizontalHeaderLabels(headers)
    layout.addWidget(self.table_widget7)

    self.table_widget7.horizontalHeader().setStretchLastSection(True)
    self.table_widget7.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    # При изменении текста в поисковой строке перезагружаем данные
    self.search_line7.textChanged.connect(lambda: load_data7(self))
    load_data7(self)

    return widget


def load_data7(self):
    """
    Загружает из базы данных последние 50 записей из таблицы SCZY.
    При наличии текста в поиске выполняется фильтрация по нескольким полям.
    """
    search_text = self.search_line7.text().strip()
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
                SELECT * FROM SCZY
                WHERE CAST(ID AS CHAR) LIKE %s 
                   OR name_of_SCZY LIKE %s 
                   OR sczy_type LIKE %s 
                   OR number_SCZY LIKE %s 
                   OR owner LIKE %s 
                   OR fullname_owner LIKE %s
                ORDER BY ID DESC
                LIMIT 50
            """
            like_pattern = f"%{search_text}%"
            cursor.execute(query, (like_pattern, like_pattern, like_pattern, like_pattern, like_pattern, like_pattern))
        else:
            query = "SELECT * FROM SCZY ORDER BY ID DESC LIMIT 500"
            cursor.execute(query)
        results = cursor.fetchall()
        connection.close()

        self.table_widget7.setRowCount(len(results))
        for row_idx, row_data in enumerate(results):
            # Порядок колонок согласно структуре таблицы SCZY:
            # ID, name_of_SCZY, sczy_type, number_SCZY, date, number_license, location,
            # location_TOM_text, owner, date_and_number, contract, fullname_owner, owners,
            # buss_proc, additional, note, number_certificate, date_expired
            columns = [
                row_data.get("ID"),
                row_data.get("name_of_SCZY"),
                row_data.get("sczy_type"),
                row_data.get("number_SCZY"),
                row_data.get("date"),
                row_data.get("number_license"),
                row_data.get("location"),
                row_data.get("location_TOM_text"),
                row_data.get("owner"),
                row_data.get("date_and_number"),
                row_data.get("contract"),
                row_data.get("fullname_owner"),
                row_data.get("owners"),
                row_data.get("buss_proc"),
                row_data.get("additional"),
                row_data.get("note"),
                row_data.get("number_certificate"),
                row_data.get("date_expired")
            ]
            for col_idx, value in enumerate(columns):
                item = QTableWidgetItem(str(value) if value is not None else "")
                self.table_widget7.setItem(row_idx, col_idx, item)
    except Exception as e:
        print("Ошибка загрузки данных для SCZY:", e)


def save_value7(self):
    errors = []


    # Сбор данных из виджетов
    skzi_name = self.skzi_name_cb.currentText()               # Наименование ПО
    if len(skzi_name) == 0:
        errors.append("Поле 'Номер' должен не быть пустым")

    skzi_type = self.skzi_type.currentText()                    # Тип СКЗИ
    if len(skzi_type) == 0:
        errors.append("Поле 'ТИП СКЗИ' должен не быть пустым")

    skzi_version = self.skzi_version_cb.currentText()           # Версия СКЗИ
    if len(skzi_version) == 0:
        errors.append("Поле 'skzi_version' должен не быть пустым")

    date_str = self.dateedit7.date().toPyDate().strftime('%Y-%m-%d')  # Дата

    reg_number = self.reg_number_le.text()                      # Рег. номер
    if len(reg_number) < 3:
        errors.append("Рег. номер должен содержать более 2 символов")
    location_text = self.location.text()                        # Местонахождение (ТОМ)
    if len(location_text) < 2:
        errors.append("Местонахождение должно содержать более 2 символов")
    location_TOM_text = self.location_TOM.text()
    if len(location_TOM_text) < 1:
        errors.append("Местонахождение ТОМа должно содержать более 1 символа")
    from_whom_cb = self.from_whom_cb.currentText()                 # От кого получены
    if len(from_whom_cb) < 4:
        errors.append("'От кого получены' должен содержать более 4 символов")
    doc_info = self.doc_info_skzi.text()                          # Документ
    if len(doc_info) < 4:
        errors.append("'Документ' должно содержать более 4 символа")
    contract = self.contract_skzi.text()                             # Договор
    if len(contract) < 4:
        errors.append("'Договор' должно содержать более 4 символа")
    owners = self.owners.currentText()                          # Владельцы
    if len(owners) < 4:
        errors.append("'Владельцы' должно содержать более 4 символа")
    buss_proc = self.buss_proc.currentText()                    # Бизнес процессы
    if len(buss_proc) < 4:
        errors.append("'Бизнес процессы' должно содержать более 4 символа")
    fullname_owner = self.fullname_owner.text()
    if len(fullname_owner) < 4:
        errors.append("'fullname_owner' должно содержать более 4 символа")
    additional = self.additional_le.text()                      # Дополнительно
    note = self.note_cb.currentText()                           # Примечание
    certnum = self.certnum_le.text()                            # Сертификат
    if len(certnum) < 4:
        errors.append("'Сертификат' должно содержать более 4 символа")
    dateedit2_str = self.dateedit2.date().toPyDate().strftime('%Y-%m-%d')  # Доп. дата

    if errors:
        error_message = "Обнаружены ошибки:\n\n" + "\n".join(f"• {error}" for error in errors)
        QMessageBox.critical(self, "Ошибка заполнения", error_message)
        return

    enter_sczy(
        skzi_name,
        skzi_type,
        skzi_version,
        date_str,
        reg_number,
        location_text,
        location_TOM_text,
        from_whom_cb,
        doc_info,
        contract,
        fullname_owner,
        owners,
        buss_proc,
        additional,
        note,
        certnum,
        dateedit2_str
    )


    # Обновление таблицы сразу после сохранения
    load_data7(self)

    # Обновление выпадающих списков с данными из БД
    refresh_comboboxes(self)

    clear_fields(self)

    QMessageBox.information(self, "Успех", "Данные успешно сохранены")


def clear_fields(self):
    self.skzi_name_cb.setCurrentText("")
    self.skzi_version_cb.setCurrentText("")
    self.dateedit7.date()  # просто вызываем, без очистки
    self.doc_info_skzi.setText("")
    self.reg_number_le.setText("")
    self.from_whom_cb.setCurrentText("")
    self.location_TOM.setText("")
    self.note_cb.setCurrentText("")
    self.additional_le.setText("")
    self.certnum_le.setText("")
    self.dateedit2.date()
    self.owners.setCurrentText("")
    self.fullname_owner.setText("")
    self.location.setText("")
    self.contract_skzi.setText("")
    self.buss_proc.setCurrentText("")


def fetch_distinct_options(column_name: str) -> list:
    """
    Выбирает уникальные значения для указанного столбца из таблицы SCZY.
    """
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
        query = f"""
            SELECT DISTINCT {column_name} FROM SCZY
            WHERE {column_name} IS NOT NULL AND TRIM({column_name}) != ''
            ORDER BY {column_name}
        """
        cursor.execute(query)
        results = cursor.fetchall()
        connection.close()
        # Формируем список значений; предполагаем, что результат имеет вид: [{"имя_столбца": value}, ...]
        return [row[column_name] for row in results]
    except Exception as e:
        print(f"Ошибка при загрузке данных для {column_name}: {e}")
        return []


def populate_combobox_with_db(combo_box: QComboBox, column_name: str):
    """
    Очищает combo_box и заполняет его уникальными значениями из указанного столбца БД.
    """
    options = fetch_distinct_options(column_name)
    combo_box.clear()
    for option in options:
        combo_box.addItem(option)
    completer = QCompleter(options)
    completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    combo_box.setCompleter(completer)


def refresh_comboboxes(self):
    """
    Обновляет выпадающие списки, заполняемые данными из базы.
    При этом используются уже реализованные функции для заполнения списка.
    """
    populate_combobox_with_db(self.skzi_name_cb, "name_of_SCZY")
    populate_combobox_with_db(self.skzi_version_cb, "number_SCZY")
    populate_combobox_with_db(self.owners, "owners")
    populate_combobox_with_db(self.from_whom_cb, "owner")
    populate_combobox_with_db(self.note_cb, "note")
    populate_combobox_with_db(self.buss_proc, "buss_proc")

