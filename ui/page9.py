# ui/page9.py
from datetime import datetime

from PyQt6.QtCore   import Qt, QDate, QTimer
from PyQt6.QtGui    import QFontDatabase, QShortcut, QKeySequence, QColor
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QLabel, QScrollArea, QFrame, QGraphicsDropShadowEffect, QDateEdit, QSizePolicy, QPushButton, QComboBox, QLineEdit,
    QTableWidget, QHeaderView, QTableWidgetItem, QStyleOptionViewItem, QStyledItemDelegate
)
from PyQt6.uic.Compiler.qtproxies import QtWidgets

from ui.page1 import load_gilroy, BG, ACCENT, TXT_DARK, CARD_R, PAD_H, PAD_V, BTN_R, BTN_H
from logic.db import enter_CBR
import pymysql                         # для load_data9
from ui.page7 import (          # берём фабрики/стили из «красивой» 7-й страницы
    _combo
)

CBR_FIELDS = {
     0: "ID",
     1: "number",          # заявка
     2: "status",
     3: "number_serial",
     4: "number_key",
     5: "owner",           # УЦ
     6: "scope_using",
     7: "fullname_owner",
     8: "date_start",
     9: "date_end",
    10: "additional",
    11: "note",
}


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


def create_page9(self) -> QWidget:
    fam, sty = load_gilroy()
    f_h1   = QFontDatabase.font(fam, sty, 28)
    f_h2   = QFontDatabase.font(fam, sty, 20)
    f_body = QFontDatabase.font(fam, sty, 12)

    page = QWidget(); page.setStyleSheet(f"background:{BG};")
    root = QVBoxLayout(page)
    root.setContentsMargins(16,16,16,16); root.setSpacing(8)

    # Esc → назад
    QShortcut(QKeySequence("Escape"), page).activated.connect(self.go_to_second_page)

    # ── заголовок
    ttl = QLabel("КБР"); ttl.setFont(f_h1)
    ttl.setStyleSheet(f"color:#fff;border-bottom:3px solid {ACCENT};padding-bottom:4px;")
    root.addWidget(ttl, alignment=Qt.AlignmentFlag.AlignLeft)

    # ── скролл + карточка ─────────────────────────────────────────
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
    cbox = QVBoxLayout(card); cbox.setContentsMargins(PAD_H, PAD_V//2, PAD_H, PAD_V//2)

    wrap_l.addWidget(card); scroll.setWidget(wrapper)

    # ── Header внутри карточки
    hdr = QWidget(); hb = QHBoxLayout(hdr); hb.setContentsMargins(0,0,0,0); hb.setSpacing(12)
    back = _btn("←", 34); back.setFixedWidth(42); back.clicked.connect(self.go_to_second_page)
    hb.addWidget(back, 0, Qt.AlignmentFlag.AlignLeft)
    htxt = QLabel("Информация по КБР"); htxt.setFont(f_h2); htxt.setStyleSheet(f"color:{TXT_DARK};")
    hb.addWidget(htxt, 0, Qt.AlignmentFlag.AlignLeft); hb.addStretch(1)
    cbox.addWidget(hdr)

    # ── две формы в GridLayout ───────────────────────────────────
    g = QGridLayout(); g.setContentsMargins(12,12,12,12)
    g.setHorizontalSpacing(20); g.setVerticalSpacing(8)
    cbox.addLayout(g)

    f_group = QFontDatabase.font(fam, sty, 14); f_group.setBold(True)
    for col, txt in enumerate(("Основные данные", "Дополнительные сведения")):
        lab = QLabel(txt); lab.setFont(f_group); lab.setStyleSheet(f"color:{TXT_DARK};")
        g.addWidget(lab, 0, col*2)
    g.addWidget(_hline(ACCENT,1), 1, 0, 1, 3)

    FL, FR = QFormLayout(), QFormLayout()
    for F in (FL, FR):
        F.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        F.setVerticalSpacing(6); F.setHorizontalSpacing(18)
        F.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)

    g.addWidget(_vline(), 2, 1, 1, 1)
    g.addLayout(FL, 2, 0); g.addLayout(FR, 2, 2)
    g.setColumnStretch(0,1); g.setColumnStretch(2,1)

    # ── левая форма ──────────────────────────────────────────────
    self.request_le         = _edit("Номер обращения", f_body)
    self.nositel_cb         = _combo("Тип носителя? (Да/Нет)", ["Да","Нет"], f_body)
    self.nositel_serial_cb  = _combo("Носитель (серийный)", [], f_body)
    self.key_number_le      = _edit("Номер ключа", f_body)
    self.issuer_cb_cbr      = _combo("УЦ", [], f_body)

    FL.addRow("Обращение",       self.request_le)
    FL.addRow("Тип носителя",    self.nositel_cb)
    FL.addRow("Серийный номер",  self.nositel_serial_cb)
    FL.addRow("Номер ключа",     self.key_number_le)
    FL.addRow("УЦ",              self.issuer_cb_cbr)

    # ── правая форма ─────────────────────────────────────────────
    self.scope_cb_cbr   = _combo("Область/ЭДО", [], f_body)
    self.owner_cb_cbr   = _combo("Владелец", [], f_body)
    self.dateedit1      = _date(f_body)
    self.dateedit2      = _date(f_body)
    self.additional1_le = _edit("Дополнительно", f_body)
    self.additional2_le = _edit("Дополнительно", f_body)

    FR.addRow("Область/ЭДО", self.scope_cb_cbr)
    FR.addRow("Владелец",    self.owner_cb_cbr)
    FR.addRow("Дата 1",      self.dateedit1)
    FR.addRow("Дата 2",      self.dateedit2)
    FR.addRow("Дополнительно", self.additional1_le)
    FR.addRow("Дополнительно", self.additional2_le)

    # ── кнопка «Сохранить»
    btn_save = _btn("Сохранить", 30)
    btn_save.setFixedWidth(300)
    btn_save.clicked.connect(lambda: save_value9(self))
    cbox.addSpacing(5); cbox.addWidget(btn_save,0,Qt.AlignmentFlag.AlignHCenter); cbox.addSpacing(5)

    # ── export-кнопки в ряд ───────────────────────────────────────────
    ex_row = QHBoxLayout()
    ex_row.setSpacing(12)
    btn_export_all = _btn("Экспорт всех данных КБР", 30)
    btn_export_all.setFixedWidth(350)
    btn_export_filtered = _btn("Экспорт отфильтрованных КБР", 30)
    btn_export_filtered.setFixedWidth(350)

    ex_row.addWidget(btn_export_all, alignment=Qt.AlignmentFlag.AlignRight)
    ex_row.addWidget(btn_export_filtered, alignment=Qt.AlignmentFlag.AlignLeft)
    cbox.addLayout(ex_row)

    btn_export_all.clicked.connect(self.export_all_CBR)
    btn_export_filtered.clicked.connect(self.export_filtered_CBR)

    # ── таблица + поиск
    tbl_frame = create_data_table9(self)
    tbl_frame.setStyleSheet("background:#fff;border:1px solid #d0d0d0;border-radius:8px;")
    tbl_frame.setMinimumHeight(200)
    cbox.addWidget(tbl_frame)


    # Enter → сохранить
    QShortcut(QKeySequence("Return"), page).activated.connect(lambda: save_value9(self))

    fill_recent_values9(self)

    return page

def create_data_table9(self) -> QWidget:
    """
    Поисковая строка + таблица CBR.
    1) создаём виджеты;
    2) полностью настраиваем таблицу;
    3) «тихо» загружаем данные (сигналы ещё не подключены);
    4) подключаем itemChanged и поиск.
    """
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setSpacing(6)

    # ── строка поиска ──────────────────────────────────────────────
    search_row = QHBoxLayout()
    search_row.addWidget(QLabel("Поиск:"))
    self.search_line9 = QLineEdit(placeholderText="Введите текст для поиска…")
    search_row.addWidget(self.search_line9)
    layout.addLayout(search_row)

    # ── таблица ────────────────────────────────────────────────────
    self.table_widget9 = QTableWidget()                      # ① СОЗДАЁМ

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
        get = lambda col: self.table_widget9.item(row, col).text() if self.table_widget9.item(row, col) else ""

        self.request_le.setText(get(1))
        self.nositel_cb.lineEdit().setText(get(2))
        self.nositel_serial_cb.lineEdit().setText(get(3))
        self.key_number_le.setText(get(4))
        self.issuer_cb.lineEdit().setText(get(5))
        self.scope_cb.lineEdit().setText(get(6))
        self.owner_cb.lineEdit().setText(get(7))
        # ─── дата начала ─────────────────────────────────────────
        _safe_set(self.dateedit1, get(8))
        _safe_set(self.dateedit2, get(9))  # конец
        self.additional_cb_key.lineEdit().setText(get(10))
        self.additional1_le.setText(get(11))
        self.additional2_le.setText(get(12))

    # ─── on_key_row_double_clicked ─────────────────────────────
    def _safe_set(dateedit: QDateEdit, txt: str):
        for fmt in ("yyyy-MM-dd", "dd.MM.yyyy"):
            qd = QDate.fromString(txt, fmt)
            if qd.isValid():  # ✔ только валидные даты
                dateedit.setDate(qd)
                break  # нашли – хватит

    self.table_widget9 = KeysTable()
    headers = [
        "ID", "Заявка", "Статус", "Серийный номер", "Номер ключа",
        "УЦ", "Область/ЭДО", "Владелец", "Дата начала", "Дата окончания",
        "Дополнительно", "Примечание"
    ]
    self.table_widget9.setColumnCount(len(headers))
    self.table_widget9.setHorizontalHeaderLabels(headers)
    self.table_widget9.verticalHeader().setVisible(False)
    self.table_widget9.setSizePolicy(QSizePolicy.Policy.Expanding,
                                     QSizePolicy.Policy.Expanding)

    # перенос текста без «…»
    self.table_widget9.setWordWrap(True)
    self.table_widget9.setTextElideMode(Qt.TextElideMode.ElideNone)

    class _Wrap(QStyledItemDelegate):                         # делегат wrap
        def initStyleOption(self, opt, idx):
            super().initStyleOption(opt, idx)
            opt.features |= QStyleOptionViewItem.ViewItemFeature.WrapText
    self.table_widget9.setItemDelegate(_Wrap(self.table_widget9))

    # заголовок
    hdr = self.table_widget9.horizontalHeader()
    hdr.setSectionsMovable(True)
    hdr.setStretchLastSection(True)
    hdr.setMinimumSectionSize(30)
    self.table_widget9.verticalHeader().setSectionResizeMode(
        QHeaderView.ResizeMode.ResizeToContents)

    layout.addWidget(self.table_widget9, stretch=1)

    # ── «тихая» первая загрузка ─────────────────────────────────── ②
    load_data9(self)                                          # сигнала ещё НЕТ

    # ── подключаем обработчики ──────────────────────────────────── ③
    self.table_widget9.itemChanged.connect(
        lambda it: on_cbr_item_changed(self, it))
    self.search_line9.textChanged.connect(lambda: load_data9(self))

    return widget


def load_data9(self):
    search_text = self.search_line9.text().strip()

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
                SELECT * FROM CBR
                WHERE CONCAT_WS('|',
                        ID, number, status, number_serial, number_key,
                        owner, scope_using, fullname_owner,
                        date_start, date_end, additional, note
                ) LIKE %s
                ORDER BY ID DESC LIMIT 500
            """, (patt,))
        else:
            cur.execute("SELECT * FROM CBR ORDER BY ID DESC LIMIT 500")

        rows = cur.fetchall()

    finally:
        con.close()

    # ─── заливаем данные без срабатывания itemChanged ───
    self.table_widget9.blockSignals(True)

    self.table_widget9.setRowCount(len(rows))
    for r, row in enumerate(rows):
        for c, field in CBR_FIELDS.items():
            val = row.get(field)
            it  = QTableWidgetItem("" if val is None else str(val))

            it.setData(Qt.ItemDataRole.UserRole, it.text())     # «оригинал»
            if c == 0:
                it.setFlags(it.flags() & ~Qt.ItemFlag.ItemIsEditable)
            it.setTextAlignment(Qt.AlignmentFlag.AlignLeft |
                                Qt.AlignmentFlag.AlignVCenter)
            self.table_widget9.setItem(r, c, it)

    self.table_widget9.resizeRowsToContents()
    self.table_widget9.blockSignals(False)

def _flash_row9(tbl: QTableWidget, row: int, msec: int = 400):
    tbl.blockSignals(True)
    for c in range(tbl.columnCount()):
        cell = tbl.item(row, c)
        if cell:
            cell.setBackground(QColor(139, 197, 64, 40))
    tbl.blockSignals(False)

    def _clear():
        tbl.blockSignals(True)
        for c in range(tbl.columnCount()):
            cell = tbl.item(row, c)
            if cell:
                cell.setBackground(QColor(0, 0, 0, 0))
        tbl.blockSignals(False)
    QTimer.singleShot(msec, _clear)


def on_cbr_item_changed(self, item: QTableWidgetItem):
    if item.column() == 0:              # ID не редактируем
        return

    original = item.data(Qt.ItemDataRole.UserRole)
    new_val  = item.text().strip()
    col      = item.column()

    # пример валидации дат прямо здесь ─ можно расширить по своим правилам
    if item.column() in (8, 9):  # «Начало» / «Окончание»
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
            _rollback_cbr(item, original, e)
            return

    field  = CBR_FIELDS[col]
    rec_id = self.table_widget9.item(item.row(), 0).text()

    # ── запись в БД ──
    try:
        with pymysql.connect(host="localhost", port=3306,
                             user="newuser", password="852456qaz",
                             database="IB", charset="utf8mb4",
                             cursorclass=pymysql.cursors.DictCursor) as con:
            cur = con.cursor()
            cur.execute(f"UPDATE CBR SET `{field}`=%s WHERE ID=%s",
                        (new_val, rec_id))
            con.commit()

        item.setData(Qt.ItemDataRole.UserRole, new_val)  # зафиксировали
        _flash_row9(self.table_widget9, item.row())

    except Exception as e:
        _rollback_cbr(item, original, e)

def _rollback_cbr(item: QTableWidgetItem, original: str, err) -> None:
    tbl = item.tableWidget()
    tbl.blockSignals(True)
    item.setText(original)                        # визуальный откат
    tbl.blockSignals(False)
    QtWidgets.QMessageBox.critical(tbl, "Ошибка сохранения", str(err))

def save_value9(self):
    errors = []

    # Проверка обязательных полей (не включая «Дополнительно»)
    if not self.request_le.text().strip():
        errors.append("Поле «Обращение» не должно быть пустым.")
    if not self.nositel_cb.currentText():
        errors.append("Поле «Тип носителя» не должно быть пустым.")
    if not self.nositel_serial_cb.currentText():
        errors.append("Поле «Носитель (серийный)» не должно быть пустым.")
    if not self.key_number_le.text().strip():
        errors.append("Поле «Номер ключа» не должно быть пустым.")
    if not self.issuer_cb_cbr.currentText():
        errors.append("Поле «УЦ» не должно быть пустым.")
    if not self.scope_cb_cbr.currentText():
        errors.append("Поле «Область/ЭДО» не должно быть пустым.")
    if not self.owner_cb_cbr.currentText():
        errors.append("Поле «Владелец» не должно быть пустым.")

    if errors:
        QtWidgets.QMessageBox.critical(
            self,
            "Ошибка заполнения",
            "Обнаружены ошибки:\n\n• " + "\n• ".join(errors)
        )
        return

    # Сбор значений для сохранения
    request_le         = self.request_le.text().strip()
    nositel_cb         = self.nositel_cb.currentText()
    nositel_serial_cb  = self.nositel_serial_cb.currentText()
    key_number_le      = self.key_number_le.text().strip()
    issuer_cb          = self.issuer_cb_cbr.currentText()
    scope_cb           = self.scope_cb_cbr.currentText()
    owner_cb           = self.owner_cb_cbr.currentText()
    date_start_str     = self.dateedit1.date().toPyDate().strftime('%Y-%m-%d')
    date_end_str       = self.dateedit2.date().toPyDate().strftime('%Y-%m-%d')
    additional1_le     = self.additional1_le.text().strip()
    additional2_le     = self.additional2_le.text().strip()

    # Вызов функции записи в БД
    enter_CBR(
        request_le,
        nositel_cb,
        nositel_serial_cb,
        key_number_le,
        issuer_cb,
        scope_cb,
        owner_cb,
        date_start_str,
        date_end_str,
        additional1_le,
        additional2_le
    )

    # Сброс полей и обновление данных на странице
    clear_fields(self)
    fill_recent_values9(self)
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


def fill_recent_values9(self, limit: int = 5) -> None:
    """
    Заполняет динамические QComboBox-ы уникальными значениями
    из последних `limit` записей таблицы CBR:
        • self.nositel_serial_cb  – «Носитель (серийный)»
        • self.issuer_cb_cbr      – «УЦ»
        • self.scope_cb_cbr       – «Область/ЭДО»
        • self.owner_cb_cbr       – «Владелец» (ФИО)
    Пропускает пустые и дубли.
    """
    try:
        con = pymysql.connect(
            host="localhost", port=3306, user="newuser", password="852456qaz",
            database="IB", charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )
        cur = con.cursor()
        cur.execute("""
            SELECT number_serial, owner, scope_using, fullname_owner
            FROM CBR
            ORDER BY ID DESC
            LIMIT %s
        """, (limit,))
        rows = cur.fetchall()
        con.close()

        # вспомогательная: оставить только первые вхождения непустых значений
        def unique(seq):
            seen = set()
            out = []
            for v in seq:
                if v and v not in seen:
                    seen.add(v)
                    out.append(v)
            return out

        serials    = unique(r["number_serial"]  for r in rows)
        ucs        = unique(r["owner"]          for r in rows)
        scopes     = unique(r["scope_using"]    for r in rows)
        fullnames  = unique(r["fullname_owner"] for r in rows)

        def _sync(cb: QComboBox, values: list[str]):
            """Вставить в cb новые values в начало, не трогая текущее вводимое."""
            if not values:
                return
            existing = {cb.itemText(i) for i in range(cb.count())}
            to_add = [v for v in values if v not in existing]
            if not to_add:
                return
            had_sel = cb.currentIndex() != -1
            cb.insertItems(0, to_add)
            if not had_sel:
                cb.setCurrentIndex(-1)
                cb.clearEditText()

        _sync(self.nositel_serial_cb, serials)
        _sync(self.issuer_cb_cbr,     ucs)
        _sync(self.scope_cb_cbr,      scopes)
        _sync(self.owner_cb_cbr,      fullnames)

    except Exception as e:
        print("fill_recent_values9 error:", e)