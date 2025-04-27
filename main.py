# main.py
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui     import QFontDatabase, QFont

def main() -> None:
    app = QApplication(sys.argv)

    # ▸ подключаем Gilroy (если нужен) и антиалиас
    if QFontDatabase.addApplicationFont("ui/fonts/Gilroy-Medium.ttf") != -1:
        f = QFont("Gilroy", 10)
        f.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        app.setFont(f)

    from ui.main_window import MainWindow
    win = MainWindow()
    win.resize(1500, 900)
    win.setMinimumSize(1280, 800)
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
