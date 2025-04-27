# ui/page9.py
from PyQt6.QtCore   import Qt, QDate, QTimer
from PyQt6.QtGui    import QFontDatabase, QShortcut, QKeySequence, QColor
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QLabel, QScrollArea, QFrame, QGraphicsDropShadowEffect, QDateEdit, QSizePolicy, QPushButton, QComboBox, QLineEdit,
    QTableWidget, QHeaderView, QTableWidgetItem, QStyleOptionViewItem, QStyledItemDelegate
)

from ui.page1 import load_gilroy, BG, ACCENT, TXT_DARK, CARD_R, PAD_H, PAD_V, BTN_R, BTN_H
from logic.db import enter_CBR
import pymysql                         # для load_data9

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

def _combo(ph: str, items: list[str], font=None) -> QComboBox:
    cb = QComboBox(); cb.addItems(items); cb.setCurrentIndex(-1); cb.setEditable(True)
    cb.lineEdit().setPlaceholderText(ph); cb.setFixedHeight(34)
    cb.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    if font: cb.setFont(font); cb.lineEdit().setFont(font)
    cb.setStyleSheet(f"""
        QComboBox {{
            background:#fff; border:1px solid #88959e; border-radius:6px;
            padding:2px 32px 2px 8px; color:{TXT_DARK};
        }}
        QComboBox:focus{{ border:1px solid {ACCENT}; }}
        QComboBox QLineEdit {{ border:none; padding:0; }}
        QComboBox QLineEdit::placeholder{{ color:{ACCENT}; }}
        QComboBox::drop-down{{ subcontrol-origin:padding; subcontrol-position:top right;
                               width:26px; border:none; background:transparent; 
                               border-left:1px solid #88959e; }}
        QComboBox::down-arrow{{ image:url(icons/chevron_down.svg); width:10px;height:6px;
                                margin-right:8px; }}
        QComboBox::down-arrow:on{{ image:url(icons/chevron_up.svg); }}
        QComboBox QAbstractItemView {{
            border:1px solid #88959e; outline:0;
            selection-background-color:rgba(139,197,64,.18);
        }}
    """); return cb

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
            image:url(icons/chevron_down.svg);
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
    btn_save.setFixedWidth(1280)
    btn_save.clicked.connect(lambda: save_value9(self))
    cbox.addSpacing(5); cbox.addWidget(btn_save,0,Qt.AlignmentFlag.AlignHCenter); cbox.addSpacing(5)

    # ── таблица + поиск
    tbl_frame = create_data_table9(self)
    tbl_frame.setStyleSheet("background:#fff;border:1px solid #d0d0d0;border-radius:8px;")
    tbl_frame.setMinimumHeight(200)
    cbox.addWidget(tbl_frame)

    # таймер обновления
    self.refresh_timer = QTimer(page); self.refresh_timer.setInterval(60000)
    self.refresh_timer.timeout.connect(lambda: load_data9(self)); self.refresh_timer.start()

    # Enter → сохранить
    QShortcut(QKeySequence("Return"), page).activated.connect(lambda: save_value9(self))

    fill_recent_values9(self)

    return page

def create_data_table9(self) -> QWidget:
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setSpacing(5)

    # Поисковая строка (без изменений)
    search_layout = QHBoxLayout()
    search_label = QLabel("Поиск:")
    self.search_line9 = QLineEdit()
    self.search_line9.setPlaceholderText("Введите текст для поиска...")
    search_layout.addWidget(search_label)
    search_layout.addWidget(self.search_line9)
    layout.addLayout(search_layout)

    # Таблица
    self.table_widget9 = QTableWidget()
    headers = [
        "ID", "Заявка", "Статус", "Серийный номер", "Номер ключа",
        "УЦ", "Область/ЭДО", "Владелец", "Дата начала", "Дата окончания",
        "Дополнительно", "Примечание"
    ]
    self.table_widget9.setColumnCount(len(headers))
    self.table_widget9.setHorizontalHeaderLabels(headers)

    # Перенос текста и убираем «...»
    self.table_widget9.setWordWrap(True)
    self.table_widget9.setTextElideMode(Qt.TextElideMode.ElideNone)

    # Делегат для WrapText
    class WrapDelegate(QStyledItemDelegate):
        def initStyleOption(self, option, index):
            super().initStyleOption(option, index)
            option.features |= QStyleOptionViewItem.ViewItemFeature.WrapText

    self.table_widget9.setItemDelegate(WrapDelegate(self.table_widget9))

    # Растягиваем колонки и авто-подгонка высоты строк
    hdr = self.table_widget9.horizontalHeader()
    hdr.setStretchLastSection(True)
    hdr.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    self.table_widget9.verticalHeader().setSectionResizeMode(
        QHeaderView.ResizeMode.ResizeToContents
    )

    layout.addWidget(self.table_widget9)

    # Подключаем загрузку
    self.search_line9.textChanged.connect(lambda: load_data9(self))
    load_data9(self)

    return widget

def load_data9(self):
    """
    Загружает из базы данных записи из таблицы CBR.
    При наличии текста в поиске — фильтрация по всем столбцам.
    """
    search_text = self.search_line9.text().strip()
    try:
        con = pymysql.connect(
            host="localhost", port=3306, user="newuser", password="852456qaz",
            database="IB", charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor
        )
        cur = con.cursor()
        if search_text:
            patt = f"%{search_text}%"
            cur.execute("""
                SELECT * FROM CBR
                WHERE CAST(ID             AS CHAR) LIKE %s
                   OR number              LIKE %s
                   OR status              LIKE %s
                   OR number_serial       LIKE %s
                   OR number_key          LIKE %s
                   OR owner               LIKE %s
                   OR scope_using         LIKE %s
                   OR fullname_owner      LIKE %s
                   OR CAST(date_start     AS CHAR) LIKE %s
                   OR CAST(date_end       AS CHAR) LIKE %s
                   OR additional          LIKE %s
                   OR note                LIKE %s
                ORDER BY ID DESC
                LIMIT 500
            """, (patt,) * 12)
        else:
            cur.execute("SELECT * FROM CBR ORDER BY ID DESC LIMIT 500")

        rows = cur.fetchall()
        con.close()

        self.table_widget9.setRowCount(len(rows))
        for r, row in enumerate(rows):
            cols = [
                row.get("ID"),
                row.get("number"),
                row.get("status"),
                row.get("number_serial"),
                row.get("number_key"),
                row.get("owner"),
                row.get("scope_using"),
                row.get("fullname_owner"),
                row.get("date_start"),
                row.get("date_end"),
                row.get("additional"),
                row.get("note"),
            ]
            for c, val in enumerate(cols):
                self.table_widget9.setItem(r, c, QTableWidgetItem(str(val) if val is not None else ""))

        self.table_widget9.resizeRowsToContents()

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