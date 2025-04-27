# ui/page2.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QSizePolicy,
    QSpacerItem, QGraphicsDropShadowEffect
)
from PyQt6.QtGui import (
    QColor, QFontDatabase, QKeySequence, QShortcut
)
from PyQt6.QtCore import Qt

from ui.page1 import (
    load_gilroy, HoverButton,
    BG, ACCENT, TXT_DARK,
    CARD_R, PAD_H, PAD_V,
    BTN_H, BTN_R
)

#───────────────────────────────────────────────────────────────────────────────
def _hline(color: str, thickness: int = 2) -> QFrame:
    ln = QFrame()
    ln.setFixedHeight(thickness)
    ln.setStyleSheet(f'background:{color}; border:none;')
    return ln


def _dark_btn(text: str, font, slot):
    """Готовая тёмная кнопка (HoverButton)."""
    hb = HoverButton(text)
    hb.btn.setFont(font)
    hb.setFixedHeight(BTN_H)
    hb.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    hb.btn.setStyleSheet(
        f"QPushButton{{background:{BG};color:#fff;border:none;"
        f"border-radius:{BTN_R}px;}}"
        f"QPushButton:hover{{background:{ACCENT};}}"
    )
    hb.btn.clicked.connect(slot)
    return hb


#───────────────────────────────────────────────────────────────────────────────
def create_page2(self) -> QWidget:
    # ▸ шрифты
    family, style = load_gilroy()
    font_h1  = QFontDatabase.font(family, style, 28)
    font_h2  = QFontDatabase.font(family, style, 26)
    font_btn = QFontDatabase.font(family, style, 18)

    # ▸ корень
    page = QWidget()
    page.setStyleSheet(f'background:{BG};')
    root = QVBoxLayout(page)
    root.setContentsMargins(40, 30, 40, 30)
    root.setSpacing(0)

    # esc → назад
    QShortcut(QKeySequence('Escape'), page).activated.connect(self.go_to_first_page)

    # ▸ заголовок приложения
    hdr_app = QLabel("Регистрация заявок")
    hdr_app.setFont(font_h1)
    hdr_app.setStyleSheet(f"color:#fff;border-bottom:3px solid {ACCENT};padding-bottom:4px;")
    root.addWidget(hdr_app, alignment=Qt.AlignmentFlag.AlignLeft)
    root.addSpacerItem(QSpacerItem(0, 36,
        QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))

    # верхний stretch
    root.addSpacerItem(QSpacerItem(0, 0,
        QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding))

    # ▸ карточка
    card = QFrame()
    card.setFixedSize(1280, 580)
    card.setStyleSheet(f'background:#fff;border-radius:{CARD_R}px;')
    card.setGraphicsEffect(QGraphicsDropShadowEffect(
        blurRadius=34, xOffset=0, yOffset=5, color=QColor(0, 0, 0, 55)
    ))
    root.addWidget(card, alignment=Qt.AlignmentFlag.AlignHCenter)
    root.addSpacerItem(QSpacerItem(0, 0,
        QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding))

    # ▸ grid-layout внутри карточки
    g = QGridLayout(card)
    g.setContentsMargins(PAD_H, PAD_V, PAD_H, PAD_V)
    g.setHorizontalSpacing(90)
    g.setVerticalSpacing(40)          # чуть плотнее, чем раньше
    g.setColumnStretch(0, 1)
    g.setColumnStretch(1, 1)

    # ── header (стрелка + текст) ─────────────────────────────────────────
    header_w = QWidget()
    hh = QHBoxLayout(header_w)
    hh.setContentsMargins(0, 0, 0, 0)
    hh.setSpacing(12)

    back = QPushButton("←")
    back.setCursor(Qt.CursorShape.PointingHandCursor)
    back.setFont(font_h1)
    back.setFixedSize(30, 30)
    back.setStyleSheet(f'color:{TXT_DARK};background:none;border:none;')
    back.clicked.connect(self.go_to_first_page)

    hdr_txt = QLabel("Выберите, что зарегистрировать")
    hdr_txt.setFont(font_h1)
    hdr_txt.setStyleSheet(f'color:{TXT_DARK};')

    hh.addWidget(back, alignment=Qt.AlignmentFlag.AlignVCenter)
    hh.addWidget(hdr_txt, alignment=Qt.AlignmentFlag.AlignVCenter)
    hh.addStretch()

    g.addWidget(header_w, 0, 0, 1, 2)
    g.addWidget(_hline(ACCENT, 2), 1, 0, 1, 2)

    # ── Группа 1 ─────────────────────────────────────────────────────────
    g1 = QLabel("Группа 1")
    g1.setFont(font_h2)
    g1.setStyleSheet(f'color:{TXT_DARK};')
    g.addWidget(g1, 2, 0, alignment=Qt.AlignmentFlag.AlignLeft)

    g.addWidget(_dark_btn("Лицензии", font_btn, self.go_to_six_page), 3, 0)
    g.addWidget(_dark_btn("СКЗИ",      font_btn, self.go_to_seven_page), 4, 0)

    # ── Группа 2 ─────────────────────────────────────────────────────────
    g2 = QLabel("Группа 2")
    g2.setFont(font_h2)
    g2.setStyleSheet(f'color:{TXT_DARK};')
    g.addWidget(g2, 2, 1, alignment=Qt.AlignmentFlag.AlignLeft)

    g.addWidget(_dark_btn("Ключи УКЭП", font_btn, self.go_to_eight_page), 3, 1)
    g.addWidget(_dark_btn("КБР",        font_btn, self.go_to_nine_page),   4, 1)

    # ── Группа 3 ─────────────────────────────────────────────────────────
    g3 = QLabel("Группа 3")
    g3.setFont(font_h2)
    g3.setStyleSheet(f'color:{TXT_DARK};')
    g.addWidget(g3, 5, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft)

    g.addWidget(
        _dark_btn("TLS", font_btn, self.go_to_ten_page),
        6, 0, 1, 2
    )

    return page
