import getpass
from datetime import datetime

import pymysql
from PyQt6 import QtWidgets
from PyQt6.QtGui import QKeySequence, QShortcut, QPalette, QColor
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit,
    QRadioButton, QHBoxLayout, QComboBox, QGroupBox, QFormLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
)
from PyQt6.QtCore import Qt, QDate, QTimer
from logic.db import enter_license


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



def create_page6(self) -> QWidget:
    # ---- Создаём страницу и настраиваем тёмный фон ----
    page = QWidget()
    page.setStyleSheet("background-color: #121212; color: white;")
    main_layout = QVBoxLayout(page)
    main_layout.setContentsMargins(20, 20, 20, 20)
    main_layout.setSpacing(15)

    # 4. Подключаемся к БД (при необходимости можно использовать подключение для других операций)
    connection = pymysql.connect(
        host="localhost",
        port=3306,
        user="newuser",
        password="852456qaz",
        database="IB",
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    connection.close()  # Для примера сразу закрываем

    escape_shortcut = QShortcut(QKeySequence("Escape"), page)
    escape_shortcut.activated.connect(self.go_to_second_page)
    btn_back = QPushButton("Назад")
    btn_back.setStyleSheet( "background-color: #333333; color: white; font-size: 15px; "
        "border: 1px solid #555; border-radius: 4px; padding: 5px;")
    btn_back.clicked.connect(self.go_to_second_page)
    btn_back.setMinimumSize(150, 30)
    main_layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignLeft)

    # Заголовок
    header_label = QLabel("Лицензии")
    header_label.setWordWrap(True)
    header_label.setStyleSheet("font-size: 20px; color: white;")
    header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    main_layout.addWidget(header_label)

    # Основной горизонтальный лэйаут (левая и правая части формы)
    h_layout = QHBoxLayout()
    h_layout.setSpacing(30)
    main_layout.addLayout(h_layout)

    # ---------- ЛЕВЫЙ БЛОК (Данные заявки) ----------
    left_group = QGroupBox("Данные заявки")
    left_group.setStyleSheet("""
        QGroupBox {
            background-color: #1e1e1e;
            border: 1px solid #444;
            border-radius: 5px;
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
    left_group_layout = QFormLayout()
    left_group_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
    left_group.setLayout(left_group_layout)

    # ---- Номер заявки ----
    self.enter_number = QLineEdit(self)
    self.enter_number.setPlaceholderText("Введите номер заявки")
    palette = self.enter_number.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    self.enter_number.setPalette(palette)
    left_group_layout.addRow(QLabel("Номер заявки:"), self.enter_number)
    # Подключаем проверку: должно состоять только из цифр и не быть пустым.
    self.enter_number.textChanged.connect(
        lambda: update_line_edit_style(
            self.enter_number,
            not (self.enter_number.text() and self.enter_number.text().isdigit())
        )
    )

    # ---- Комбобокс "Наименование ПО СКЗИ" ----
    self.combobox = QComboBox(self)
    self.combobox.setEditable(True)
    self.combobox.setStyleSheet("""
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
    line_edit = self.combobox.lineEdit()
    line_edit.setPlaceholderText("Наименование ПО СКЗИ")
    palette = line_edit.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    line_edit.setPalette(palette)
    for option in ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]:
        self.combobox.addItem(option)
    self.combobox.clearEditText()
    left_group_layout.addRow(QLabel("Выберите ПО СКЗИ:"), self.combobox)
    # Подключаем проверку комбобокса
    self.combobox.lineEdit().textChanged.connect(
        lambda: update_combobox_style(
            self.combobox,
            len(self.combobox.currentText().strip()) == 0
        )
    )

    # ---- Поле "Ключ" ----
    self.enter_key = QLineEdit(self)
    self.enter_key.setPlaceholderText("Введите ключ (например, test)")
    palette = self.enter_key.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    self.enter_key.setPalette(palette)
    left_group_layout.addRow(QLabel("Ключ:"), self.enter_key)
    self.enter_key.textChanged.connect(
        lambda: update_line_edit_style(self.enter_key, len(self.enter_key.text().strip()) == 0)
    )

    # ---- Комбобокс "Область применения" ----
    self.scope = QComboBox(self)
    self.scope.setEditable(True)
    self.scope.setStyleSheet("""
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
    line_edit = self.scope.lineEdit()
    line_edit.setPlaceholderText("Область применения")
    palette = line_edit.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    line_edit.setPalette(palette)
    for option in ["Option 1", "Option 2", "Option 3"]:
        self.scope.addItem(option)
    self.scope.clearEditText()
    left_group_layout.addRow(QLabel("Область/сфера:"), self.scope)
    self.scope.lineEdit().textChanged.connect(
        lambda: update_combobox_style(
            self.scope,
            len(self.scope.currentText().strip()) == 0
        )
    )

    # ---- Поле "ФИО пользователя" ----
    self.input_fio_user = QLineEdit(self)
    self.input_fio_user.setPlaceholderText("Введите ФИО пользователя")
    palette = self.input_fio_user.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    self.input_fio_user.setPalette(palette)
    left_group_layout.addRow(QLabel("ФИО пользователя:"), self.input_fio_user)
    self.input_fio_user.textChanged.connect(
        lambda: update_line_edit_style(self.input_fio_user, len(self.input_fio_user.text().strip()) <= 3)
    )

    # ---- Поле "Имя APM/IP" ----
    self.input_apm = QLineEdit(self)
    self.input_apm.setPlaceholderText("Введите имя APM/IP")
    palette = self.input_apm.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    self.input_apm.setPalette(palette)
    left_group_layout.addRow(QLabel("Имя AP/IP:"), self.input_apm)
    self.input_apm.textChanged.connect(
        lambda: update_line_edit_style(self.input_apm, len(self.input_apm.text().strip()) <= 3)
    )

    # Добавляем левый блок в горизонтальный лэйаут
    h_layout.addWidget(left_group, 1)

    # ---------- ПРАВЫЙ БЛОК (Информация об установке) ----------
    right_group = QGroupBox("Информация об установке")
    right_group.setStyleSheet("""
        QGroupBox {
            background-color: #1e1e1e;
            border: 1px solid #444;
            border-radius: 5px;
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
    right_group_layout = QFormLayout()
    right_group_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
    right_group.setLayout(right_group_layout)

    # ---- Календарь (дата) ----
    self.dateedit = QtWidgets.QDateEdit(calendarPopup=True)
    self.dateedit.setDateTime(datetime.today())
    self.dateedit.setMaximumSize(100, 40)
    self.dateedit.setStyleSheet("""
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
    right_group_layout.addRow(QLabel("Дата выдачи:"), self.dateedit)

    # Подключаем проверку изменения даты
    self.dateedit.dateChanged.connect(
        lambda date: self.dateedit.setStyleSheet(
            "background-color: #1e1e1e; border: 1px solid red; border-radius: 4px; padding: 2px; color: white;"
            if not date.isValid()
            else "background-color: #1e1e1e; border: 1px solid #444; border-radius: 4px; padding: 2px; color: white;"
        )
    )

    # ---- Поле "Сотрудник ИБ" ----
    self.user = QLineEdit(self)
    self.user.setPlaceholderText("Введите ФИО сотрудника ИБ")
    palette = self.user.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    self.user.setPalette(palette)
    right_group_layout.addRow(QLabel("Сотрудник ИБ:"), self.user)
    self.user.textChanged.connect(
        lambda: update_line_edit_style(self.user, len(self.user.text().strip()) <= 3)
    )

    # ---- Статус лицензии (радиокнопки) ----
    self.status_group = QGroupBox("Статус лицензии")
    self.status_group.setStyleSheet("QGroupBox { background-color: transparent; border: none; }")
    status_layout = QVBoxLayout()
    self.status_group.setLayout(status_layout)
    radio_style = """
        QRadioButton {
            font-size: 16px;
            color: white;
            padding: 5px;
        }
        QRadioButton:checked {
            color: rgb(139, 197, 64);
        }
        QRadioButton::indicator {
            width: 15px;
            height: 15px;
        }
    """
    self.rb_issued = QRadioButton("Выдано")
    self.rb_issued.setStyleSheet(radio_style)
    self.rb_installed = QRadioButton("Установлено")
    self.rb_installed.setStyleSheet(radio_style)
    self.rb_taken = QRadioButton("Изьято")
    self.rb_taken.setStyleSheet(radio_style)
    status_layout.addWidget(self.rb_issued)
    status_layout.addWidget(self.rb_installed)
    status_layout.addWidget(self.rb_taken)
    right_group_layout.addRow(self.status_group)

    # Подключаем изменение видимости дополнительных полей (например, для статуса "Изьято")
    self.rb_issued.toggled.connect(self.update_extra_fields_visibility)
    self.rb_installed.toggled.connect(self.update_extra_fields_visibility)
    self.rb_taken.toggled.connect(self.update_extra_fields_visibility)

    # ---- Кнопка "Сохранить" ----
    self.save_button = QPushButton("Сохранить", self)
    self.save_button.setStyleSheet("background-color: #333; color: white; padding: 5px 10px; border-radius: 3px;")
    right_group_layout.addRow(self.save_button)
    self.save_button.clicked.connect(lambda: save_values6(self))

    # Добавляем правый блок в горизонтальный лэйаут
    h_layout.addWidget(right_group, 1)

    # ---------- Дополнительные поля (изъятие/уничтожение) ----------
    self.extra_group = QGroupBox("Дополнительные сведения")
    self.extra_group.setStyleSheet("""
        QGroupBox {
            background-color: #1e1e1e;
            border: 1px solid #444;
            border-radius: 5px;
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
    extra_layout = QFormLayout()
    self.extra_group.setLayout(extra_layout)
    self.extra_group.setVisible(False)

    self.input_date = QLineEdit(self)
    self.input_date.setPlaceholderText("Дата, расписка, номер акта об уничтожении...")
    palette = self.input_date.palette()
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(98, 150, 30))
    self.input_date.setPalette(palette)
    extra_layout.addRow(QLabel("Документ/дата:"), self.input_date)
    main_layout.addWidget(self.extra_group)

    # --- Кнопки и ярлыки ---
    enter_shortcut = QShortcut(QKeySequence("Return"), page)
    enter_shortcut.activated.connect(lambda: save_values6(self))

    # --- Добавление внизу страницы виджета с таблицей и поиском ---
    data_table_widget = create_data_table(self)
    main_layout.addWidget(data_table_widget)

    # --- Создаем таймер для периодического обновления таблицы ---
    self.refresh_timer = QTimer(self)
    self.refresh_timer.setInterval(60000)  # 60 секунд
    self.refresh_timer.timeout.connect(lambda: load_data(self))
    self.refresh_timer.start()

    return page


def create_data_table(self) -> QWidget:
    """
    Создает виджет с поисковой строкой и таблицей для отображения последних записей из таблицы License.
    """
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setSpacing(5)

    # Поисковая строка
    search_layout = QHBoxLayout()
    search_label = QLabel("Поиск:")
    self.search_line = QLineEdit()
    self.search_line.setPlaceholderText("Введите текст для поиска...")
    search_layout.addWidget(search_label)
    search_layout.addWidget(self.search_line)
    layout.addLayout(search_layout)

    # Таблица для отображения данных
    self.table_widget = QTableWidget()
    # Количество колонок согласно структуре таблицы License
    self.table_widget.setColumnCount(12)
    self.table_widget.setRowCount(5)
    self.table_widget.setHorizontalHeaderLabels([
        "ID", "Номер", "ПО", "Номер ключа", "Область применения",
        "ФИО пользователя", "APM", "Дата", "ФИО IT", "Статус", "Отметка", "Дата документа"
    ])
    self.table_widget.horizontalHeader().setStretchLastSection(True)
    self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    layout.addWidget(self.table_widget)

    # При изменении текста в поисковой строке перезагружаем данные
    self.search_line.textChanged.connect(lambda: load_data(self))
    # Первоначальная загрузка данных
    load_data(self)

    return widget


def load_data(self):
    """
    Загружает из базы данных последние 50 записей из таблицы License.
    Если введен текст в поисковой строке, выполняется фильтрация по полям: номер заявки, наименование ПО, ФИО пользователя.
    """
    search_text = self.search_line.text().strip()
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
                SELECT * FROM License
                WHERE CAST(number AS CHAR) LIKE %s 
                   OR name_of_soft LIKE %s 
                   OR fullname LIKE %s
                ORDER BY ID DESC
                LIMIT 50
            """
            like_pattern = f"%{search_text}%"
            cursor.execute(query, (like_pattern, like_pattern, like_pattern))
        else:
            query = "SELECT * FROM License ORDER BY ID DESC LIMIT 500"
            cursor.execute(query)
        results = cursor.fetchall()
        connection.close()
        self.table_widget.setStyleSheet("QTableWidget { font-size: 11pt; }")
        self.table_widget.setRowCount(len(results))
        for row_idx, row_data in enumerate(results):
            # Порядок колонок: ID, number, name_of_soft, number_lic, scop_using,
            # fullname, name_apm, date, fullname_it, status, input_mark, input_date
            columns = [
                row_data.get("ID"),
                row_data.get("number"),
                row_data.get("name_of_soft"),
                row_data.get("number_lic"),
                row_data.get("scop_using"),
                row_data.get("fullname"),
                row_data.get("name_apm"),
                row_data.get("date"),
                row_data.get("fullname_it"),
                row_data.get("status"),
                row_data.get("input_mark"),
                row_data.get("input_date"),
            ]

            for col_idx, value in enumerate(columns):
                item = QTableWidgetItem(str(value) if value is not None else "")
                self.table_widget.setItem(row_idx, col_idx, item)

        for row in range(self.table_widget.rowCount()):
            self.table_widget.setRowHeight(row, 40)
    except Exception as e:
        print("Ошибка загрузки данных:", e)


def save_values6(self):
    errors = []

    # Проверка всех полей и сбор ошибок
    enter_number = self.enter_number.text()
    if enter_number.isalpha() or len(enter_number) == 0:
        errors.append("Поле 'Номер' должно содержать ТОЛЬКО цифры и не быть пустым")

    combobox = self.combobox.currentText()
    if len(combobox) == 0:
        errors.append("Не выбрано значение статуса")

    enter_key = self.enter_key.text()
    if len(enter_key) == 0:
        errors.append("Поле 'Ключ' не может быть пустым")

    scope = self.scope.currentText()
    if len(scope) == 0:
        errors.append("Не выбрана 'Область'")

    input_fio_user = self.input_fio_user.text()
    if len(input_fio_user) <= 3:
        errors.append("ФИО пользователя должно содержать более 3 символов")

    name_apm = self.input_apm.text()
    if len(name_apm) <= 3:
        errors.append("Название АРМ должно содержать более 3 символов")

    dateedit = self.dateedit.date()
    if not dateedit.isValid():
        errors.append("Неверная дата")

    user = self.user.text()
    if len(user) <= 3:
        errors.append("Имя пользователя должно содержать более 3 символов")

    # Проверка radio buttons
    if not (self.rb_issued.isChecked() or self.rb_installed.isChecked() or self.rb_taken.isChecked()):
        errors.append("Не выбран статус")
    else:
        if self.rb_issued.isChecked():
            status = 1
            input_mark = ""
        elif self.rb_installed.isChecked():
            status = 2
            input_mark = ""
        elif self.rb_taken.isChecked():
            status = 3
            input_mark = "True"

    if errors:
        error_message = "Обнаружены ошибки:\n\n" + "\n".join(f"• {error}" for error in errors)
        QMessageBox.critical(self, "Ошибка заполнения", error_message)
        return

    input_date = self.input_date.text()

    data = {
        "enter_number": enter_number,
        "combobox": combobox,
        "enter_key": enter_key,
        "scope": scope,
        "input_fio_user": input_fio_user,
        "name_APM": name_apm,
        "dateedit": dateedit.toString("yyyy-MM-dd"),
        "user": user,
        "status": status,
        "input_mark": input_mark,
        "input_date": input_date,
    }

    print("Сохранённые данные:", data)
    dateedit_str = dateedit.toPyDate().strftime('%Y-%m-%d')
    enter_license(enter_number, combobox, enter_key, scope, input_fio_user,
                  name_apm, dateedit_str, user, status, input_mark, input_date)
    clear_fields(self)
    load_data(self)

    QMessageBox.information(self, "Успех", "Данные успешно сохранены")


def clear_fields(self):
    self.enter_number.clear()
    self.enter_key.clear()
    self.input_fio_user.clear()
    self.input_apm.clear()
    self.user.clear()
    self.input_date.clear()
    self.combobox.clearEditText()
    self.combobox.setCurrentIndex(-1)
    self.scope.clearEditText()
    self.scope.setCurrentIndex(-1)
    self.dateedit.setDate(QDate.currentDate())
    for rb in (self.rb_issued, self.rb_installed, self.rb_taken):
        rb.setAutoExclusive(False)
        rb.setChecked(False)
        rb.setAutoExclusive(True)
    self.extra_group.setVisible(False)


def update_extra_fields_visibility(self):
    """
    Показывает блок 'Дополнительные сведения', если выбрана опция "Изьято".
    """
    self.extra_group.setVisible(self.rb_taken.isChecked())
