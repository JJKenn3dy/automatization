# ui/page1.py

import os, sys, getpass
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QSizePolicy, QGraphicsDropShadowEffect, QSpacerItem, QPushButton
)
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtGui import QColor, QFontDatabase, QFont
from PyQt6.QtCore import (
    Qt, QPropertyAnimation, QEasingCurve, QRect
)


# ────────────────────────────────────────────────────────────────────────
# HoverButton с анимацией при enter/leave и press/release
# ────────────────────────────────────────────────────────────────────────
class HoverButton(QFrame):
    def __init__(self, txt, parent=None):
        super().__init__(parent)
        self.btn = QPushButton(txt, self)
        self.btn.setObjectName("animBtn")
        self.btn.pressed.connect(self._onPress)
        self.btn.released.connect(self._onRelease)

        # анимируем геометрию самого QFrame
        self._anim = QPropertyAnimation(self, b"geometry", self)
        self._anim.setDuration(120)
        # ← здесь поправлено
        self._anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        self._origGeom = None

    def resizeEvent(self, e):
        self.btn.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(e)

    def enterEvent(self, e):
        if self._anim.state():
            self._anim.stop()
        if self._origGeom is None:
            self._origGeom = self.geometry()
        target = self._origGeom.adjusted(-3, -3, 3, 3)
        self._anim.setStartValue(self.geometry())
        self._anim.setEndValue(target)
        self._anim.start()
        super().enterEvent(e)

    def leaveEvent(self, e):
        if self._anim.state():
            self._anim.stop()
        if self._origGeom:
            self._anim.setStartValue(self.geometry())
            self._anim.setEndValue(self._origGeom)
            self._anim.start()
        super().leaveEvent(e)

    def _onPress(self):
        if self._anim.state():
            self._anim.stop()
        r = self.geometry()
        target = r.adjusted(2, 2, -2, -2)
        self._anim.setStartValue(r)
        self._anim.setEndValue(target)
        self._anim.start()

    def _onRelease(self):
        if self._anim.state():
            self._anim.stop()
        cur = self.geometry()
        dest = (self._origGeom.adjusted(-3, -3, 3, 3)
                if self.underMouse() else self._origGeom)
        self._anim.setStartValue(cur)
        self._anim.setEndValue(dest)
        self._anim.start()

# ────────────────────────────────────────────────────────────────────────
def load_gilroy() -> tuple[str,str]:
    base = Path(__file__).resolve().parent.parent
    fonts = base / "fonts"
    if not fonts.is_dir():
        return QApplication.font().family(), ""
    for f in fonts.glob("Gilroy*-Medium.ttf"):
        fid = QFontDatabase.addApplicationFont(str(f))
        fams = QFontDatabase.applicationFontFamilies(fid)
        if fams:
            family = fams[0]
            styles = QFontDatabase.styles(family)
            style = next((s for s in styles if s.lower()=="medium"), styles[0])
            return family, style
    return QApplication.font().family(), ""


# ────────────────────────────────────────────────────────────────────────
# Палитра и размеры
# ────────────────────────────────────────────────────────────────────────
BG             = "#2F444E"
ACCENT         = "#8BC540"
TXT_DARK       = "#263B48"
BTN_BG         = "#263B48"

CARD_W, CARD_H = 1420, 420    # шире и выше
CARD_R         = 20
PAD_H, PAD_V   = 64, 56       # чуть просторнее

LEFT_W         = 600
BTN_H, BTN_R   = 60, 10

BAR_W          = 6
LOGO_W, LOGO_H = 220, 260

SZ_WEL       = 28
SZ_TITLE     = 18
SZ_BTN       = 18
SZ_BANK      = 34


def create_page1(self) -> QWidget:
    family, style = load_gilroy()

    # шрифты
    f_wel   = QFontDatabase.font(family, style, SZ_WEL)
    f_title = QFontDatabase.font(family, style, SZ_TITLE)
    f_bank  = QFontDatabase.font(family, style, SZ_BANK)

    # общий стиль для кнопок
    # общий стиль для кнопок
    btn_css = f"""
        QPushButton#animBtn {{
            background:{BTN_BG};
            color:#ffffff;
            border:none;
            border-radius:{BTN_R}px;
            font:{SZ_BTN}px "{family}";
        }}
        /* при наведении чуть тёмнее фон, и сероватый текст */
        QPushButton#animBtn:hover {{
            background: #1f2d36;    /* ~90% от #263B48 */
            color: #e0e0e0;         /* чуть не чисто-белый */
        }}
        /* при зажатии можно чуть сильнее потемнить */
        QPushButton#animBtn:pressed {{
            background: #19242b;    /* ещё темнее */
            color: #d0d0d0;
        }}
    """

    # главная страница
    page = QWidget()
    page.setStyleSheet(f"background:{BG};")
    root = QVBoxLayout(page)
    root.setContentsMargins(40, 30, 40, 30)
    root.setSpacing(0)

    # приветствие
    user = getpass.getuser()
    lbl = QLabel(f"Добро пожаловать, <span style='color:{ACCENT};'>{user}!</span>")
    lbl.setFont(f_wel)
    lbl.setStyleSheet(f"color:#fff; border-bottom:3px solid {ACCENT}; padding-bottom:4px;")
    root.addWidget(lbl, alignment=Qt.AlignmentFlag.AlignLeft)
    root.addSpacerItem(QSpacerItem(0, 36, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))

    # центрировка
    root.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding))

    # белая карточка
    card = QFrame()
    card.setFixedSize(CARD_W, CARD_H)
    card.setStyleSheet(f"background:#fff; border-radius:{CARD_R}px;")
    sh = QGraphicsDropShadowEffect(blurRadius=28, xOffset=0, yOffset=4, color=QColor(0,0,0,40))
    card.setGraphicsEffect(sh)
    root.addWidget(card, alignment=Qt.AlignmentFlag.AlignHCenter)
    root.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding))

    # контент карточки
    hl = QHBoxLayout(card)
    hl.setContentsMargins(PAD_H, PAD_V, PAD_H, PAD_V)
    hl.setSpacing(64)

    # левая колонка
    left = QVBoxLayout(); left.setSpacing(28)
    t = QLabel("Программа автоматизации процессов\nИнформационной Безопасности")
    t.setFont(f_title); t.setWordWrap(True); t.setFixedWidth(LEFT_W)
    t.setStyleSheet(f"color:{TXT_DARK};")
    left.addWidget(t)
    hr = QFrame(); hr.setFixedHeight(3); hr.setFixedWidth(LEFT_W)
    hr.setStyleSheet(f"background:{ACCENT}; border:none;")
    left.addWidget(hr)

    # кнопки как HoverButton
    for text, slot in [
        ("Регистрация заявок", self.go_to_second_page),
        ("Импорт базы",        self.go_to_11_page)
    ]:
        wrapper = HoverButton(text)
        wrapper.setFixedHeight(BTN_H)
        wrapper.setStyleSheet(btn_css)
        wrapper.btn.clicked.connect(self.on_toggle)
        wrapper.btn.clicked.connect(slot)
        left.addWidget(wrapper)

    left.addStretch(1)
    hl.addLayout(left, 1)

    # правая колонка
    right = QHBoxLayout(); right.setSpacing(30)
    logo = QSvgWidget("logo.svg"); logo.setFixedSize(LOGO_W, LOGO_H)
    right.addWidget(logo)
    vb = QFrame(); vb.setFixedWidth(BAR_W)
    vb.setStyleSheet(f"background:{ACCENT}; border:none;")
    right.addWidget(vb)
    bank = QLabel("БАНК"); bank.setFont(f_bank)
    bank.setStyleSheet(f"color:{TXT_DARK};")
    right.addWidget(bank)
    hl.addLayout(right, 0)

    return page
