from datetime import datetime
from PyQt6 import QtWidgets
from PyQt6.QtGui import QShortcut, QKeySequence, QPalette, QColor, QIntValidator
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout,
    QComboBox, QSizePolicy, QGroupBox, QFormLayout, QTableWidget, QTableWidgetItem, QHeaderView, QDateEdit,
    QStyleOptionViewItem, QStyledItemDelegate, QAbstractItemView
)
from PyQt6.QtCore import Qt, QDate, QTimer

from logic.db import enter_keys

# ui/page8.py
from PyQt6.QtCore import Qt, QDate, QTimer
from PyQt6.QtGui import QFontDatabase, QKeySequence, QShortcut, QColor
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QLabel, QScrollArea, QFrame, QGraphicsDropShadowEffect
)
from ui.page7 import (  # берём фабрики/стили из «красивой» 7-й страницы
    _combo
)
from ui.page1 import load_gilroy, BG, ACCENT, TXT_DARK, CARD_R, PAD_H, PAD_V, BTN_H, BTN_R
from logic.db import enter_keys  # ← как и раньше
import pymysql  # для load_data8



# ───── маленькие фабрики ──────────────────────────────────────────────
def _hline(color=ACCENT, h=2):
    ln = QFrame();
    ln.setFixedHeight(h)
    ln.setStyleSheet(f"background:{color};border:none;")
    return ln


def _vline(color="#d0d0d0", w=1):
    ln = QFrame();
    ln.setFixedWidth(w)
    ln.setFrameShape(QFrame.Shape.VLine)
    ln.setStyleSheet(f"background:{color};border:none;")
    return ln


def _edit(ph: str, font=None) -> QLineEdit:
    e = QLineEdit();
    e.setPlaceholderText(ph);
    e.setFixedHeight(34)
    e.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    if font: e.setFont(font)
    e.setStyleSheet(f"""
        QLineEdit {{
            background:#fff; border:1px solid #88959e; border-radius:6px;
            padding:4px 8px; color:{TXT_DARK};
        }}
        QLineEdit:focus{{ border:1px solid {ACCENT}; }}
        QLineEdit::placeholder{{ color:{ACCENT}; }}
    """);
    return e


def _btn(text: str, h=BTN_H):
    b = QPushButton(text);
    b.setCursor(Qt.CursorShape.PointingHandCursor);
    b.setFixedHeight(h)
    b.setStyleSheet(
        f"QPushButton{{background:{BG};color:#fff;border:none;border-radius:{BTN_R}px;}}"
        f"QPushButton:hover{{background:{ACCENT};}}"
    );
    return b


# ───── вверху рядом с _edit и _combo ─────────────────────────────
def _date(font=None) -> QDateEdit:
    d = QDateEdit(calendarPopup=True)
    d.setDate(QDate.currentDate())
    d.setDisplayFormat("dd.MM.yyyy")  # как на скрине
    d.setFixedHeight(34)
    d.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    if font: d.setFont(font)

    return d


def create_page8(self) -> QWidget:
    fam, sty = load_gilroy()
    f_h1 = QFontDatabase.font(fam, sty, 28)
    f_h2 = QFontDatabase.font(fam, sty, 20)
    f_body = QFontDatabase.font(fam, sty, 12)

    page = QWidget();
    page.setStyleSheet(f"background:{BG};")
    root = QVBoxLayout(page)
    root.setContentsMargins(16, 16, 16, 16)
    root.setSpacing(8)

    # Esc → назад
    QShortcut(QKeySequence("Escape"), page).activated.connect(self.go_to_second_page)

    # ── заголовок
    ttl = QLabel("Ключи УКЭП");
    ttl.setFont(f_h1)
    ttl.setStyleSheet(f"color:#fff;border-bottom:3px solid {ACCENT};padding-bottom:4px;")
    root.addWidget(ttl, alignment=Qt.AlignmentFlag.AlignLeft)

    # ── скролл + карточка
    scroll = QScrollArea();
    scroll.setWidgetResizable(True)
    scroll.setFrameShape(QFrame.Shape.NoFrame)
    scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    root.addWidget(scroll)

    wrapper = QWidget();
    wrap_l = QVBoxLayout(wrapper);
    wrap_l.setContentsMargins(0, 0, 0, 0)

    card = QFrame()
    card.setMinimumWidth(1300);
    card.setStyleSheet(f"background:#fff;border-radius:{CARD_R}px;")
    card.setGraphicsEffect(QGraphicsDropShadowEffect(
        blurRadius=32, xOffset=0, yOffset=4, color=QColor(0, 0, 0, 55)))
    cbox = QVBoxLayout(card)
    cbox.setContentsMargins(PAD_H, PAD_V // 2, PAD_H, PAD_V // 2)

    wrap_l.addWidget(card);
    scroll.setWidget(wrapper)

    # ── Header внутри карточки
    hdr = QWidget();
    hb = QHBoxLayout(hdr);
    hb.setContentsMargins(0, 0, 0, 0);
    hb.setSpacing(12)
    back = _btn("←", 34);
    back.setFixedWidth(42);
    back.clicked.connect(self.go_to_second_page)
    hb.addWidget(back, 0, Qt.AlignmentFlag.AlignLeft)
    htxt = QLabel("Информация по ключам УКЭП");
    htxt.setFont(f_h2)
    htxt.setStyleSheet(f"color:{TXT_DARK};")
    hb.addWidget(htxt, 0, Qt.AlignmentFlag.AlignLeft);
    hb.addStretch(1)
    cbox.addWidget(hdr)

    # ── две формы в GridLayout ────────────────────────────────────
    g = QGridLayout();
    g.setContentsMargins(12, 12, 12, 12)
    g.setHorizontalSpacing(20);
    g.setVerticalSpacing(8)
    cbox.addLayout(g)

    f_group = QFontDatabase.font(fam, sty, 14);
    f_group.setBold(True)
    for col, txt in enumerate(("Основные данные", "Дополнительные сведения")):
        lbl = QLabel(txt);
        lbl.setFont(f_group);
        lbl.setStyleSheet(f"color:{TXT_DARK};")
        g.addWidget(lbl, 0, col * 2)
    g.addWidget(_hline(ACCENT, 1), 1, 0, 1, 3)

    FL, FR = QFormLayout(), QFormLayout()
    for F in (FL, FR):
        F.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        F.setVerticalSpacing(6);
        F.setHorizontalSpacing(18)
        F.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)

    g.addWidget(_vline(), 2, 1, 1, 1)
    g.addLayout(FL, 2, 0);
    g.addLayout(FR, 2, 2)
    g.setColumnStretch(0, 1);
    g.setColumnStretch(2, 1)

    # ── левая форма
    self.status_cb = _combo("Статус", ["Да", "Нет"], f_body)
    self.nositel_type_cb_key = _combo("Тип носителя + серийный", [], f_body)
    self.serial_le_key = _edit("Серийный номер", f_body)
    self.issuer_cb_key = _combo("УЦ", [], f_body)
    self.scope_cb_key = _combo("Область/ЭДО", [], f_body)
    self.owner_cb_key = _combo("Владелец", [], f_body)

    FL.addRow("Статус", self.status_cb)
    FL.addRow("Носитель", self.nositel_type_cb_key)
    FL.addRow("Серийный номер", self.serial_le_key)
    FL.addRow("УЦ", self.issuer_cb_key)
    FL.addRow("Область/ЭДО", self.scope_cb_key)
    FL.addRow("Владелец", self.owner_cb_key)

    # ── правая форма
    self.vip_cb = _combo("VIP / Critical", ["VIP", "Critical"], f_body)
    self.dateedit1_key = _date(f_body)
    self.dateedit2 = _date(f_body)
    self.additional_cb_key = _combo("Дополнительно", [], f_body)
    self.request_let_key = _edit("Номер обращения", f_body)
    self.note_le_key = _edit("Примечание", f_body)

    FR.addRow("VIP / Critical", self.vip_cb)
    FR.addRow("Дата начала", self.dateedit1_key)
    FR.addRow("Дата окончания", self.dateedit2)
    FR.addRow("Дополнительно", self.additional_cb_key)
    FR.addRow("Номер обращения", self.request_let_key)
    FR.addRow("Примечание", self.note_le_key)
    self.request_let_key = _edit("Номер обращения", f_body)
    self.request_let_key.setValidator(QIntValidator(0, 2_000_000_000, self))
    FR.addRow("Номер обращения", self.request_let_key)

    # ── кнопка «Сохранить»
    btn_save = _btn("Сохранить", 30)
    btn_save.setFixedWidth(300)
    btn_save.clicked.connect(lambda: save_value8(self))
    cbox.addSpacing(5);
    cbox.addWidget(btn_save, 0, Qt.AlignmentFlag.AlignHCenter);
    cbox.addSpacing(5)

    # ── export-кнопки в ряд ───────────────────────────────────────────
    ex_row = QHBoxLayout()
    ex_row.setSpacing(12)
    btn_export_all = _btn("Экспорт всех данных УКЭП", 30)
    btn_export_all.setFixedWidth(350)
    btn_export_filtered = _btn("Экспорт отфильтрованных УКЭП", 30)
    btn_export_filtered.setFixedWidth(350)

    ex_row.addWidget(btn_export_all, alignment=Qt.AlignmentFlag.AlignRight)
    ex_row.addWidget(btn_export_filtered, alignment=Qt.AlignmentFlag.AlignLeft)
    cbox.addLayout(ex_row)

    btn_export_all.clicked.connect(self.export_all_keystab)
    btn_export_filtered.clicked.connect(self.export_filtered_keystab)

    # ── таблица + поиск
    tbl_frame = create_data_table8(self)
    tbl_frame.setStyleSheet("background:#fff;border:1px solid #d0d0d0;border-radius:8px;")
    tbl_frame.setMinimumHeight(200)
    cbox.addWidget(tbl_frame)

    # Enter → сохранить
    QShortcut(QKeySequence("Return"), page).activated.connect(lambda: save_value8(self))

    fill_recent_values8(self)

    return page


def create_data_table8(self) -> QWidget:
    from PyQt6.QtCore import QEvent      # локальный импорт – как просили

    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setSpacing(5)

    # ── строка поиска ──────────────────────────────────────────
    search_row = QHBoxLayout()
    label = QLabel("Поиск:")
    self.search_line8 = QLineEdit(placeholderText="Введите текст для поиска…")
    self.search_line8.setStyleSheet(
        "QLineEdit{border:1px solid #d0d0d0; border-radius:4px; padding:2px 6px;}"
        f"QLineEdit:focus{{border:1px solid {ACCENT};}}"
    )
    search_row.addWidget(label)
    search_row.addWidget(self.search_line8)
    layout.addLayout(search_row)

    # ──   Т А Б Л И Ц А   ──────────────────────────────────────
    outer_self = self          # понадобится в замыкании

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

    self.table_widget8 = KeysTable()
    self.table_widget8.setStyleSheet(
        "QTableWidget{border:1px solid #d0d0d0; border-radius:4px;}"
    )

    headers = [
        "ID", "Статус", "Тип носителя", "Серийный №", "УЦ",
        "Область/ЭДО", "Владелец", "VIP / Crit.",
        "Начало", "Окончание", "Дополнит.",
        "№ обращения", "Примечание"
    ]
    self.table_widget8.setColumnCount(len(headers))
    self.table_widget8.setHorizontalHeaderLabels(headers)
    self.table_widget8.verticalHeader().setVisible(False)

    # перенос строк без «…»
    self.table_widget8.setWordWrap(True)
    self.table_widget8.setTextElideMode(Qt.TextElideMode.ElideNone)

    class _Wrap(QStyledItemDelegate):
        def initStyleOption(self, opt, idx):
            super().initStyleOption(opt, idx)
            opt.features |= QStyleOptionViewItem.ViewItemFeature.WrapText
    self.table_widget8.setItemDelegate(_Wrap(self.table_widget8))

    # стартовые ширины
    for col, w in enumerate(
        (40, 70, 110, 120, 110, 140, 150, 90, 95, 95, 120, 120, 150)
    ):
        hdr = self.table_widget8.horizontalHeader()
        hdr.setSectionResizeMode(col, QHeaderView.ResizeMode.Interactive)
        hdr.resizeSection(col, w)
    self.table_widget8.horizontalHeader().setStretchLastSection(True)
    self.table_widget8.verticalHeader().setSectionResizeMode(
        QHeaderView.ResizeMode.ResizeToContents
    )

    layout.addWidget(self.table_widget8)

    # ── поиск / загрузка ──────────────────────────────────────
    self.search_line8.textChanged.connect(lambda: load_data8(self))
    load_data8(self)

    # разрешаем редактирование ЛКМ
    self.table_widget8.setEditTriggers(
        QAbstractItemView.EditTrigger.DoubleClicked
        | QAbstractItemView.EditTrigger.SelectedClicked
    )

    # сохранение изменений
    self.table_widget8.itemChanged.connect(
        lambda it: on_key_item_changed(self, it)
    )

    return widget


def on_key_row_double_clicked(self, item: QTableWidgetItem):
    row = item.row()
    get = lambda col: self.table_widget8.item(row, col).text() if self.table_widget8.item(row, col) else ""

    self.status_cb.lineEdit().setText(get(1))
    self.nositel_type_cb_key.lineEdit().setText(get(2))
    self.serial_le_key.setText(get(3))
    self.issuer_cb_key.lineEdit().setText(get(4))
    self.scope_cb_key.lineEdit().setText(get(5))
    self.owner_cb_key.lineEdit().setText(get(6))
    self.vip_cb.lineEdit().setText(get(7))
    # ─── дата начала ─────────────────────────────────────────
    _safe_set(self.dateedit1_key, get(8))
    _safe_set(self.dateedit2, get(9))  # конец
    self.additional_cb_key.lineEdit().setText(get(10))
    self.request_let_key.setText(get(11))
    self.note_le_key.setText(get(12))

# ─── on_key_row_double_clicked ─────────────────────────────
def _safe_set(dateedit: QDateEdit, txt: str):
    for fmt in ("yyyy-MM-dd", "dd.MM.yyyy"):
        qd = QDate.fromString(txt, fmt)
        if qd.isValid():           # ✔️ только валидные даты
            dateedit.setDate(qd)
            break                  # нашли – хватит

def load_data8(self):
    """
    Загружает из базы данных записи из таблицы KeysTable.
    При наличии текста в поиске — фильтрация по всем столбцам.
    """
    search_text = self.search_line8.text().strip()
    try:
        con = pymysql.connect(
            host="localhost", port=3306, user="newuser", password="852456qaz",
            database="IB", charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor
        )
        cur = con.cursor()
        if search_text:
            patt = f"%{search_text}%"
            cur.execute("""
                SELECT * FROM KeysTable
                WHERE CAST(ID            AS CHAR) LIKE %s
                   OR status               LIKE %s
                   OR type                 LIKE %s
                   OR cert_serial_le       LIKE %s
                   OR owner                LIKE %s
                   OR scope_using          LIKE %s
                   OR owner_fullname       LIKE %s
                   OR VIP_Critical         LIKE %s
                   OR CAST(start_date      AS CHAR) LIKE %s
                   OR CAST(date_end        AS CHAR) LIKE %s
                   OR additional           LIKE %s
                   OR number_request       LIKE %s
                   OR note                 LIKE %s
                ORDER BY ID DESC
                LIMIT 500
            """, (patt,) * 13)
        else:
            cur.execute("SELECT * FROM KeysTable ORDER BY ID DESC LIMIT 500")

        rows = cur.fetchall()
        con.close()

        # ▸ блокируем сигналы, чтобы itemChanged не срабатывал
        self.table_widget8.blockSignals(True)

        self.table_widget8.setRowCount(len(rows))
        for r, row in enumerate(rows):
            cols = [
                row.get("ID"), row.get("status"),
                row.get("type"), row.get("cert_serial_le"),
                row.get("owner"), row.get("scope_using"),
                row.get("owner_fullname"), row.get("VIP_Critical"),
                row.get("start_date"), row.get("date_end"),
                row.get("additional"), row.get("number_request"),
                row.get("note"),
            ]
            for c, val in enumerate(cols):
                item = QTableWidgetItem("" if val is None else str(val))
                item.setData(Qt.ItemDataRole.UserRole, item.text())
                if c == 0:  # ID – только для чтения
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.table_widget8.setItem(r, c, item)
        self.table_widget8.resizeRowsToContents()

    finally:
        # ▸ обязательно возвращаем сигнал обратно
        self.table_widget8.blockSignals(False)

def _flash_row(tbl: QTableWidget, row: int, msec: int = 400):
    tbl.blockSignals(True)
    for col in range(tbl.columnCount()):
        cell = tbl.item(row, col)
        if cell:
            cell.setBackground(QColor(139, 197, 64, 40))   # мягкая зелёная
    tbl.blockSignals(False)

    def _clear():
        tbl.blockSignals(True)
        for col in range(tbl.columnCount()):
            cell = tbl.item(row, col)
            if cell:
                cell.setBackground(QColor(0, 0, 0, 0))
        tbl.blockSignals(False)

    QTimer.singleShot(msec, _clear)

def on_key_item_changed(self, item: QTableWidgetItem):
    # 0-я колонка (ID) – неизменяема
    if item.column() == 0:
        return

    original = item.data(Qt.ItemDataRole.UserRole)     # то, что было
    new_val  = item.text().strip()

    # пример валидации дат прямо здесь ─ можно расширить по своим правилам
    if item.column() in (8, 9):                        # «Начало» / «Окончание»
        try:
            # допускаем dd.MM.yyyy или yyyy-MM-dd
            for fmt in ("%d.%m.%Y", "%Y-%m-%d"):
                try:
                    new_val = datetime.strptime(new_val, fmt).strftime("%Y-%m-%d")
                    break
                except ValueError:
                    pass
            else:                                      # не распознали
                raise ValueError("Неверный формат даты")
        except ValueError as e:
            _rollback(item, original, str(e))
            return

    field_names = [
        "ID","status","type","cert_serial_le","owner",
        "scope_using","owner_fullname","VIP_Critical",
        "start_date","date_end","additional","number_request","note"
    ]
    field     = field_names[item.column()]
    record_id = self.table_widget8.item(item.row(), 0).text()

    try:
        with pymysql.connect(
            host="localhost", port=3306, user="newuser", password="852456qaz",
            database="IB", charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        ) as con:
            cur = con.cursor()
            cur.execute(f"UPDATE KeysTable SET `{field}`=%s WHERE ID=%s",
                        (new_val, record_id))
            con.commit()

        # ✓ всё сохранилось – запоминаем новое значение как «оригинал»
        item.setData(Qt.ItemDataRole.UserRole, new_val)
        _flash_row(self.table_widget8, item.row())     # зелёная вспышка

    except Exception as e:
        con.rollback()                                 # на всякий случай
        _rollback(item, original, e)


def _rollback(item: QTableWidgetItem, original: str, err) -> None:
    """Откатывает визуально и показывает ошибку."""
    tbl = item.tableWidget()
    tbl.blockSignals(True)         # ⚠️ чтобы не вызвать itemChanged второй раз
    item.setText(original)         # вернули как было
    tbl.blockSignals(False)

    QtWidgets.QMessageBox.critical(
        tbl, "Ошибка сохранения", str(err)
    )

def _flash_row(tbl: QTableWidget, row: int, msec: int = 400):
    """Мягко подсвечивает строку — как на page 6."""
    tbl.blockSignals(True)
    for col in range(tbl.columnCount()):
        cell = tbl.item(row, col)
        if cell:
            cell.setBackground(QColor(139, 197, 64, 40))
    tbl.blockSignals(False)

    def _clear():
        tbl.blockSignals(True)
        for col in range(tbl.columnCount()):
            cell = tbl.item(row, col)
            if cell:
                cell.setBackground(QColor(0, 0, 0, 0))
        tbl.blockSignals(False)

    QTimer.singleShot(msec, _clear)

def save_value8(self):
    errors = []

    # Проверка обязательных полей
    if not self.status_cb.currentText():
        errors.append("Поле «Статус» не должно быть пустым.")
    if not self.nositel_type_cb_key.currentText():
        errors.append("Поле «Носитель» не должно быть пустым.")
    if not self.serial_le_key.text().strip():
        errors.append("Поле «Серийный номер» не должно быть пустым.")
    if not self.issuer_cb_key.currentText():
        errors.append("Поле «УЦ» не должно быть пустым.")
    if not self.scope_cb_key.currentText():
        errors.append("Поле «Область/ЭДО» не должно быть пустым.")
    if not self.owner_cb_key.currentText():
        errors.append("Поле «Владелец» не должно быть пустым.")
    if not self.vip_cb.currentText():
        errors.append("Поле «VIP / Critical» не должно быть пустым.")
    if not self.request_let_key.text().strip():
        errors.append("Поле «Номер обращения» не должно быть пустым.")

    # Если есть ошибки, показываем диалог и выходим
    if errors:
        QtWidgets.QMessageBox.critical(
            self,
            "Ошибка заполнения",
            "Обнаружены ошибки:\n\n• " + "\n• ".join(errors)
        )
        return

    # Все поля прошли валидацию — собираем значения и сохраняем
    status_cb = self.status_cb.currentText()
    nositel_type_cb = self.nositel_type_cb_key.currentText()
    cert_serial_le = self.serial_le_key.text().strip()
    issuer_cb = self.issuer_cb_key.currentText()
    scope_cb = self.scope_cb_key.currentText()
    owner_cb = self.owner_cb_key.currentText()
    vip_cb = self.vip_cb.currentText()
    dateedit1 = self.dateedit1_key.date().toPyDate().strftime('%Y-%m-%d')
    dateedit2 = self.dateedit2.date().toPyDate().strftime('%Y-%m-%d')
    additional_cb = self.additional_cb_key.currentText()
    request_let = self.request_let_key.text().strip()
    note_le = self.note_le_key.text().strip()

    # уже есть проверка на пустое поле -> значит точно число
    number_request = int(self.request_let_key.text().strip())
    print("► BEFORE insert")

    enter_keys(
        status_cb, nositel_type_cb, cert_serial_le, issuer_cb,
        scope_cb, owner_cb, vip_cb,
        dateedit1, dateedit2,
        additional_cb, number_request, note_le
    )
    print("◄ AFTER  insert")

    # Очищаем поля и обновляем таблицу
    clear_fields(self)
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
    """
    Заполняет динамические QComboBox-ы уникальными значениями
    из последних `limit` записей KeysTable, сохраняя порядок по убыванию ID
    и пропуская пустые поля.
    """
    try:
        con = pymysql.connect(
            host="localhost", port=3306, user="newuser", password="852456qaz",
            database="IB", charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )
        cur = con.cursor()
        cur.execute("""
            SELECT status, type, owner, scope_using, owner_fullname, additional
            FROM KeysTable
            ORDER BY ID DESC
            LIMIT %s
        """, (limit,))
        rows = cur.fetchall()
        con.close()

        # Собираем уникальные значения в порядке появления
        def unique(vals):
            seen = set()
            out = []
            for v in vals:
                if v and v not in seen:
                    seen.add(v)
                    out.append(v)
            return out

        statuses = unique(r["status"] for r in rows)
        media = unique(r["type"] for r in rows)
        ucs = unique(r["owner"] for r in rows)
        scopes = unique(r["scope_using"] for r in rows)
        owners = unique(r["owner_fullname"] for r in rows)
        additionals = unique(r["additional"] for r in rows)

        # Функция синхронизации ComboBox
        def _sync(cb: QComboBox, values: list[str]):
            if not values:
                return
            existing = [cb.itemText(i) for i in range(cb.count())]
            new_items = [v for v in values if v not in existing]
            if not new_items:
                return
            had_selection = cb.currentIndex() != -1
            cb.insertItems(0, new_items)
            if not had_selection:
                cb.setCurrentIndex(-1)
                cb.clearEditText()

        # Подтягиваем в каждый ComboBox
        _sync(self.status_cb, statuses)  # «Да/Нет»
        _sync(self.nositel_type_cb_key, media)  # «Тип носителя + серийный»
        _sync(self.issuer_cb_key, ucs)  # «УЦ»
        _sync(self.scope_cb_key, scopes)  # «Область/ЭДО»
        _sync(self.owner_cb_key, owners)  # «Владелец»
        _sync(self.additional_cb_key, additionals)  # «Дополнительно»

    except Exception as e:
        print("fill_recent_values8 error:", e)
