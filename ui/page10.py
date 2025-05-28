# ui/page10.py
from datetime import datetime

from PyQt6 import QtWidgets
from PyQt6.QtCore   import Qt, QDate, QTimer
from PyQt6.QtGui    import QFontDatabase, QShortcut, QKeySequence, QColor
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout,
    QLabel, QPushButton, QLineEdit, QComboBox, QDateEdit, QFrame,
    QGraphicsDropShadowEffect, QSizePolicy, QScrollArea, QTableWidget, QHeaderView, QTableWidgetItem,
    QStyleOptionViewItem, QStyledItemDelegate
)

from ui.page1 import load_gilroy, BG, ACCENT, TXT_DARK, CARD_R, PAD_H, PAD_V, BTN_R, BTN_H
from logic.db import enter_TLS
import pymysql               # для load_data10
from ui.page7 import (          # берём фабрики/стили из «красивой» 7-й страницы
   _combo
)

TLS_FIELDS = {
    0:  "ID",
    1:  "number",        # Заявка
    2:  "date",          # Дата
    3:  "environment",   # Среда
    4:  "access",        # Доступ
    5:  "issuer",        # УЦ
    6:  "initiator",     # Инициатор
    7:  "owner",         # Владелец АС
    8:  "algorithm",     # Алгоритм
    9:  "scope",         # Область/ЭДО
    10: "DNS",
    11: "resolution",    # Резолюция ИБ
    12: "note",          # Примечание
}

def _flash_row10(tbl: QTableWidget, row: int, msec: int = 400):
    tbl.blockSignals(True)
    for c in range(tbl.columnCount()):
        it = tbl.item(row, c)
        if it:
            it.setBackground(QColor(139, 197, 64, 40))
    tbl.blockSignals(False)

    def _clr():
        tbl.blockSignals(True)
        for c in range(tbl.columnCount()):
            it = tbl.item(row, c)
            if it:
                it.setBackground(QColor(0, 0, 0, 0))
        tbl.blockSignals(False)
    QTimer.singleShot(msec, _clr)


def _rollback_tls(item: QTableWidgetItem, original: str, err) -> None:
    if original is None:
        original = ""
    tbl = item.tableWidget()
    tbl.blockSignals(True)
    item.setText(original)                    # визуальный откат
    tbl.blockSignals(False)
    QtWidgets.QMessageBox.critical(tbl, "Ошибка сохранения", str(err))

# ───── маленькие фабрики ──────────────────────────────────────────────
def _hline(color=ACCENT, h=2):
    ln = QFrame(); ln.setFixedHeight(h)
    ln.setStyleSheet(f"background:{color};border:none;")
    return ln

def _vline(color="#d0d0d0", w=1):
    ln = QFrame(); ln.setFixedWidth(w)
    ln.setFrameShape(QFrame.Shape.VLine)
    ln.setStyleSheet(f"background:{color};border:none;")
    return ln

def _edit(ph: str, font=None) -> QLineEdit:
    e = QLineEdit(); e.setPlaceholderText(ph); e.setFixedHeight(34)
    e.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    if font: e.setFont(font)
    e.setStyleSheet(f"""
        QLineEdit {{
            background:#fff; border:1px solid #88959e; border-radius:6px;
            padding:4px 8px; color:{TXT_DARK};
        }}
        QLineEdit:focus{{ border:1px solid {ACCENT}; }}
        QLineEdit::placeholder{{ color:{ACCENT}; }}
    """); return e


def _btn(text:str, h=BTN_H):
    b = QPushButton(text); b.setCursor(Qt.CursorShape.PointingHandCursor); b.setFixedHeight(h)
    b.setStyleSheet(
        f"QPushButton{{background:{BG};color:#fff;border:none;border-radius:{BTN_R}px;}}"
        f"QPushButton:hover{{background:{ACCENT};}}"
    ); return b

# ───── вверху рядом с _edit и _combo ─────────────────────────────
def _date(font=None) -> QDateEdit:
    d = QDateEdit(calendarPopup=True)
    d.setDate(QDate.currentDate())
    d.setDisplayFormat("dd.MM.yyyy")      # как на скрине
    d.setFixedHeight(34)
    d.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    if font: d.setFont(font)
    d.setStyleSheet(f"""
        QDateEdit {{
            background:#fff; border:1px solid #88959e; border-radius:6px;
            padding:2px 32px 2px 8px; color:{TXT_DARK};
        }}
        QDateEdit:focus{{ border:1px solid {ACCENT}; }}
        QDateEdit::drop-down{{
            subcontrol-origin:padding; subcontrol-position:top right;
            width:26px; border:none; background:transparent;
            border-left:1px solid #88959e;
        }}
        QDateEdit::down-arrow{{
            image:url(icons/chevron_down.png);
            width:10px; height:6px; margin-right:8px;
        }}
    """)
    return d


def on_tls_item_changed(self, item: QTableWidgetItem):
    # 1. ID не редактируем
    if item.column() == 0:
        return

    col       = item.column()
    original  = item.data(Qt.ItemDataRole.UserRole)
    new_val   = item.text().strip()
    field     = TLS_FIELDS[col]
    rec_id    = self.table_widget10.item(item.row(), 0).text()   # ID из нулевой колонки

    # ── валидация даты (колонка «Дата» = 2) ──────────────────────
    # пример валидации дат прямо здесь ─ можно расширить по своим правилам
    if item.column() == 2:  # «Начало» / «Окончание»
        try:
            for fmt in ("%d.%m.%Y", "%Y-%m-%d"):
                try:
                    new_val = datetime.strptime(new_val, fmt) \
                        .strftime("%Y-%m-%d")
                    break
                except ValueError:
                    pass
            else:
                raise ValueError("Неверный формат даты")

            # здесь можно добавить другие проверки по желанию

        except Exception as e:  # ошибка локальной проверки
            _rollback_tls(item, original, e)
            return

    # ── обновление БД по первичному ключу ID ─────────────────────
    try:
        with pymysql.connect(
                host="localhost", port=3306,
                user="newuser", password="852456qaz",
                database="IB", charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True) as con:           # autocommit чтобы лишний commit не писать
            with con.cursor() as cur:
                cur.execute(
                    f"UPDATE TLS SET `{field}`=%s WHERE ID=%s",
                    (new_val, rec_id)
                )

        # фиксация нового значения в таблице
        item.setData(Qt.ItemDataRole.UserRole, new_val)
        _flash_row10(self.table_widget10, item.row())

    except Exception as e:
        _rollback_tls(item, original, e)

# ───── главная функция страницы ───────────────────────────────────────
def create_page10(self) -> QWidget:
    fam, sty = load_gilroy()
    f_h1   = QFontDatabase.font(fam, sty, 28)
    f_h2   = QFontDatabase.font(fam, sty, 20)
    f_body = QFontDatabase.font(fam, sty, 12)

    page = QWidget(); page.setStyleSheet(f"background:{BG};")

    root = QVBoxLayout(page)
    root.setContentsMargins(16, 16, 16, 16)
    root.setSpacing(8)

    # Esc → назад
    QShortcut(QKeySequence("Escape"), page).activated.connect(self.go_to_second_page)

    # заголовок
    ttl = QLabel("TLS"); ttl.setFont(f_h1)
    ttl.setStyleSheet(f"color:#fff;border-bottom:3px solid {ACCENT};padding-bottom:4px;")
    root.addWidget(ttl, alignment=Qt.AlignmentFlag.AlignLeft)

    # ─── прокручиваемая карточка ───────────────────────────────────
    scroll = QScrollArea(); scroll.setWidgetResizable(True)
    scroll.setFrameShape(QFrame.Shape.NoFrame)
    scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    root.addWidget(scroll)

    wrapper = QWidget(); wrap_l = QVBoxLayout(wrapper); wrap_l.setContentsMargins(0,0,0,0)

    card = QFrame()
    card.setMinimumWidth(1300);
    card.setStyleSheet(f"background:#fff;border-radius:{CARD_R}px;")
    card.setGraphicsEffect(QGraphicsDropShadowEffect(
        blurRadius=32, xOffset=0, yOffset=4, color=QColor(0,0,0,55)))

    cbox = QVBoxLayout(card)
    cbox.setContentsMargins(PAD_H, PAD_V//2, PAD_H, PAD_V//2)

    wrap_l.addWidget(card); scroll.setWidget(wrapper)

    # ― Header внутри карточки
    h = QWidget(); hb = QHBoxLayout(h); hb.setContentsMargins(0,0,0,0); hb.setSpacing(12)
    back = _btn("←", 34); back.setFixedWidth(42); back.clicked.connect(self.go_to_second_page)
    hb.addWidget(back, 0, Qt.AlignmentFlag.AlignLeft)
    header_txt = QLabel("Информация по TLS"); header_txt.setFont(f_h2)
    header_txt.setStyleSheet(f"color:{TXT_DARK};")
    hb.addWidget(header_txt, 0, Qt.AlignmentFlag.AlignLeft)
    hb.addStretch(1)
    cbox.addWidget(h)

    # ― две формы в GridLayout
    g = QGridLayout(); g.setContentsMargins(12, 12, 12, 12)
    g.setHorizontalSpacing(20); g.setVerticalSpacing(8)
    cbox.addLayout(g)

    # секционные заголовки
    f_group = QFontDatabase.font(fam, sty, 14); f_group.setBold(True)
    for col, txt in enumerate(("Основные данные", "Дополнительные сведения")):
        lab = QLabel(txt); lab.setFont(f_group); lab.setStyleSheet(f"color:{TXT_DARK};")
        g.addWidget(lab, 0, col*2)
    g.addWidget(_hline(ACCENT, 1), 1, 0, 1, 3)

    FL, FR = QFormLayout(), QFormLayout()
    for F in (FL, FR):
        F.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        F.setVerticalSpacing(6); F.setHorizontalSpacing(18)
        F.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)

    g.addWidget(_vline(), 2, 1, 1, 1)
    g.addLayout(FL, 2, 0)
    g.addLayout(FR, 2, 2)
    g.setColumnStretch(0,1); g.setColumnStretch(1,0); g.setColumnStretch(2,1)

    # ― виджеты формы (лево)
    self.request_number_le = _edit("Номер заявки", f_body)
    self.dateedit1 = _date(f_body)
    self.env_cb      = _combo("Среда", ["тест", "продуктив"], f_body)
    self.access_cb   = _combo("Доступ", ["внешний", "внутренний"], f_body)
    self.issuer_cb   = _combo("УЦ", [], f_body)
    self.initiator_cb= _combo("Инициатор", [], f_body)

    FL.addRow("Заявка",   self.request_number_le)
    FL.addRow("Дата",     self.dateedit1)
    FL.addRow("Среда",    self.env_cb)
    FL.addRow("Доступ",   self.access_cb)
    FL.addRow("УЦ",       self.issuer_cb)
    FL.addRow("Инициатор", self.initiator_cb)

    # ― форма (право)
    self.owner_cb      = _combo("Владелец АС", [], f_body)
    self.algo_cb       = _combo("Алгоритм", ["RSA", "ГОСТ"], f_body)
    self.scope_cb      = _combo("ЭДО", [], f_body)
    self.dns_le        = _edit("DNS", f_body)
    self.resolution_cb = _combo("Резолюция ИБ", ["уточнение","согласовано","отказано"], f_body)
    self.note_le       = _edit("Примечание", f_body)

    FR.addRow("Владелец АС", self.owner_cb)
    FR.addRow("Алгоритм",    self.algo_cb)
    FR.addRow("ЭДО", self.scope_cb)
    FR.addRow("DNS",         self.dns_le)
    FR.addRow("Резолюция ИБ",self.resolution_cb)
    FR.addRow("Примечание",  self.note_le)

    # ― кнопка «Сохранить»
    btn_save = _btn("Сохранить", 30)
    btn_save.setFixedWidth(300)              # CARD_W – PAD*2
    btn_save.clicked.connect(lambda: save_value10(self))
    cbox.addSpacing(5); cbox.addWidget(btn_save,0,Qt.AlignmentFlag.AlignHCenter); cbox.addSpacing(5)

    # ── export-кнопки в ряд ───────────────────────────────────────────
    ex_row = QHBoxLayout()
    ex_row.setSpacing(12)
    btn_export_all = _btn("Экспорт всех данных TLS", 30)
    btn_export_all.setFixedWidth(350)
    btn_export_filtered = _btn("Экспорт отфильтрованных TLS", 30)
    btn_export_filtered.setFixedWidth(350)

    ex_row.addWidget(btn_export_all, alignment=Qt.AlignmentFlag.AlignRight)
    ex_row.addWidget(btn_export_filtered, alignment=Qt.AlignmentFlag.AlignLeft)
    cbox.addLayout(ex_row)

    btn_export_all.clicked.connect(self.export_all_TLS)
    btn_export_filtered.clicked.connect(self.export_filtered_TLS)

    # ― таблица + поиск
    tbl_frame = create_data_table10(self)
    tbl_frame.setStyleSheet("background:#fff;border:1px solid #d0d0d0;border-radius:8px;")
    tbl_frame.setMinimumHeight(200)
    cbox.addWidget(tbl_frame)


    # Enter → сохранить
    QShortcut(QKeySequence("Return"), page).activated.connect(lambda: save_value10(self))

    fill_recent_values10(self)

    return page

# ─── ПЕРЕПИСАННАЯ функция таблицы ───────────────────────────────────
def create_data_table10(self) -> QWidget:
    widget = QWidget()
    lay = QVBoxLayout(widget)
    lay.setSpacing(6)

    # ── строка поиска ──────────────────────────────────────────────
    row = QHBoxLayout()
    row.addWidget(QLabel("Поиск:"))
    self.search_line10 = QLineEdit(placeholderText="Введите текст для поиска…")
    row.addWidget(self.search_line10)
    lay.addLayout(row)

    # ── таблица ────────────────────────────────────────────────────
    self.table_widget10 = QTableWidget()

    outer_self = self  # понадобится в замыкании

    class KeysTable(QTableWidget):
        """Отдельный класс, чтобы не плодить eventFilter-ов."""

        def mouseDoubleClickEvent(tbl, ev):
            # правый ⇢ копируем строку; левый ⇢ обычное редактирование
            if ev.button() == Qt.MouseButton.RightButton:
                row = tbl.rowAt(ev.position().toPoint().y())
                if row != -1:
                    on_key_row_double_clicked(outer_self, tbl.item(row, 0))
                # «съедаем» событие, чтобы Qt не открывал редактор
                return
            super().mouseDoubleClickEvent(ev)

    def on_key_row_double_clicked(self, item: QTableWidgetItem):
        row = item.row()
        get = lambda col: self.table_widget10.item(row, col).text() if self.table_widget10.item(row, col) else ""

        self.request_number_le.setText(get(1))
        _safe_set(self.dateedit1, get(2))
        self.env_cb.lineEdit().setText(get(3))
        self.access_cb.lineEdit().setText(get(4))
        self.issuer_cb.lineEdit().setText(get(5))
        self.initiator_cb.lineEdit().setText(get(6))
        self.owner_cb.lineEdit().setText(get(7))
        self.algo_cb.lineEdit().setText(get(10))
        self.scope_cb.lineEdit().setText(get(11))
        self.dns_le.setText(get(12))
        self.resolution_cb.lineEdit().setText(get(13))
        self.note_le.setText(get(14))



    # ─── on_key_row_double_clicked ─────────────────────────────
    def _safe_set(dateedit: QDateEdit, txt: str):
        for fmt in ("yyyy-MM-dd", "dd.MM.yyyy"):
            qd = QDate.fromString(txt, fmt)
            if qd.isValid():  # ✔ только валидные даты
                dateedit.setDate(qd)
                break  # нашли – хватит

    self.table_widget10 = KeysTable()

    headers = [
        "ID", "Заявка", "Дата", "Среда", "Доступ", "УЦ",
        "Инициатор", "Владелец АС", "Алгоритм", "Область/ЭДО",
        "DNS", "Резолюция", "Примечание"
    ]
    self.table_widget10.setHorizontalHeaderLabels(headers)
    self.table_widget10.setColumnCount(len(headers))
    self.table_widget10.setHorizontalHeaderLabels(headers)
    self.table_widget10.verticalHeader().setVisible(False)

    # перенос текста без «…»
    self.table_widget10.setWordWrap(True)
    self.table_widget10.setTextElideMode(Qt.TextElideMode.ElideNone)

    class _Wrap(QStyledItemDelegate):
        def initStyleOption(self, opt, idx):
            super().initStyleOption(opt, idx)
            opt.features |= QStyleOptionViewItem.ViewItemFeature.WrapText
    self.table_widget10.setItemDelegate(_Wrap(self.table_widget10))

    hdr = self.table_widget10.horizontalHeader()
    hdr.setSectionsMovable(True)
    hdr.setStretchLastSection(True)
    hdr.setMinimumSectionSize(30)
    self.table_widget10.verticalHeader().setSectionResizeMode(
        QHeaderView.ResizeMode.ResizeToContents)

    lay.addWidget(self.table_widget10, stretch=1)

    # ── первая «тихая» загрузка (без itemChanged) ─────────────────
    load_data10(self)                         # сигналы ещё не подключены

    # ── подключаем поисковую строку и редактирование ──────────────
    self.table_widget10.itemChanged.connect(
        lambda it: on_tls_item_changed(self, it))
    self.search_line10.textChanged.connect(lambda: load_data10(self))

    return widget

def load_data10(self) -> None:
    """Загружает записи TLS в таблицу self.table_widget10."""
    search = self.search_line10.text().strip()

    # ── запрос к БД ──────────────────────────────────────────────
    with pymysql.connect(host="localhost", port=3306,
                         user="newuser", password="852456qaz",
                         database="IB", charset="utf8mb4",
                         cursorclass=pymysql.cursors.DictCursor) as con:
        cur = con.cursor()
        if search:
            patt = f"%{search}%"
            cur.execute("""
                SELECT * FROM TLS
                WHERE CONCAT_WS('|', ID, number, date, environment, access,
                                issuer, initiator, owner, algorithm, scope,
                                DNS, resolution, note) LIKE %s
                ORDER BY ID DESC LIMIT 500
            """, (patt,))
        else:
            cur.execute("SELECT * FROM TLS ORDER BY ID DESC LIMIT 500")
        rows = cur.fetchall()

    # ── тихо заполняем таблицу ──────────────────────────────────
    self.table_widget10.blockSignals(True)

    self.table_widget10.setRowCount(len(rows))
    for r, row in enumerate(rows):
        cols = [
            row.get("ID"),
            row.get("number"),
            row.get("date"),
            row.get("environment"),
            row.get("access"),
            row.get("issuer"),
            row.get("initiator"),
            row.get("owner"),
            row.get("algorithm"),
            row.get("scope"),
            row.get("DNS"),
            row.get("resolution"),
            row.get("note"),
        ]
        for c, val in enumerate(cols):
            for c, val in enumerate(cols):
                it = QTableWidgetItem("" if val is None else str(val))
                it.setData(Qt.ItemDataRole.UserRole, it.text())  # «оригинал»

                if c == 0:  # ID
                    it.setFlags(it.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table_widget10.setItem(r, c, it)
        self.table_widget10.setColumnHidden(0, True)

    self.table_widget10.resizeRowsToContents()
    self.table_widget10.blockSignals(False)

def save_value10(self):
    errors = []

    # Проверка обязательных полей (не включая «Примечание»)
    if not self.request_number_le.text().strip():
        errors.append("Поле «Заявка» не должно быть пустым.")
    if not self.env_cb.currentText():
        errors.append("Поле «Среда» не должно быть пустым.")
    if not self.access_cb.currentText():
        errors.append("Поле «Доступ» не должно быть пустым.")
    if not self.issuer_cb.currentText():
        errors.append("Поле «УЦ» не должно быть пустым.")
    if not self.initiator_cb.currentText():
        errors.append("Поле «Инициатор» не должно быть пустым.")
    if not self.owner_cb.currentText():
        errors.append("Поле «Владелец АС» не должно быть пустым.")
    if not self.algo_cb.currentText():
        errors.append("Поле «Алгоритм» не должно быть пустым.")
    if not self.scope_cb.currentText():
        errors.append("Поле «Область/ЭДО» не должно быть пустым.")
    if not self.dns_le.text().strip():
        errors.append("Поле «DNS» не должно быть пустым.")
    if not self.resolution_cb.currentText():
        errors.append("Поле «Резолюция ИБ» не должно быть пустым.")

    if errors:
        from PyQt6 import QtWidgets
        QtWidgets.QMessageBox.critical(
            self,
            "Ошибка заполнения",
            "Обнаружены ошибки:\n\n• " + "\n• ".join(errors)
        )
        return

    # Сбор значений
    request_number  = self.request_number_le.text().strip()
    date_str        = self.dateedit1.date().toPyDate().strftime('%Y-%m-%d')
    env             = self.env_cb.currentText()
    access          = self.access_cb.currentText()
    issuer          = self.issuer_cb.currentText()
    initiator       = self.initiator_cb.currentText()
    owner           = self.owner_cb.currentText()
    algo            = self.algo_cb.currentText()
    scope           = self.scope_cb.currentText()
    dns             = self.dns_le.text().strip()
    resolution      = self.resolution_cb.currentText()
    note            = self.note_le.text().strip()

    # Сохранение в базу
    enter_TLS(
        request_number,
        date_str,
        env,
        access,
        issuer,
        initiator,
        owner,
        algo,
        scope,
        dns,
        resolution,
        note
    )

    # Очистка и обновление
    clear_fields(self)
    fill_recent_values10(self)
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


def fill_recent_values10(self, limit: int = 5) -> None:
    """
    Берёт последние `limit` строк из таблицы TLS и
    добавляет уникальные значения в выпадающие списки:
        • self.env_cb
        • self.access_cb
        • self.issuer_cb
        • self.initiator_cb
        • self.owner_cb
        • self.algo_cb
        • self.scope_cb
        • self.resolution_cb
    Без дубликатов, новые вставляются в начало списка.
    """
    try:
        con = pymysql.connect(
            host="localhost", port=3306,
            user="newuser", password="852456qaz",
            database="IB", charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )
        cur = con.cursor()
        cur.execute("""
            SELECT environment, access, issuer, initiator,
                   owner, algorithm, scope, resolution
            FROM TLS
            ORDER BY ID DESC
            LIMIT %s
        """, (limit,))
        rows = cur.fetchall()
        con.close()

        # уникальные множества
        envs = {r["environment"] for r in rows if r["environment"]}
        accs = {r["access"]      for r in rows if r["access"]}
        issu = {r["issuer"]      for r in rows if r["issuer"]}
        inits= {r["initiator"]   for r in rows if r["initiator"]}
        owns = {r["owner"]       for r in rows if r["owner"]}
        algs = {r["algorithm"]   for r in rows if r["algorithm"]}
        scps = {r["scope"]       for r in rows if r["scope"]}
        reso = {r["resolution"]  for r in rows if r["resolution"]}

        def _sync(cb: QComboBox, vals: set[str]):
            if not vals:
                return
            old = {cb.itemText(i) for i in range(cb.count())}
            new = [v for v in vals if v not in old]
            if new:
                had = cb.currentIndex() != -1
                cb.insertItems(0, new)
                if not had:
                    cb.setCurrentIndex(-1)
                    cb.clearEditText()

        _sync(self.env_cb,      envs)
        _sync(self.access_cb,   accs)
        _sync(self.issuer_cb,   issu)
        _sync(self.initiator_cb,inits)
        _sync(self.owner_cb,    owns)
        _sync(self.algo_cb,     algs)
        _sync(self.scope_cb,    scps)
        _sync(self.resolution_cb,reso)

    except Exception as e:
        print("fill_recent_values10 error:", e)