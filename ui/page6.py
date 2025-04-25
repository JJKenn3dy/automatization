# page6_light.py
from PyQt6.QtCore import Qt, QTimer, QDate
from PyQt6.QtGui  import QFontDatabase, QShortcut, QKeySequence, QColor
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout, QFrame,
    QLabel, QPushButton, QRadioButton, QScrollArea, QLineEdit, QComboBox,
    QDateEdit, QTableWidget, QHeaderView, QTableWidgetItem, QApplication,
    QGraphicsDropShadowEffect, QMessageBox
)

from ui.page1 import load_gilroy, BG, ACCENT, TXT_DARK, CARD_R, PAD_H, PAD_V
from ui.page7 import (          # берём фабрики/стили из «красивой» 7-й страницы
    _edit, _combo, _btn, _hline, _vline,
    set_edit_error_style, set_combo_error_style
)
from logic.db import enter_license

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

    # таймер авто-обновления
    self.refresh_timer = QTimer(page)
    self.refresh_timer.setInterval(60_000)
    self.refresh_timer.timeout.connect(lambda: load_data(self))
    self.refresh_timer.start()

    # Enter → сохранить
    QShortcut(QKeySequence("Return"), page).activated.connect(lambda: save_values6(self))

    self.refresh_timer.start()

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

    self.user = _edit("Сотрудник ИБ", f_body)

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

    # показать/скрыть дополнительное поле
    def _toggle():
        show = self.rb_taken.isChecked()
        self.extra_lbl.setVisible(show)
        self.input_date.setVisible(show)
    for rb in (self.rb_taken, self.rb_issued, self.rb_installed): rb.toggled.connect(_toggle)

    # валидация
    self.enter_number.textChanged.connect(
        lambda: set_edit_error_style(self.enter_number,
                not (self.enter_number.text().isdigit())))
    self.combobox.lineEdit().textChanged.connect(
        lambda: set_combo_error_style(self.combobox,
                len(self.combobox.currentText().strip()) == 0))
    self.enter_key.textChanged.connect(
        lambda: set_edit_error_style(self.enter_key, len(self.enter_key.text()) == 0))
    self.scope.lineEdit().textChanged.connect(
        lambda: set_combo_error_style(self.scope,
                len(self.scope.currentText().strip()) == 0))
    self.input_fio_user.textChanged.connect(
        lambda: set_edit_error_style(self.input_fio_user, len(self.input_fio_user.text()) <= 3))
    self.input_apm.textChanged.connect(
        lambda: set_edit_error_style(self.input_apm, len(self.input_apm.text()) <= 3))
    self.user.textChanged.connect(
        lambda: set_edit_error_style(self.user, len(self.user.text()) <= 3))

    return frame


# ╔═══════════════════════════════════════════════════════════════════╗
# ║   Т А Б Л И Ц А   +   П О И С К                                   ║
# ╚═══════════════════════════════════════════════════════════════════╝
def create_data_table(self) -> QFrame:
    frame = QFrame()
    frame.setStyleSheet("border:1px solid #d0d0d0;border-radius:8px;")
    lay = QVBoxLayout(frame); lay.setContentsMargins(12, 12, 12, 12)

    self.search_line = QLineEdit(placeholderText="Введите текст для поиска…")
    lay.addWidget(self.search_line)

    self.table_widget = QTableWidget()
    self.table_widget.setColumnCount(12)
    self.table_widget.setHorizontalHeaderLabels([
        "ID","Номер","ПО","№ лицензии","Область",
        "ФИО","APM","Дата","ФИО IT","Статус","Отметка","Дата док-та"
    ])
    self.table_widget.verticalHeader().setVisible(False)
    self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    lay.addWidget(self.table_widget)

    self.search_line.textChanged.connect(lambda: load_data(self))
    load_data(self)               # первичная загрузка
    return frame


# ╔═══════════════════════════════════════════════════════════════════╗
# ║   З А Г Р У З К А   Д А Н Н Ы Х                                   ║
# ╚═══════════════════════════════════════════════════════════════════╝
def load_data(self):
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
                WHERE CAST(number AS CHAR) LIKE %s
                   OR name_of_soft LIKE %s
                   OR fullname      LIKE %s
                ORDER BY ID DESC LIMIT 50
            """, (patt, patt, patt))
        else:
            cur.execute("SELECT * FROM License ORDER BY ID DESC LIMIT 500")

        rows = cur.fetchall()
        con.close()

        self.table_widget.setRowCount(len(rows))

        for r, row in enumerate(rows):
            columns = [
                row.get("ID"),          row.get("number"),
                row.get("name_of_soft"),row.get("number_lic"),
                row.get("scop_using"),  row.get("fullname"),
                row.get("name_apm"),    row.get("date"),
                row.get("fullname_it"), row.get("status"),
                row.get("input_mark"),  row.get("input_date")
            ]
            for c, val in enumerate(columns):
                if c >= self.table_widget.columnCount():
                    break
                item = QTableWidgetItem(str(val) if val is not None else "")
                self.table_widget.setItem(r, c, item)

            # ← здесь строка уже создана — безопасно задаём высоту
            self.table_widget.setRowHeight(r, 40)

    except Exception as e:
        print("Ошибка загрузки данных:", e)


# ╔═══════════════════════════════════════════════════════════════════╗
# ║   С О Х Р А Н Е Н И Е   В   Б Д                                   ║
# ╚═══════════════════════════════════════════════════════════════════╝
def save_values6(self):
    # — проверки (оставлены прежними) —
    errors = []

    if not (self.enter_number.text().isdigit()):
        errors.append("Поле «Номер» должно содержать цифры")
    if not self.combobox.currentText().strip():
        errors.append("Не выбрано ПО СКЗИ")
    if not self.enter_key.text().strip():
        errors.append("Поле «Ключ» пустое")
    if not self.scope.currentText().strip():
        errors.append("Не заполнена «Область применения»")
    if len(self.input_fio_user.text()) <= 3:
        errors.append("ФИО пользователя слишком короткое")
    if len(self.input_apm.text()) <= 3:
        errors.append("Имя APM/IP слишком короткое")
    if len(self.user.text()) <= 3:
        errors.append("ФИО сотрудника ИБ слишком короткое")
    if not (self.rb_issued.isChecked() or self.rb_installed.isChecked() or self.rb_taken.isChecked()):
        errors.append("Не выбран статус")

    if errors:
        QMessageBox.critical(self, "Ошибка заполнения",
                             "Обнаружены ошибки:\n\n• " + "\n• ".join(errors))
        return

    # статус / отметка
    if self.rb_issued.isChecked():
        status, mark = 1, ""
    elif self.rb_installed.isChecked():
        status, mark = 2, ""
    else:
        status, mark = 3, "True"

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
            SELECT name_of_soft, scop_using
            FROM License
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