# page6_light.py
from PyQt6.QtCore import Qt, QTimer, QDate
from PyQt6.QtGui import QFontDatabase, QShortcut, QKeySequence, QColor, QPixmap, QIcon
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout, QFrame,
    QLabel, QPushButton, QRadioButton, QScrollArea, QLineEdit, QComboBox,
    QDateEdit, QTableWidget, QHeaderView, QTableWidgetItem, QApplication,
    QGraphicsDropShadowEffect, QMessageBox, QStyledItemDelegate, QStyleOptionViewItem, QAbstractItemView, QToolButton,
    QSizePolicy
)

from ui.page1 import load_gilroy, BG, ACCENT, TXT_DARK, CARD_R, PAD_H, PAD_V
from ui.page7 import (          # берём фабрики/стили из «красивой» 7-й страницы
    _edit, _combo, _btn, _hline, _vline,
    set_edit_error_style, set_combo_error_style
)
from logic.db import enter_license
from PyQt6.QtCore import Qt, QTimer, QDate, QEvent

import pymysql
from datetime import datetime


# ————————————————————————————————————
CARD_W = 1300          # ширина «карточки»
PAD_H  = 20            # внутренние отступы
PAD_V  = 16
# ————————————————————————————————————


# ╔═══════════════════════════════════════════════════════════════════╗
# ║   С О З Д А Н И Е   С Т Р А Н И Ц Ы   « Л И Ц Е Н З И И »         ║
# ╚═══════════════════════════════════════════════════════════════════╝
def create_page6(self) -> QWidget:
    fam, sty = load_gilroy()
    f_h1   = QFontDatabase.font(fam, sty, 28)
    f_body = QFontDatabase.font(fam, sty, 12)

    page = QWidget()
    page.setStyleSheet(f"background:{BG};")
    QApplication.setFont(f_body)

    root = QVBoxLayout(page)
    root.setContentsMargins(16, 16, 16, 16)
    root.setSpacing(8)

    # ——— заголовок ———
    ttl = QLabel("Лицензии")
    ttl.setFont(f_h1)
    ttl.setStyleSheet(f"color:#fff;border-bottom:3px solid {ACCENT};padding-bottom:4px;")
    root.addWidget(ttl, alignment=Qt.AlignmentFlag.AlignLeft)

    # ESC → назад
    QShortcut(QKeySequence("Escape"), page).activated.connect(self.go_to_second_page)

    # ——— прокручиваемая карточка ———
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setFrameShape(QFrame.Shape.NoFrame)
    scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    root.addWidget(scroll)

    wrapper  = QWidget()
    wrap_lay = QVBoxLayout(wrapper); wrap_lay.setContentsMargins(0, 0, 0, 0)

    card = QFrame()
    card.setMinimumWidth(CARD_W)
    card.setStyleSheet(f"background:#fff;border-radius:{CARD_R}px;")
    card.setGraphicsEffect(QGraphicsDropShadowEffect(
        blurRadius=32, xOffset=0, yOffset=4, color=QColor(0, 0, 0, 55)))
    wrap_lay.addWidget(card)
    scroll.setWidget(wrapper)

    cbox = QVBoxLayout(card)
    cbox.setContentsMargins(PAD_H, PAD_V // 2, PAD_H, PAD_V // 2)

    # ── кнопка «← Назад» внутри карточки ─────────────────────────

    hdr = QWidget()
    hb = QHBoxLayout(hdr)
    hb.setContentsMargins(0, 0, 0, 0)
    hb.setSpacing(0)
    back_btn = _btn("←", 34)
    back_btn.setFixedWidth(42)
    back_btn.clicked.connect(self.go_to_second_page)
    hb.addWidget(back_btn, 0, Qt.AlignmentFlag.AlignLeft)
    hb.addStretch(1)
    cbox.addWidget(hdr)
    # ========== Форма ==========
    form = _build_form(self, fam, sty, f_body)
    cbox.addWidget(form)

        # ——— кнопка «Сохранить» ———
    btn_save = _btn("Сохранить", 30)
    btn_save.clicked.connect(lambda: save_values6(self))
    cbox.addSpacing(4)
    cbox.addWidget(btn_save, alignment=Qt.AlignmentFlag.AlignHCenter)

    # ——— таблица + поиск ———
    cbox.addWidget(create_data_table(self))



    # Enter → сохранить
    QShortcut(QKeySequence("Return"), page).activated.connect(lambda: save_values6(self))



    # Enter → сохранить
    QShortcut(QKeySequence("Return"), page).activated.connect(lambda: save_values6(self))

    fill_recent_values6(self)  # ← добавили
    return page


# ╔═══════════════════════════════════════════════════════════════════╗
# ║   П О С Т Р О Й К А   Ф О Р М Ы                                   ║
# ╚═══════════════════════════════════════════════════════════════════╝
def _build_form(self, fam, sty, f_body) -> QWidget:
    f_group = QFontDatabase.font(fam, sty, 14); f_group.setBold(True)

    frame = QFrame()
    frame.setStyleSheet("border:1px solid #d0d0d0;border-radius:8px;")
    grid  = QGridLayout(frame)
    grid.setContentsMargins(12, 12, 12, 12)
    grid.setHorizontalSpacing(20)
    grid.setVerticalSpacing(8)

    # заголовки секций
    for col, title in enumerate(("Данные заявки", "Информация об установке")):
        lbl = QLabel(title); lbl.setFont(f_group)
        lbl.setStyleSheet(f"color:{TXT_DARK};border:none;")
        grid.addWidget(lbl, 0, col * 2)

    grid.addWidget(_hline(ACCENT, 1), 1, 0, 1, 3)
    grid.addWidget(_vline(),          2, 1, 1, 1)

    FL, FR = QFormLayout(), QFormLayout()
    for F in (FL, FR):
        F.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        F.setVerticalSpacing(6)
        F.setHorizontalSpacing(18)
        F.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)

    grid.addLayout(FL, 2, 0)
    grid.addLayout(FR, 2, 2)
    grid.setColumnStretch(0, 1)
    grid.setColumnStretch(2, 1)

    # —— левый столбец
    self.enter_number   = _edit("Номер заявки", f_body)
    self.combobox       = _combo("Наименование ПО СКЗИ",
                                 ["CryptoPro CSP", "ViPNet CSP", "Signal-Com"],
                                 f_body)
    self.enter_key      = _edit("Ключ", f_body)
    self.scope          = _combo("Область применения", [], f_body)
    self.input_fio_user = _edit("ФИО пользователя", f_body)
    self.input_apm      = _edit("Имя APM / IP",  f_body)

    FL.addRow("Номер заявки",         self.enter_number)
    FL.addRow("Наименование ПО СКЗИ", self.combobox)
    FL.addRow("Ключ",                 self.enter_key)
    FL.addRow("Область / сфера",      self.scope)
    FL.addRow("ФИО пользователя",     self.input_fio_user)
    FL.addRow("Имя APM / IP",         self.input_apm)


    # —— правый столбец
    self.dateedit = QDateEdit(calendarPopup=True)
    self.dateedit.setDate(QDate.currentDate())
    self.dateedit.setFixedHeight(34); self.dateedit.setFont(f_body)

    self.dateedit.setStyleSheet("""
            /* ─ Навигационная панель ─────────────────────────── */
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background: #ffffff;              /* белый фон */
            }

            /* Все кнопки на панели */
            QCalendarWidget QToolButton {
                background: transparent;
                color: #000000;                  /* ЧЁРНЫЙ текст всегда виден */
                height: 24px;
                margin: 2px;
            }
            QCalendarWidget QToolButton:hover {   /* лёгкая подсветка при наведении */
                background: rgba(0,0,0,0.06);
            }
        """)
    self.user = _edit("Сотрудник ИБ", f_body)

    for btn_name, char in (("qt_calendar_prevmonth", "‹"),
                           ("qt_calendar_nextmonth", "›")):
        cal = self.dateedit.calendarWidget()  # то же для dateedit2
        btn = cal.findChild(QToolButton, btn_name)
        btn.setText(char)
        btn.setStyleSheet("color:#000; font:16px 'Gilroy'; background:transparent;")
        btn.setIcon(QIcon())  # убрать встроенную пиктограмму

    # радиокнопки статуса
    radio_box = QWidget(); rb_lay = QVBoxLayout(radio_box); rb_lay.setContentsMargins(0, 0, 0, 0)
    self.rb_issued    = QRadioButton("Выдано")
    self.rb_installed = QRadioButton("Установлено")
    self.rb_taken     = QRadioButton("Изъято")
    for rb in (self.rb_issued, self.rb_installed, self.rb_taken):
        rb.setStyleSheet(
            f"QRadioButton{{font-size:14px;color:{TXT_DARK};}}"
            f"QRadioButton:checked{{color:{ACCENT};}}"
        ); rb_lay.addWidget(rb)

    FR.addRow("Дата выдачи",   self.dateedit)
    FR.addRow("Сотрудник ИБ", self.user)
    FR.addRow("Статус",        radio_box)

    # дополнительное поле «Документ / дата»
    self.extra_lbl  = QLabel("Документ / дата")
    self.input_date = _edit("Дата, расписка, номер акта …", f_body)
    self.extra_lbl.hide(); self.input_date.hide()
    FR.addRow(self.extra_lbl, self.input_date)

    for form in (FL, FR):
        for i in range(form.rowCount()):
            lbl = form.itemAt(i, QFormLayout.ItemRole.LabelRole).widget()
            lbl.setStyleSheet(f"color:{TXT_DARK};border:none;background:transparent;padding:0;margin:0;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignLeft)

    # показать/скрыть дополнительное поле
    def _toggle():
        show = self.rb_taken.isChecked()
        self.extra_lbl.setVisible(show)
        self.input_date.setVisible(show)
    for rb in (self.rb_taken, self.rb_issued, self.rb_installed): rb.toggled.connect(_toggle)



    return frame




# ╔═══════════════════════════════════════════════════════════════════╗
# ║   Т А Б Л И Ц А   +   П О И С К                                   ║
# ╚═══════════════════════════════════════════════════════════════════╝
def create_data_table(self) -> QFrame:
    """
    Создаёт фрейм с полем поиска и таблицей,
    в которой можно править ячейки двойным кликом.
    """
    frame = QFrame()
    lay = QVBoxLayout(frame)
    lay.setContentsMargins(12, 12, 12, 12)
    fam, sty = load_gilroy()
    f_h2 = QFontDatabase.font(fam, sty, 10)

    """# ——— Инструкция по двойному клику ———
    attention_png = QLabel(self)
    pixmap = QPixmap('left_click.png') \
        .scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio)
    attention_png.setPixmap(pixmap)

    attention_6 = QLabel(
        "Редактирование таблицы"
    )
    attention_6.setFont(f_h2)

    attention_6_2 = QLabel(
        "Дублирование полей"
    )
    attention_6_2.setFont(f_h2)

    # Собираем картинку и текст в один горизонтальный layout,
    info_bar = QWidget()
    info_bar.setStyleSheet("background: transparent; border: none;")
    hbox_info = QHBoxLayout(info_bar)
    hbox_info.setContentsMargins(0, 0, 0, 0)
    hbox_info.setSpacing(8)  # отступ между виджетами
    attention_6.setAlignment(Qt.AlignmentFlag.AlignLeft)
    attention_png.setAlignment(Qt.AlignmentFlag.AlignLeft)
    attention_6_2.setAlignment(Qt.AlignmentFlag.AlignLeft)
    hbox_info.addWidget(attention_png)  # картинка
    hbox_info.addWidget(attention_6)  # текст
    hbox_info.addWidget(attention_6_2)

    lay.addWidget(info_bar)
"""
    frame.setStyleSheet("border:1px solid #d0d0d0;border-radius:3px;")
    # Поле поиска
    self.search_line = QLineEdit(placeholderText="Введите текст для поиска…")
    lay.addWidget(self.search_line, stretch=0)
    # Таблица
    self.table_widget = QTableWidget()
    self.table_widget.setSizePolicy(QSizePolicy.Policy.Expanding,
                                    QSizePolicy.Policy.Expanding)
    self.table_widget.setColumnCount(12)
    self.table_widget.setHorizontalHeaderLabels([
        "ID","Номер","ПО","№ лицензии","Область",
        "ФИО","APM","Дата","ФИО IT","Статус","Отметка","Документ/дата"
    ])
    self.table_widget.verticalHeader().setVisible(False)
    hdr = self.table_widget.horizontalHeader()
    # разрешаем перетаскивать и менять порядок
    hdr.setSectionsMovable(True)
    self.table_widget.verticalHeader().setSectionResizeMode(
        QHeaderView.ResizeMode.ResizeToContents
    )


    # Перенос текста без «…»
    self.table_widget.setWordWrap(True)
    self.table_widget.setTextElideMode(Qt.TextElideMode.ElideNone)
    class WrapDelegate(QStyledItemDelegate):
        def initStyleOption(self, option: QStyleOptionViewItem, index):
            super().initStyleOption(option, index)
            option.features |= QStyleOptionViewItem.ViewItemFeature.WrapText
    self.table_widget.setItemDelegate(WrapDelegate(self.table_widget))

    hdr = self.table_widget.horizontalHeader()
    hdr.setSectionsMovable(True)
    # последняя колонка будет «резиновой» и заполняет всё лишнее место
    hdr.setStretchLastSection(True)
    # задаём минимальный размер секции для всех колонок
    hdr.setMinimumSectionSize(30)

    # Стартовые режимы и ширины колонок (px)

    # минимальный размер для ЛЮБОГО столбца
    hdr.setMinimumSectionSize(30)


    # минимальный «хинт» для любой колонки
    hdr.setMinimumSectionSize(30)

    # стартовые ширины (px) для пропорций
    initial_widths = [15, 100, 100, 100, 150, 180, 100, 100, 180, 75, 100, 120]
    for col, w in enumerate(initial_widths):
        hdr.setSectionResizeMode(col, QHeaderView.ResizeMode.Interactive)
        hdr.resizeSection(col, w)



    # 1) Разрешаем редактирование ячеек
    self.table_widget.setEditTriggers(
        QAbstractItemView.EditTrigger.DoubleClicked |
        QAbstractItemView.EditTrigger.SelectedClicked
    )
    # 2) Подписываемся на изменение
    self.table_widget.itemChanged.connect(lambda item: on_license_item_changed(self, item))

    self.table_widget.viewport().installEventFilter(self)


    lay.addWidget(self.table_widget, stretch=1)

    # Поиск
    self.search_line.textChanged.connect(lambda: load_data(self))
    load_data(self)

    return frame




# ╔═══════════════════════════════════════════════════════════════════╗
# ║   З А Г Р У З К А   Д А Н Н Ы Х                                   ║
# ╚═══════════════════════════════════════════════════════════════════╝
def load_data(self):
    """
    Загружает данные в таблицу License,
    при поиске фильтруя по всем столбцам.
    """
    search_text = self.search_line.text().strip()
    try:
        con = pymysql.connect(
            host="localhost", port=3306, user="newuser", password="852456qaz",
            database="IB", charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )
        cur = con.cursor()
        if search_text:
            patt = f"%{search_text}%"
            cur.execute("""
                SELECT * FROM License
                WHERE CAST(ID           AS CHAR) LIKE %s
                   OR CAST(number       AS CHAR) LIKE %s
                   OR name_of_soft             LIKE %s
                   OR number_lic               LIKE %s
                   OR scop_using               LIKE %s
                   OR fullname                 LIKE %s
                   OR name_apm                 LIKE %s
                   OR CAST(date          AS CHAR) LIKE %s
                   OR fullname_it              LIKE %s
                   OR CAST(status       AS CHAR) LIKE %s
                   OR input_mark               LIKE %s
                   OR input_date               LIKE %s
                ORDER BY ID DESC
                LIMIT 50
            """, (patt,)*12)
        else:
            cur.execute("SELECT * FROM License ORDER BY ID DESC LIMIT 500")

        rows = cur.fetchall()
        con.close()

        # Блокируем сигнал itemChanged, чтобы не реагировать на программное заполнение
        self.table_widget.blockSignals(True)
        self.table_widget.setRowCount(len(rows))
        for r, row in enumerate(rows):
            columns = [
                row.get("ID"),
                row.get("number"),
                row.get("name_of_soft"),
                row.get("number_lic"),
                row.get("scop_using"),
                row.get("fullname"),
                row.get("name_apm"),
                row.get("date"),
                row.get("fullname_it"),
                row.get("status"),
                row.get("input_mark"),
                row.get("input_date")
            ]
            for c, val in enumerate(columns):
                item = QTableWidgetItem(str(val) if val is not None else "")
                # выравниваем по левому краю
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.table_widget.setItem(r, c, item)
        self.table_widget.resizeRowsToContents()
        self.table_widget.blockSignals(False)

    except Exception as e:
        print("Ошибка загрузки данных:", e)

def on_license_item_changed(self, item: QTableWidgetItem):
    """
    При ручном редактировании ячейки: сохраняем новое значение в БД.
    ID (столбец 0) не правим.
    """
    if item.column() == 0:
        return

    field_names = [
        "ID", "number", "name_of_soft", "number_lic", "scop_using",
        "fullname", "name_apm", "date", "fullname_it", "status",
        "input_mark", "input_date"
    ]
    field = field_names[item.column()]
    record_id = self.table_widget.item(item.row(), 0).text()
    new_value = item.text()

    try:
        con = pymysql.connect(
            host="localhost", port=3306, user="newuser", password="852456qaz",
            database="IB", charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )
        cur = con.cursor()
        cur.execute(f"UPDATE License SET `{field}` = %s WHERE ID = %s",
                    (new_value, record_id))
        con.commit()
        con.close()
    except Exception as e:
        QMessageBox.critical(self, "Ошибка сохранения", str(e))

# ╔═══════════════════════════════════════════════════════════════════╗
# ║   С О Х Р А Н Е Н И Е   В   Б Д                                   ║
# ╚═══════════════════════════════════════════════════════════════════╝
def save_values6(self):
    # — проверки (оставлены прежними) —
    errors = []

    if len(self.enter_number.text()) <= 0:
        errors.append("Поле «Номер» не должно быть пустым.")
    if len(self.combobox.currentText()) <= 0:
        errors.append("«ПО СКЗИ» не должно быть пустым.")
    if len(self.enter_key.text()) <= 0:
        errors.append("Поле «Ключ» не должно быть пустым.")
    if len(self.scope.currentText()) <= 0:
        errors.append("Поле «Область применения» не должно быть пустым")
    if len(self.input_fio_user.text()) <= 0:
        errors.append("Поле «ФИО пользователя» не должно быть пустым")
    if len(self.input_apm.text()) <= 0:
        errors.append("Поле «Имя APM/IP» не должно быть пустым")
    if len(self.user.text()) <= 0:
        errors.append("Поле «ФИО сотрудника ИБ» не должно быть пустым")
    if not (self.rb_issued.isChecked() or self.rb_installed.isChecked() or self.rb_taken.isChecked()):
        errors.append("Не выбран статус")


    # статус / отметка
    if self.rb_issued.isChecked():
        status, mark = 1, "Выдано"
    elif self.rb_installed.isChecked():
        status, mark = 2, "Установлено"
    else:
        status, mark = 3, "Изъято"
        if len(self.input_date.text()) <= 0:
            errors.append("Поле «Документ / Дата» не должно быть пустым")

    if errors:
        QMessageBox.critical(self, "Ошибка заполнения",
                             "Обнаружены ошибки:\n\n• " + "\n• ".join(errors))
        return

    # запись
    enter_license(
        self.enter_number.text(),               self.combobox.currentText(),
        self.enter_key.text(),                  self.scope.currentText(),
        self.input_fio_user.text(),             self.input_apm.text(),
        self.dateedit.date().toString("yyyy-MM-dd"),
        self.user.text(),                       status,
        mark,                                   self.input_date.text()
    )

    clear_fields(self)
    load_data(self)
    fill_recent_values6(self)
    QMessageBox.information(self, "Успех", "Данные успешно сохранены")



# ╔═══════════════════════════════════════════════════════════════════╗
# ║   С Б Р О С   Ф О Р М Ы                                           ║
# ╚═══════════════════════════════════════════════════════════════════╝
def clear_fields(self):
    for w in (
        self.enter_number, self.enter_key, self.input_fio_user,
        self.input_apm, self.user, self.input_date
    ):
        w.clear()

    self.combobox.setCurrentIndex(-1)
    self.scope.setCurrentIndex(-1); self.scope.clearEditText()
    self.dateedit.setDate(QDate.currentDate())

    self.extra_lbl.hide(); self.input_date.hide()
    for rb in (self.rb_issued, self.rb_installed, self.rb_taken):
        rb.setAutoExclusive(False); rb.setChecked(False); rb.setAutoExclusive(True)



# ────────────────────────────────────────────────────────────────
def fill_recent_values6(self, limit: int = 5) -> None:
    """
    Берём последние `limit` строк из таблицы License и
    добавляем уникальные значения в ComboBox-ы:
        • self.combobox   – «Наименование ПО СКЗИ»  (поле name_of_soft)
        • self.scope      – «Область применения»    (поле scop_using)
    Повторов не создаём — новые элементы вставляем в начало списков.
    """
    try:
        con = pymysql.connect(host="localhost", port=3306, user="newuser",
                              password="852456qaz", database="IB",
                              charset="utf8mb4",
                              cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        cur.execute("""
            SELECT DISTINCT name_of_soft, scop_using
            FROM License
            WHERE name_of_soft <> '' AND scop_using <> ''
            ORDER BY ID DESC
            LIMIT %s
        """, (limit,))
        rows = cur.fetchall()
        con.close()

        # множества уникальных значений
        names  = {r["name_of_soft"] for r in rows if r["name_of_soft"]}
        scopes = {r["scop_using"]   for r in rows if r["scop_using"]}

        def _sync(cb: QComboBox, values: set[str]):
            """Добавить в ComboBox уникальные values, НЕ изменяя текущее поле."""
            if not values:
                return
            old = {cb.itemText(i) for i in range(cb.count())}
            new = [v for v in values if v not in old]

            if new:
                # запомним, был ли выбран элемент
                had_selection = cb.currentIndex() != -1
                cb.insertItems(0, new)
                # если до вставки выбор отсутствовал — вернём состояние «пусто»
                if not had_selection:
                    cb.setCurrentIndex(-1)  # ← ключевая строка
                    cb.clearEditText()  # убираем текст из lineEdit

        _sync(self.combobox, names)
        _sync(self.scope,    scopes)

    except Exception as e:
        print("fill_recent_values6 error:", e)



def on_row_double_clicked(self, item: QTableWidgetItem):
    """При двойном клике заполняем форму данными из выбранной строки."""
    row = item.row()
    # вспомогательная лямбда — безопасно вытягивает текст
    get = lambda col: self.table_widget.item(row, col).text() if self.table_widget.item(row, col) else ""

    # читаем колонки по их индексам
    num       = get(1)
    po        = get(2)
    lic_num   = get(3)
    area      = get(4)
    fio_user  = get(5)
    apm       = get(6)
    date_str  = get(7)
    fio_it    = get(8)
    status_v  = get(9)
    doc_mark  = get(10)
    doc_date  = get(11)

    # заполняем поля формы
    self.enter_number.setText(num)
    self.combobox.lineEdit().setText(po)
    self.enter_key.setText(lic_num)
    self.scope.lineEdit().setText(area)
    self.input_fio_user.setText(fio_user)
    self.input_apm.setText(apm)

    dt = QDate.fromString(date_str, "yyyy-MM-dd")
    if dt.isValid():
        self.dateedit.setDate(dt)

    self.user.setText(fio_it)

    # статус: 1=Выдано,2=Установлено,3=Изъято
    self.rb_issued.setChecked(status_v == "1")
    self.rb_installed.setChecked(status_v == "2")
    self.rb_taken.setChecked(status_v == "3")

    # показываем/скрываем поле «Документ/дата» и заполняем его
    self.extra_lbl.setVisible(self.rb_taken.isChecked())
    self.input_date.setVisible(self.rb_taken.isChecked())
    self.input_date.setText(doc_date)



