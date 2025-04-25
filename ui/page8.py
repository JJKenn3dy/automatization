from datetime import datetime
from PyQt6 import QtWidgets
from PyQt6.QtGui import QShortcut, QKeySequence, QPalette, QColor
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout,
    QComboBox, QSizePolicy, QGroupBox, QFormLayout, QTableWidget, QTableWidgetItem, QHeaderView, QDateEdit
)
from PyQt6.QtCore import Qt, QDate, QTimer

from logic.db import enter_keys

# ui/page8.py
from PyQt6.QtCore   import Qt, QDate, QTimer
from PyQt6.QtGui    import QFontDatabase, QKeySequence, QShortcut, QColor
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QLabel, QScrollArea, QFrame, QGraphicsDropShadowEffect
)

from ui.page1 import load_gilroy, BG, ACCENT, TXT_DARK, CARD_R, PAD_H, PAD_V, BTN_H, BTN_R
from logic.db import enter_keys              # ← как и раньше
import pymysql                               # для load_data8

#  ─── если у вас ещё нет _date, скопируйте из page10 ───
# def _date(font=None): ...

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


def create_page8(self) -> QWidget:
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

    # ── заголовок
    ttl = QLabel("Ключи УКЭП"); ttl.setFont(f_h1)
    ttl.setStyleSheet(f"color:#fff;border-bottom:3px solid {ACCENT};padding-bottom:4px;")
    root.addWidget(ttl, alignment=Qt.AlignmentFlag.AlignLeft)

    # ── скролл + карточка
    scroll = QScrollArea(); scroll.setWidgetResizable(True)
    scroll.setFrameShape(QFrame.Shape.NoFrame)
    scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    root.addWidget(scroll)

    wrapper = QWidget(); wrap_l = QVBoxLayout(wrapper); wrap_l.setContentsMargins(0,0,0,0)

    card = QFrame()
    card.setMinimumWidth(1300); card.setMaximumWidth(1600)
    card.setStyleSheet(f"background:#fff;border-radius:{CARD_R}px;")
    card.setGraphicsEffect(QGraphicsDropShadowEffect(
            blurRadius=32, xOffset=0, yOffset=4, color=QColor(0,0,0,55)))
    cbox = QVBoxLayout(card)
    cbox.setContentsMargins(PAD_H, PAD_V//2, PAD_H, PAD_V//2)

    wrap_l.addWidget(card); scroll.setWidget(wrapper)

    # ── Header внутри карточки
    hdr = QWidget(); hb = QHBoxLayout(hdr); hb.setContentsMargins(0,0,0,0); hb.setSpacing(12)
    back = _btn("←", 34); back.setFixedWidth(42); back.clicked.connect(self.go_to_second_page)
    hb.addWidget(back, 0, Qt.AlignmentFlag.AlignLeft)
    htxt = QLabel("Информация по ключам УКЭП"); htxt.setFont(f_h2)
    htxt.setStyleSheet(f"color:{TXT_DARK};")
    hb.addWidget(htxt, 0, Qt.AlignmentFlag.AlignLeft); hb.addStretch(1)
    cbox.addWidget(hdr)

    # ── две формы в GridLayout ────────────────────────────────────
    g = QGridLayout(); g.setContentsMargins(12,12,12,12)
    g.setHorizontalSpacing(20); g.setVerticalSpacing(8)
    cbox.addLayout(g)

    f_group = QFontDatabase.font(fam, sty, 14); f_group.setBold(True)
    for col, txt in enumerate(("Основные данные", "Дополнительные сведения")):
        lbl = QLabel(txt); lbl.setFont(f_group); lbl.setStyleSheet(f"color:{TXT_DARK};")
        g.addWidget(lbl, 0, col*2)
    g.addWidget(_hline(ACCENT,1), 1, 0, 1, 3)

    FL, FR = QFormLayout(), QFormLayout()
    for F in (FL, FR):
        F.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        F.setVerticalSpacing(6); F.setHorizontalSpacing(18)
        F.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)

    g.addWidget(_vline(), 2, 1, 1, 1)
    g.addLayout(FL, 2, 0); g.addLayout(FR, 2, 2)
    g.setColumnStretch(0,1); g.setColumnStretch(2,1)

    # ── левая форма
    self.status_cb          = _combo("Статус", ["Да","Нет"], f_body)
    self.nositel_type_cb_key= _combo("Тип носителя + серийный", [], f_body)
    self.serial_le_key      = _edit("Серийный номер", f_body)
    self.issuer_cb_key      = _combo("УЦ", [], f_body)
    self.scope_cb_key       = _combo("Область/ЭДО", [], f_body)
    self.owner_cb_key       = _combo("Владелец", [], f_body)

    FL.addRow("Статус",           self.status_cb)
    FL.addRow("Носитель",         self.nositel_type_cb_key)
    FL.addRow("Серийный номер",   self.serial_le_key)
    FL.addRow("УЦ",               self.issuer_cb_key)
    FL.addRow("Область/ЭДО",      self.scope_cb_key)
    FL.addRow("Владелец",         self.owner_cb_key)

    # ── правая форма
    self.vip_cb              = _combo("VIP / Critical", ["VIP","Critical"], f_body)
    self.dateedit1_key       = _date(f_body)
    self.dateedit2           = _date(f_body)
    self.additional_cb_key   = _combo("Дополнительно", [], f_body)
    self.request_let_key     = _edit("Номер обращения", f_body)
    self.note_le_key         = _edit("Примечание", f_body)

    FR.addRow("VIP / Critical", self.vip_cb)
    FR.addRow("Дата начала",    self.dateedit1_key)
    FR.addRow("Дата окончания", self.dateedit2)
    FR.addRow("Дополнительно",  self.additional_cb_key)
    FR.addRow("Номер обращения",self.request_let_key)
    FR.addRow("Примечание",     self.note_le_key)

    # ── кнопка «Сохранить»
    btn_save = _btn("Сохранить", 30)
    btn_save.setFixedWidth(1280)
    btn_save.clicked.connect(lambda: save_value8(self))
    cbox.addSpacing(5); cbox.addWidget(btn_save,0,Qt.AlignmentFlag.AlignHCenter); cbox.addSpacing(5)

    # ── таблица + поиск
    tbl_frame = create_data_table8(self)
    tbl_frame.setStyleSheet("background:#fff;border:1px solid #d0d0d0;border-radius:8px;")
    tbl_frame.setMinimumHeight(200)
    cbox.addWidget(tbl_frame)

    # таймер обновления
    self.refresh_timer = QTimer(page); self.refresh_timer.setInterval(60000)
    self.refresh_timer.timeout.connect(lambda: load_data8(self)); self.refresh_timer.start()

    # Enter → сохранить
    QShortcut(QKeySequence("Return"), page).activated.connect(lambda: save_value8(self))

    fill_recent_values8(self)

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
    fill_recent_values8(self)
    return widget


def load_data8(self):
    """
    Загружает из базы данных последние 50 записей из таблицы KeysTable.
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
                LIMIT 50
            """
            like_pattern = f"%{search_text}%"
            cursor.execute(query, (like_pattern, like_pattern, like_pattern, like_pattern,
                                     like_pattern, like_pattern, like_pattern, like_pattern))
        else:
            query = "SELECT * FROM KeysTable ORDER BY ID DESC LIMIT 1000"
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
    status_cb = self.status_cb.currentText()
    nositel_type_cb = self.nositel_type_cb_key.currentText()
    cert_serial_le = self.serial_le_key.text()
    issuer_cb = self.issuer_cb_key.currentText()
    scope_cb = self.scope_cb_key.currentText()
    owner_cb = self.owner_cb_key.currentText()
    vip_cb = self.vip_cb.currentText()
    dateedit1 = self.dateedit1_key.date()
    dateedit2 = self.dateedit2.date()
    additional_cb = self.additional_cb_key.currentText()
    request_let = self.request_let_key.text()
    note_le = self.note_le_key.text()
    dateedit_str = dateedit1.toPyDate().strftime('%Y-%m-%d')
    dateedit2_str = dateedit2.toPyDate().strftime('%Y-%m-%d')

    enter_keys(status_cb, nositel_type_cb, cert_serial_le, issuer_cb, scope_cb, owner_cb, vip_cb,
               dateedit_str, dateedit2_str, additional_cb, request_let, note_le)
    clear_fields(self)
    # Обновляем таблицу сразу после сохранения
    load_data8(self)
    fill_recent_values8(self)



def clear_fields(self):
    # LineEdit’ы
    for le in (self.serial_le_key, self.request_let_key, self.note_le_key):
        le.clear()

    # ComboBox’ы – сбрасываем выбор, но НЕ .clear()
    for cb in (
            self.status_cb, self.nositel_type_cb_key, self.issuer_cb_key,
            self.scope_cb_key, self.owner_cb_key, self.vip_cb,
            self.additional_cb_key
    ):
        cb.setCurrentIndex(-1)
        cb.clearEditText()

    # даты
    self.dateedit1_key.setDate(QDate.currentDate())
    self.dateedit2.setDate(QDate.currentDate())


# ────────────────────────────────────────────────────────────────
def fill_recent_values8(self, limit: int = 5) -> None:
    """Пополняет ComboBox-ы уникальными значениями из последних записей."""
    try:
        con = pymysql.connect(host="localhost", port=3306, user="newuser",
                              password="852456qaz", database="IB",
                              charset="utf8mb4",
                              cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        cur.execute("""
            SELECT type, owner, scope_using,
                   owner_fullname, additional, status
            FROM KeysTable
            ORDER BY ID DESC
            LIMIT %s
        """, (limit,))
        rows = cur.fetchall(); con.close()

        # множества уникальных
        media   = {r["type"]            for r in rows if r["type"]}
        ucs     = {r["owner"]           for r in rows if r["owner"]}          # УЦ
        scopes  = {r["scope_using"]     for r in rows if r["scope_using"]}
        owners  = {r["owner_fullname"]  for r in rows if r["owner_fullname"]}
        adds    = {r["additional"]      for r in rows if r["additional"]}
        stats   = {r["status"]          for r in rows if r["status"]}

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

        _sync(self.nositel_type_cb_key, media)   # «Тип носителя + серийный»
        _sync(self.issuer_cb_key,       ucs)     # УЦ
        _sync(self.scope_cb_key,        scopes)
        _sync(self.owner_cb_key,        owners)
        _sync(self.additional_cb_key,   adds)
        _sync(self.status_cb,           stats)   # «Да/Нет»

    except Exception as e:
        print("fill_recent_values8 error:", e)
