# ────────────────────────────────────────────────────────────────────
#  Страница 7  —  СКЗИ  (оформление, как у page6)
# ────────────────────────────────────────────────────────────────────
from PyQt6.QtCore   import Qt, QTimer, QDate
from PyQt6.QtGui    import QFontDatabase, QShortcut, QKeySequence, QColor
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QLabel, QPushButton, QLineEdit, QComboBox, QDateEdit,
    QFrame, QGraphicsDropShadowEffect, QTableWidget, QHeaderView,
    QTableWidgetItem, QSizePolicy, QScrollArea, QSpacerItem, QApplication
)
import pymysql
from datetime import datetime
from ui.page1 import load_gilroy, BG, ACCENT, TXT_DARK, CARD_R, PAD_H, PAD_V, BTN_R, BTN_H
from logic.db   import enter_sczy



def set_edit_error_style(edit: QLineEdit, error: bool) -> None:
    """
    Красим QLineEdit:
      • error == True  → красная рамка
      • error == False → штатная серая
    """
    base = (
        "background:#fff;"
        "border-radius:6px;"
        "padding:4px 8px;"
        f"color:{TXT_DARK};"
    )
    red   = "border:1px solid red;"
    gray  = "border:1px solid #88959e;"
    edit.setStyleSheet(base + (red if error else gray))


def set_combo_error_style(cb: QComboBox, error: bool) -> None:
    """
    То же самое для QComboBox.
    """
    base = (
        "background:#fff;"
        "border-radius:6px;"
        "padding:2px 32px 2px 8px;"
        f"color:{TXT_DARK};"
    )
    red   = "border:1px solid red;"
    gray  = "border:1px solid #88959e;"
    # сохраняем остальную часть стилей (стрелка, список) из _combo()
    extra = """
        QComboBox QAbstractItemView {
            border:1px solid #88959e;
            outline:0;
            selection-background-color:rgba(139,197,64,.18);
        }
    """
    cb.setStyleSheet(base + (red if error else gray) + extra)


# ─── глобальные мелочи ────────────────────────────────────────────
CARD_W = 1300
PAD_H  = 20
PAD_V  = 16

# ─── маленькие фабрики для линий, полей и кнопок ─────────────────────
def _hline(color=ACCENT, h=2):
    ln = QFrame(); ln.setFixedHeight(h)
    ln.setStyleSheet(f"background:{color};border:none;")
    return ln

def _vline(color="#d0d0d0", w=1):
    ln = QFrame()                 # вертикальная тонкая линия
    ln.setFixedWidth(w)
    ln.setFrameShape(QFrame.Shape.VLine)
    ln.setStyleSheet(f"background:{color};border:none;")
    return ln

def _edit(ph: str, font=None):
    e = QLineEdit()
    e.setPlaceholderText(ph)
    e.setFixedHeight(34)
    e.setSizePolicy(QSizePolicy.Policy.Expanding,  # ← добавлено
                    QSizePolicy.Policy.Fixed)
    if font:
        e.setFont(font)

    e.setStyleSheet(f"""
        QLineEdit {{
            background:#fff;
            border:1px solid #88959e;       /* чуть темнее и без «прилипания» к QLabel */
            border-radius:6px;
            padding:4px 8px;
            color:{TXT_DARK};               /* основной цвет текста */
        }}
        QLineEdit:focus {{
            border:1px solid {ACCENT};
        }}
        QLineEdit::placeholder {{
            color:{ACCENT};                 /* зелёный плейс-холдер */
        }}
    """)
    return e


# helpers.py ­— финальный вариант фабрики
def _combo(ph: str, items: list[str], font=None) -> QComboBox:
    cb = QComboBox()
    cb.addItems(items)
    cb.setCurrentIndex(-1)
    cb.setEditable(True)
    cb.lineEdit().setPlaceholderText(ph)
    cb.setFixedHeight(34)
    cb.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    if font:
        cb.setFont(font)
        cb.lineEdit().setFont(font)

    cb.setStyleSheet(f"""
    /* ───────────────────────────────────────── основное поле ──── */
    QComboBox {{
        background:#fff;
        border:1px solid #88959e;
        border-radius:6px;
        padding:2px 32px 2px 8px;            /* справа место под стрелку */
        color:{TXT_DARK};
    }}
    QComboBox:focus {{ border:1px solid {ACCENT}; }}

    QComboBox QLineEdit {{ border:none; padding:0; }}
    QComboBox QLineEdit::placeholder {{ color:{ACCENT}; letter-spacing:.3px; }}

    /* ───────────────────────────────────────── зона стрелки ───── */
    QComboBox::drop-down {{
        subcontrol-origin:padding;
        subcontrol-position:top right;
        width:26px;
        border:none;                         /* ← убираем «усы» */
        background:transparent;              /* ← БЕЗ заливки */
    }}

    /* рисуем ТОЛЬКО разделительную линию — псевдо-границей */
    QComboBox::drop-down {{
        border-left:1px solid #88959e;
    }}
    QComboBox:hover::drop-down {{
        background:rgba(139,197,64,.12);     /* мягкий accent-hover */
    }}

    /* ───────────────────────────────────────── стрелка ────────── */
    QComboBox::down-arrow {{
        image:url(icons/chevron_down.svg);   /* 10×6 px одноцветный SVG */
        width:10px; height:6px; margin-right:8px;
    }}
    QComboBox::down-arrow:on {{ image:url(icons/chevron_up.svg); }}

    /* ───────────────────────────────────────── список ─────────── */
    QComboBox QAbstractItemView {{
        border:1px solid #88959e;
        outline:0;
        selection-background-color:rgba(139,197,64,.18);
        padding:2px 0;
    }}
    """)

    return cb


def _btn(text:str, h=BTN_H):
    b = QPushButton(text); b.setCursor(Qt.CursorShape.PointingHandCursor); b.setFixedHeight(h)
    b.setStyleSheet(
        f"QPushButton{{background:{BG};color:#fff;border:none;border-radius:{BTN_R}px;}}"
        f"QPushButton:hover{{background:{ACCENT};}}"
    )
    return b


def _fix_form_labels(form: QFormLayout, f_norm, f_small, small_set):
    """Снять рамку + выставить правильный шрифт у всех QLabel в форме."""
    for i in range(form.rowCount()):
        lbl = form.itemAt(i, QFormLayout.ItemRole.LabelRole).widget()
        lbl.setStyleSheet(f"color:{TXT_DARK};border:none;background:transparent;padding:0;margin:0;")
        lbl.setFont(f_small if lbl.text() in small_set else f_norm)

# ─────────────────────────────────────────────────────────────────────
def create_page7(self) -> QWidget:
    fam, sty = load_gilroy()
    f_h1 = QFontDatabase.font(fam, sty, 28)
    f_h2 = QFontDatabase.font(fam, sty, 20)
    f_body = QFontDatabase.font(fam, sty, 12)  # <-- основной текст

    # ─── внутри create_page7 ────────────────────────────────────────────
    page = QWidget();
    page.setStyleSheet(f"background:{BG};")

    # 1) убираем лишние внешние отступы
    root = QVBoxLayout(page)
    root.setContentsMargins(16, 16, 16, 16)  # было 24,24,24,24

    # Escape → назад
    QShortcut(QKeySequence("Escape"), page).activated.connect(self.go_to_second_page)
    # глобально подменим семейство дефолтного шрифта приложения
    QApplication.setFont(f_body)
    # Заголовок страницы
    ttl = QLabel("СКЗИ"); ttl.setFont(f_h1)
    ttl.setStyleSheet(f"color:#fff;border-bottom:3px solid {ACCENT};padding-bottom:4px;")
    root.addWidget(ttl, alignment=Qt.AlignmentFlag.AlignLeft)
    root.addSpacing(8)  # было 34

    # ── прокручиваемая карточка ─────────────────────────────────────
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setFrameShape(QFrame.Shape.NoFrame)

    # ← п.1  правильный enum в Qt6
    scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    root.addWidget(scroll)  # оставляем ОДИН раз, без AlignHCenter

    # ── создаём wrapper и card ──────────────────────────────────────
    wrapper = QWidget()
    wrap_l = QVBoxLayout(wrapper)
    wrap_l.setContentsMargins(0, 0, 0, 0)

    card = QFrame()
    card.setMinimumWidth(CARD_W)
    card.setMaximumWidth(1600)
    card.setSizePolicy(
               QSizePolicy.Policy.Expanding,
               QSizePolicy.Policy.Preferred
        )
    card.setStyleSheet(f"background:#fff;border-radius:{CARD_R}px;")
    card.setGraphicsEffect(QGraphicsDropShadowEffect(
        blurRadius=32, xOffset=0, yOffset=4, color=QColor(0, 0, 0, 55)))

    # Layout внутри карточки
    cbox = QVBoxLayout(card)
    cbox.setContentsMargins(PAD_H, PAD_V//2, PAD_H, PAD_V // 2)

    wrap_l.addWidget(card)

    scroll.setWidget(wrapper)



    # Header внутри карточки
    h = QWidget(); hb = QHBoxLayout(h); hb.setSpacing(12); hb.setContentsMargins(0,0,0,0)
    back = QPushButton("←")
    back.setFont(f_h2)  # 20 pt стрелка
    h_txt = QLabel("Информация по СКЗИ")
    h_txt.setFont(f_h2)  # 20 pt текст

    # ── рамка с формами ─────────────────────────────────────────────
    frame = QFrame()
    frame.setStyleSheet("border:1px solid #d0d0d0;border-radius:8px;")
    cbox.addWidget(frame)

    g = QGridLayout(frame)
    g.setContentsMargins(12, 12, 12, 12)  # было 18,18,18,18
    g.setHorizontalSpacing(20)  # было 30
    g.setVerticalSpacing(8)  # было 12

    # секционные заголовки – меньше шрифт + жирный
    f_group = QFontDatabase.font(fam, sty, 14)
    f_group.setBold(True)

    for col, txt in enumerate(("Основные данные", "Дополнительные сведения")):
        h_lbl = QLabel(txt);
        h_lbl.setFont(f_group)
        h_lbl.setStyleSheet(f"color:{TXT_DARK}; border:none;")  # ← без рамки!
        g.addWidget(h_lbl, 0, col * 2)
    g.addWidget(_hline(ACCENT, 1), 1, 0, 1, 3)  # ACCENT-зелёная, 1 px

    FL, FR = QFormLayout(), QFormLayout()
    for F in (FL, FR):
        F.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        F.setVerticalSpacing(6)
        F.setHorizontalSpacing(18)
        F.setFieldGrowthPolicy(
            QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        # разбираем автоматически созданные метки:
        for i in range(F.rowCount()):
            lbl = F.itemAt(i, QFormLayout.ItemRole.LabelRole).widget()
            lbl.setStyleSheet("background:transparent;padding:0;margin:0;")

    g.addWidget(_vline(), 2, 1, 1, 1)  # разделитель колонок
    g.addLayout(FL, 2, 0)
    g.addLayout(FR, 2, 2)
    g.setColumnStretch(0, 1)  # левая форма
    g.setColumnStretch(1, 0)  # вертикальная линия
    g.setColumnStretch(2, 1)  # правая форма
    # ── левая колонка ───────────────────────────────────────────────
    self.skzi_name_cb = _combo("Наименование СКЗИ", [], f_body)
    self.skzi_type       = _combo("Тип СКЗИ", ["ПО", "ПАК"], f_body)
    self.skzi_version_cb = _combo("Версия СКЗИ", [], f_body)
    self.dateedit        = QDateEdit(calendarPopup=True)
    self.dateedit.setFont(f_body)


    self.dateedit.setDate(QDate.currentDate())
    self.dateedit.setFixedHeight(34)
    self.location        = _edit("Местонахождение ТОМ", f_body)
    self.location_TOM = _edit("ТОМ", f_body)
    self.doc_info_skzi = _edit("Дата и номер документа", f_body)
    self.contract_skzi = _edit("Договор", f_body)
    self.fullname_owner = _edit("Владелец", f_body)

    FL.addRow("Название СКЗИ", self.skzi_name_cb)
    FL.addRow("Тип СКЗИ", self.skzi_type)
    FL.addRow("Версия СКЗИ", self.skzi_version_cb)
    FL.addRow("Дата регистрации СКЗИ", self.dateedit)
    FL.addRow("Местонахождение ТОМ", self.location)
    FL.addRow("ТОМ", self.location_TOM)
    FL.addRow("Документ", self.doc_info_skzi)
    FL.addRow("Договор", self.contract_skzi)
    FL.addRow("Владелец", self.fullname_owner)

    # ── правая колонка ──────────────────────────────────────────────
    self.reg_number_le = _edit("Регистрационный номер", f_body)
    self.from_whom_cb  = _combo("От кого получены", [], f_body)
    self.owners = _combo("Владельцы", [], f_body)
    self.buss_proc = _combo("Бизнес-процессы", [], f_body)
    self.additional_le = _edit("Дополнительно", f_body)
    self.note_cb = _combo("Примечание", [], f_body)
    self.certnum_le = _edit("Сертификат", f_body)
    self.dateedit2 = QDateEdit(calendarPopup=True)
    self.dateedit2.setDate(QDate.currentDate())
    self.dateedit2.setFixedHeight(34)
    self.dateedit2.setFont(f_body)

    FR.addRow("Регистрационный номер", self.reg_number_le)
    FR.addRow("От кого получены", self.from_whom_cb)
    FR.addRow("Владельцы", self.owners)
    FR.addRow("Бизнес-процессы", self.buss_proc)
    FR.addRow("Дополнительно", self.additional_le)
    FR.addRow("Примечание", self.note_cb)
    FR.addRow("Сертификат", self.certnum_le)
    FR.addRow("Доп. дата", self.dateedit2)



    #   ▸ после того, как в FL и FR добавили все строки …
    small_labels = {
        "Дата регистрации СКЗИ",
        "Местонахождение ТОМ",
        "Регистрационный номер",
    }
    f_body = QFontDatabase.font(fam, sty, 12)
    f_body_small = QFontDatabase.font(fam, sty, 11)

    _fix_form_labels(FL, f_body, f_body_small, small_labels)
    _fix_form_labels(FR, f_body, f_body_small, small_labels)

    for form in (FL, FR):
        for i in range(form.rowCount()):
            lbl = form.itemAt(i, QFormLayout.ItemRole.LabelRole).widget()
            if lbl.text() in small_labels:
                lbl.setFont(f_body_small)

    g.addLayout(FL, 2, 0)
    g.addLayout(FR,2,2)

    # ── кнопка «Сохранить» ────────────────────────────────────────────
    btn_save = _btn("Сохранить", 30)
    btn_save.setFixedWidth(CARD_W - PAD_H * 2)
    btn_save.clicked.connect(lambda: save_value7(self))
    cbox.addSpacing(5); cbox.addWidget(btn_save,0,Qt.AlignmentFlag.AlignHCenter); cbox.addSpacing(5)
    btn_save.setFixedWidth(CARD_W - PAD_H * 2)

    # ── export-кнопки в ряд ───────────────────────────────────────────
    ex_row = QHBoxLayout(); ex_row.setSpacing(12)
    ex_row.addWidget(_btn("Экспорт всех данных SCZY", 30))  # 36 px
    ex_row.addWidget(_btn("Экспорт отфильтрованных SCZY", 30))
    cbox.addLayout(ex_row);

    # ── таблица + поиск ──────────────────────────────────────────────
    tbl_frame = create_data_table7(self)
    tbl_frame.setStyleSheet("background:#fff;border:1px solid #d0d0d0;border-radius:8px;")
    tbl_frame.setContentsMargins(0, 0, 0, 0)
    tbl_frame.setMinimumHeight(180)
    cbox.addWidget(tbl_frame)

    # таймер обновления
    self.refresh_timer = QTimer(page); self.refresh_timer.setInterval(60000)
    self.refresh_timer.timeout.connect(lambda: load_data7(self)); self.refresh_timer.start()

    # Enter → сохранить
    QShortcut(QKeySequence("Return"), page).activated.connect(lambda: save_value7(self))

    # перед return page
    fill_recent_values7(self)
    return page


# ─────────────────────────────────────────────────────────────────────
def create_data_table7(self) -> QFrame:
    frame = QFrame();
    frame.setStyleSheet("border:1px solid #d0d0d0;border-radius:8px;")
    lay = QVBoxLayout(frame); lay.setContentsMargins(12,12,12,12); lay.setSpacing(6)

    self.search_line7 = QLineEdit(placeholderText="Введите текст для поиска…")
    lay.addWidget(self.search_line7)

    self.table_widget7 = QTableWidget()
    headers = [
        "ID","Наименование СКЗИ","Тип СКЗИ","Версия","Дата","Рег. номер",
        "Местонахождение","ТОМ","От кого","Документ","Договор",
        "Владелец","Владельцы","Б-проц.","Доп.","Примеч.","Сертификат","Доп. дата"
    ]
    self.table_widget7.setColumnCount(len(headers))
    self.table_widget7.setHorizontalHeaderLabels(headers)
    self.table_widget7.setStyleSheet(
                "QTableWidget{font-size:9pt;} "
         "QHeaderView::section{font-weight:bold; font-size:9pt;}"
        )
    lay.addWidget(self.table_widget7)
    self.table_widget7.verticalHeader().setVisible(False)   #  ← добавили
    self.table_widget7.setMinimumWidth(CARD_W - PAD_H * 2)
    hdr = self.table_widget7.horizontalHeader()
    hdr.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    # уменьшаем минимальную ширину колонок до 60px
    hdr.setMinimumSectionSize(60)
    self.search_line7.textChanged.connect(lambda: load_data7(self))
    load_data7(self)
    return frame


# ─────────────────────────────────────────────────────────────────────
def load_data7(self):
    srch = self.search_line7.text().strip()
    try:
        con = pymysql.connect(host="localhost", port=3306, user="newuser",
                              password="852456qaz", database="IB",
                              charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        if srch:
            patt = f"%{srch}%"
            cur.execute("""
                SELECT * FROM SCZY WHERE
                CAST(ID AS CHAR) LIKE %s OR name_of_SCZY LIKE %s OR sczy_type LIKE %s
                OR number_SCZY LIKE %s OR owner LIKE %s OR fullname_owner LIKE %s
                ORDER BY ID DESC LIMIT 50
            """, (patt,)*6)
        else:
            cur.execute("SELECT * FROM SCZY ORDER BY ID DESC LIMIT 500")
        rows = cur.fetchall(); con.close()

        self.table_widget7.setRowCount(len(rows))
        for r,row in enumerate(rows):
            data = [
                row.get("ID"), row.get("name_of_SCZY"), row.get("sczy_type"), row.get("number_SCZY"),
                row.get("date"), row.get("number_license"), row.get("location"), row.get("location_TOM_text"),
                row.get("owner"), row.get("date_and_number"), row.get("contract"), row.get("fullname_owner"),
                row.get("owners"), row.get("buss_proc"), row.get("additional"), row.get("note"),
                row.get("number_certificate"), row.get("date_expired")
            ]
            for c,val in enumerate(data):
                self.table_widget7.setItem(r,c,QTableWidgetItem(str(val) if val else ""))
    except Exception as e:
        print("SCZY load error:", e)


# ─────────────────────────────────────────────────────────────────────
def save_value7(self):
    enter_sczy(
        self.skzi_name_cb.currentText(), self.skzi_type.currentText(),
        self.skzi_version_cb.currentText(), self.dateedit.date().toString("yyyy-MM-dd"),
        self.reg_number_le.text(), self.location.text(), self.location_TOM.text(),
        self.from_whom_cb.currentText(), self.doc_info_skzi.text(), self.contract_skzi.text(),
        self.fullname_owner.text(), self.owners.currentText(), self.buss_proc.currentText(),
        self.additional_le.text(), self.note_cb.currentText(), self.certnum_le.text(),
        self.dateedit2.date().toString("yyyy-MM-dd")
    )
    clear_fields(self);
    load_data7(self)
    fill_recent_values7(self)


# ─────────────────────────────────────────────────────────────────────
def clear_fields(self):
    # LineEdit’ы
    for le in (
        self.reg_number_le, self.location, self.location_TOM,
        self.doc_info_skzi, self.contract_skzi, self.fullname_owner,
        self.additional_le, self.certnum_le
    ):
        le.clear()

    # ComboBox’ы — сброс выбора, но не .clear()
    for cb in (
        self.skzi_name_cb, self.skzi_version_cb, self.from_whom_cb,
        self.owners, self.buss_proc, self.note_cb, self.skzi_type
    ):
        cb.setCurrentIndex(-1)
        cb.clearEditText()          # чистим текст в lineEdit()

    # даты
    self.dateedit.setDate(QDate.currentDate())
    self.dateedit2.setDate(QDate.currentDate())


def fill_recent_values7(self, limit: int = 5) -> None:
    """
    Берём последние `limit` строк из SCZY и заполняем выпадающие списки
    уникальными значениями (без дубликатов).
    """
    try:
        con = pymysql.connect(host="localhost", port=3306, user="newuser",
                              password="852456qaz", database="IB",
                              charset="utf8mb4",
                              cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        cur.execute("""
            SELECT name_of_SCZY, number_SCZY, owner,
                   fullname_owner, buss_proc
            FROM SCZY ORDER BY ID DESC LIMIT %s
        """, (limit,))
        rows = cur.fetchall(); con.close()

        # множества уникальных значений
        names   = {r["name_of_SCZY"]     for r in rows if r["name_of_SCZY"]}
        vers    = {r["number_SCZY"]      for r in rows if r["number_SCZY"]}
        owners  = {r["owner"]            for r in rows if r["owner"]}
        fullown = {r["fullname_owner"]   for r in rows if r["fullname_owner"]}
        bproc   = {r["buss_proc"]        for r in rows if r["buss_proc"]}

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

        _sync(self.skzi_name_cb, names)
        _sync(self.skzi_version_cb, vers)
        _sync(self.from_whom_cb, owners)
        _sync(self.owners, fullown)
        _sync(self.buss_proc, bproc)

    except Exception as e:
        print("fill_recent_values7 error:", e)