# ui/page11.py
from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QSizePolicy, QGraphicsDropShadowEffect, QSpacerItem
)
from PyQt6.QtGui import QColor, QFontDatabase, QFont, QShortcut, QKeySequence
from PyQt6.QtCore import Qt

# всё готовое берём из page1
from ui.page1 import (
    HoverButton, load_gilroy,
    BG, ACCENT, TXT_DARK, BTN_BG,
    CARD_W, CARD_H, CARD_R, PAD_H, PAD_V,
    BTN_H, BTN_R, SZ_TITLE, SZ_BTN
)


# ────────────────────────────────────────────────────────────────────────
def create_page11(self) -> QWidget:
    """
    Страница импорта Excel-данных, стилизованная в едином ключе с page1.
    Предполагается, что у self уже есть методы:
        • go_to_first_page()
        • upload_file()
        • on_toggle() – тот же, что и на page1 (для анимации кнопок)
    """

    # шрифты
    family, style = load_gilroy()
    f_header = QFontDatabase.font(family, style, SZ_TITLE)
    f_btn    = QFontDatabase.font(family, style, SZ_BTN)

    # общий CSS для анимированных кнопок HoverButton
    btn_css = f"""
        QPushButton#animBtn {{
            background:{BTN_BG};
            color:#ffffff;
            border:none;
            border-radius:{BTN_R}px;
            font:{SZ_BTN}px "{family}";
        }}
        QPushButton#animBtn:hover {{
            background:#1f2d36;
            color:#e0e0e0;
        }}
        QPushButton#animBtn:pressed {{
            background:#19242b;
            color:#d0d0d0;
        }}
    """

    # ── корневой виджет ───────────────────────────────────────────────
    page = QWidget()
    page.setStyleSheet(f"background:{BG};")

    root = QVBoxLayout(page)
    root.setContentsMargins(40, 30, 40, 30)
    root.setSpacing(0)
    # ← Esc → назад

    shortcut = QShortcut(QKeySequence(Qt.Key.Key_Escape), page)
    shortcut.activated.connect(self.go_to_first_page)

    # ── верхняя панель: «Назад» ───────────────────────────────────────
    back = HoverButton("←  На главную")
    back.setFixedHeight(BTN_H)
    back.setStyleSheet(btn_css)
    back.btn.clicked.connect(self.on_toggle)
    back.btn.clicked.connect(self.go_to_first_page)
    root.addWidget(back, alignment=Qt.AlignmentFlag.AlignLeft)

    root.addSpacerItem(QSpacerItem(0, 36,
        QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))

    # ── центрирование по вертикали ────────────────────────────────────
    root.addSpacerItem(QSpacerItem(0, 0,
        QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding))

    # ── «карточка» – белый блок с тенью ───────────────────────────────
    card = QFrame()
    card.setFixedSize(CARD_W, CARD_H)
    card.setStyleSheet(f"background:#ffffff; border-radius:{CARD_R}px;")
    sh = QGraphicsDropShadowEffect(
        blurRadius=28, xOffset=0, yOffset=4, color=QColor(0, 0, 0, 40))
    card.setGraphicsEffect(sh)
    root.addWidget(card, alignment=Qt.AlignmentFlag.AlignHCenter)

    # нижний «пружинный» отступ
    root.addSpacerItem(QSpacerItem(0, 0,
        QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding))

    # ── содержимое карточки ───────────────────────────────────────────
    hl = QVBoxLayout(card)
    hl.setContentsMargins(PAD_H, PAD_V, PAD_H, PAD_V)
    hl.setSpacing(32)

    # Заголовок
    header = QLabel("Импорт Excel-файла")
    header.setFont(f_header)
    header.setStyleSheet(f"color:{TXT_DARK};")
    header.setAlignment(Qt.AlignmentFlag.AlignCenter)
    hl.addWidget(header)

    # Горизонтальный разделитель-линия (акцентный цвет)
    hr = QFrame()
    hr.setFixedHeight(3)
    hr.setStyleSheet(f"background:{ACCENT}; border:none;")
    hl.addWidget(hr)

    # Кнопка импорта
    upload = HoverButton("Выбрать файл и импортировать")
    upload.setFixedSize(340, BTN_H)
    upload.setStyleSheet(btn_css)
    upload.btn.clicked.connect(self.on_toggle)
    upload.btn.clicked.connect(self.upload_file)
    hl.addWidget(upload, alignment=Qt.AlignmentFlag.AlignHCenter)

    # Подпись-подсказка
    tip = QLabel("Поддерживаются таблицы Excel (.xlsx, .xls). "
                 "После выбора файл будет загружен в БД.")
    tip.setWordWrap(True)
    tip.setStyleSheet(f"color:{TXT_DARK};")
    tip.setAlignment(Qt.AlignmentFlag.AlignCenter)
    hl.addWidget(tip)

    hl.addStretch(1)        # «прижимаем» содержимое вверх

    return page
