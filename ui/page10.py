# ui/page10.py
from datetime import datetime
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
    self.scope_cb      = _combo("Область/ЭДО", [], f_body)
    self.dns_le        = _edit("DNS", f_body)
    self.resolution_cb = _combo("Резолюция ИБ", ["уточнение","согласовано","отказано"], f_body)
    self.note_le       = _edit("Примечание", f_body)

    FR.addRow("Владелец АС", self.owner_cb)
    FR.addRow("Алгоритм",    self.algo_cb)
    FR.addRow("Область/ЭДО", self.scope_cb)
    FR.addRow("DNS",         self.dns_le)
    FR.addRow("Резолюция ИБ",self.resolution_cb)
    FR.addRow("Примечание",  self.note_le)

    # ― кнопка «Сохранить»
    btn_save = _btn("Сохранить", 30)
    btn_save.setFixedWidth(1280)              # CARD_W – PAD*2
    btn_save.clicked.connect(lambda: save_value10(self))
    cbox.addSpacing(5); cbox.addWidget(btn_save,0,Qt.AlignmentFlag.AlignHCenter); cbox.addSpacing(5)

    # ― таблица + поиск
    tbl_frame = create_data_table10(self)
    tbl_frame.setStyleSheet("background:#fff;border:1px solid #d0d0d0;border-radius:8px;")
    tbl_frame.setMinimumHeight(200)
    cbox.addWidget(tbl_frame)

    # таймер обновления
    self.refresh_timer = QTimer(page); self.refresh_timer.setInterval(60000)
    self.refresh_timer.timeout.connect(lambda: load_data10(self)); self.refresh_timer.start()

    # Enter → сохранить
    QShortcut(QKeySequence("Return"), page).activated.connect(lambda: save_value10(self))

    fill_recent_values10(self)

    return page

def create_data_table10(self) -> QWidget:
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

    # Перенос текста и отключаем усечение
    self.table_widget10.setWordWrap(True)
    self.table_widget10.setTextElideMode(Qt.TextElideMode.ElideNone)

    # Делегат для WrapText
    class WrapDelegate(QStyledItemDelegate):
        def initStyleOption(self, option, index):
            super().initStyleOption(option, index)
            option.features |= QStyleOptionViewItem.ViewItemFeature.WrapText

    self.table_widget10.setItemDelegate(WrapDelegate(self.table_widget10))

    # Растягиваем колонки и авто-подгоняем высоту строк
    hdr = self.table_widget10.horizontalHeader()
    hdr.setStretchLastSection(True)
    hdr.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    self.table_widget10.verticalHeader().setSectionResizeMode(
        QHeaderView.ResizeMode.ResizeToContents
    )

    layout.addWidget(self.table_widget10)

    # Подключаем загрузку и первоначальную отрисовку
    self.search_line10.textChanged.connect(lambda: load_data10(self))
    load_data10(self)

    return widget

def load_data10(self):
    """
    Загружает из базы данных записи из таблицы TLS.
    При наличии текста в поиске — фильтрация по всем столбцам.
    """
    search_text = self.search_line10.text().strip()
    try:
        import pymysql
        con = pymysql.connect(
            host="localhost", port=3306, user="newuser", password="852456qaz",
            database="IB", charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor
        )
        cur = con.cursor()
        if search_text:
            patt = f"%{search_text}%"
            cur.execute("""
                SELECT * FROM TLS
                WHERE CAST(ID          AS CHAR) LIKE %s
                   OR number           LIKE %s
                   OR date             LIKE %s
                   OR environment      LIKE %s
                   OR access           LIKE %s
                   OR issuer           LIKE %s
                   OR initiator        LIKE %s
                   OR owner            LIKE %s
                   OR algorithm        LIKE %s
                   OR scope            LIKE %s
                   OR DNS              LIKE %s
                   OR resolution       LIKE %s
                   OR note             LIKE %s
                ORDER BY ID DESC
                LIMIT 50
            """, (patt,) * 13)
        else:
            cur.execute("SELECT * FROM TLS ORDER BY ID DESC LIMIT 500")

        rows = cur.fetchall()
        con.close()

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
                self.table_widget10.setItem(r, c, QTableWidgetItem(str(val) if val is not None else ""))

        self.table_widget10.resizeRowsToContents()

    except Exception as e:
        print("Ошибка загрузки данных для TLS:", e)

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