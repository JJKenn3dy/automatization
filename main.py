import sys
from openpyxl import Workbook
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QSizePolicy,
    QLabel, QPushButton, QStackedWidget,
    QTableWidget, QTableWidgetItem
)
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QFontDatabase
from openpyxl import Workbook, load_workbook  # Excel
from openpyxl.styles import PatternFill, Font  # Стилизация ячеек
import os  # ОС
from documents import Type1
import getpass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DOM RF")
        self.resize(800, 500)


        # 1) Создаем QStackedWidget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # 2) Создаем и добавляем страницы
        self.page1 = self.create_page1()
        self.page2 = self.create_page2()
        self.page3 = self.create_page3()
        self.page4 = self.create_page4()
        self.page5 = self.create_page5()

        self.stacked_widget.addWidget(self.page1)  # Индекс 0
        self.stacked_widget.addWidget(self.page2)  # Индекс 1
        self.stacked_widget.addWidget(self.page3)  # Индекс 2
        self.stacked_widget.addWidget(self.page4)  # Индекс 3
        self.stacked_widget.addWidget(self.page5)  # Индекс 4

        # По умолчанию показываем первую страницу
        self.stacked_widget.setCurrentIndex(0)

    def create_page1(self) -> QWidget:
        """Создаём первую страницу: текст, несколько кнопок, SVG справа."""
        page = QWidget()
        main_layout = QHBoxLayout(page)
        main_layout.setContentsMargins(50, 40, 50, 40)

        # Левая колонка (текст + несколько кнопок)
        left_layout = QVBoxLayout()

        # Текст
        text_label = QLabel(f"Добро пожаловать {getpass.getuser()}!")
        text_label.setWordWrap(True)
        text_label.setStyleSheet("font-size: 25px; color: #8BC540;")
        # Растягиваем текст по вертикали при необходимости
        text_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        left_layout.addWidget(text_label, alignment=Qt.AlignmentFlag.AlignTop)

        # Текст
        text_label = QLabel("Програма для автоматизации\nпроцессов ИБ")
        text_label.setWordWrap(True)
        text_label.setStyleSheet("font-size: 15px; color: #76787A;")
        # Растягиваем текст по вертикали при необходимости
        text_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        left_layout.addWidget(text_label, alignment=Qt.AlignmentFlag.AlignTop)

        # Добавим несколько кнопок
        btn_to_second = QPushButton(f"Лицензии")
        btn_to_second.clicked.connect(self.on_toggle)
        btn_to_second.setFixedSize(150, 50)
        btn_to_second.setStyleSheet('color: rgb(139, 197, 064);')
        btn_to_second.clicked.connect(self.go_to_second_page)
        left_layout.addWidget(btn_to_second, alignment=Qt.AlignmentFlag.AlignLeft)
        btn_to_second = QPushButton(f"СКЗИ")
        btn_to_second.clicked.connect(self.on_toggle)
        btn_to_second.setFixedSize(150, 50)
        btn_to_second.clicked.connect(self.go_to_third_page)
        btn_to_second.setStyleSheet('color: rgb(139, 197, 064);')
        left_layout.addWidget(btn_to_second, alignment=Qt.AlignmentFlag.AlignLeft)
        btn_to_second = QPushButton(f"Страница 3")
        btn_to_second.clicked.connect(self.on_toggle)
        btn_to_second.setFixedSize(150, 50)
        btn_to_second.setStyleSheet('color: rgb(139, 197, 064);')
        btn_to_second.clicked.connect(self.go_to_fourth_page)
        left_layout.addWidget(btn_to_second, alignment=Qt.AlignmentFlag.AlignLeft)
        btn_to_second = QPushButton(f"Страница 4")
        btn_to_second.clicked.connect(self.on_toggle)
        btn_to_second.setFixedSize(150, 50)
        btn_to_second.setStyleSheet('color: rgb(139, 197, 064);')
        btn_to_second.clicked.connect(self.go_to_five_page)
        left_layout.addWidget(btn_to_second, alignment=Qt.AlignmentFlag.AlignLeft)
        main_layout.addLayout(left_layout)

        # Справа – SVG
        self.svg_widget = QSvgWidget("logo.svg")
        self.svg_widget.setFixedSize(200, 200)
        self.svg_widget.setAutoFillBackground(True)
        # Обёртка для SVG
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(20, 20, 20, 20)
        container_layout.addWidget(self.svg_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(container, alignment=Qt.AlignmentFlag.AlignRight)

        return page

    def create_page2(self) -> QWidget:
        """Вторая страница с кнопкой «Назад» на первую."""
        page = QWidget()
        layout = QVBoxLayout(page)

        EXCEL_FILE = 'Журналы2.xlsx'

        # Существует ли файл Excel с данными
        if not os.path.exists(EXCEL_FILE):
            typeDoc = 1
            docs = {}
            if typeDoc == 1:
                for i in range(0, 3):
                    docs[f"document_{i}"] = getattr(Type1, f"document_{i}")

            # Если не существует — создаём новую книгу Excel
            wb = Workbook()
            ws = wb.active
            ws.title = "Данные"
            # Добавляем строку заголовков
            ws.append(["ФИО", docs["document_0"], docs["document_1"], docs["document_2"]])
            wb.save(EXCEL_FILE)

        label = QLabel("Лицензии")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        table = "Журналы2.xlsx"
        table = QTableWidget(self)  # Create a table
        table.setColumnCount(3)  # Set three columns
        table.setRowCount(1)  # and one row

        # Set the table headers
        table.setHorizontalHeaderLabels(["Header 1", "Header 2", "Header 3"])

        # Set the tooltips to headings
        table.horizontalHeaderItem(0).setToolTip("Column 1 ")
        table.horizontalHeaderItem(1).setToolTip("Column 2 ")
        table.horizontalHeaderItem(2).setToolTip("Column 3 ")

        # Set the alignment to the headers
        layout.addWidget(table)
        layout.addWidget(table, alignment=Qt.AlignmentFlag.AlignCenter)

        # Fill the first line
        table.setItem(0, 0, QTableWidgetItem("Text in column 1"))
        table.setItem(0, 1, QTableWidgetItem("Text in column 2"))
        table.setItem(0, 2, QTableWidgetItem("Text in column 3"))

        table.setMinimumSize(500, 400)

        # Do the resize of the columns by content
        table.resizeColumnsToContents()

        btn_back = QPushButton("Назад на главную.")
        btn_back.clicked.connect(self.go_to_first_page)
        layout.addWidget(label)
        layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)
        return page

    def create_page3(self) -> QWidget:
        """Третья страница"""
        page = QWidget()
        layout = QVBoxLayout(page)

        label = QLabel("СКЗИ")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_back = QPushButton("Назад на главную.")
        btn_back.clicked.connect(self.go_to_first_page)

        layout.addWidget(label)
        layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)

        return page

    def create_page4(self) -> QWidget:
        """Четвертая страница"""
        page = QWidget()
        layout = QVBoxLayout(page)

        label = QLabel("Это четвертая страница")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_back = QPushButton("Назад на главную.")
        btn_back.clicked.connect(self.go_to_first_page)

        layout.addWidget(label)
        layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)

        return page

    def create_page5(self) -> QWidget:
        """Пятая страница"""
        page = QWidget()
        layout = QVBoxLayout(page)

        label = QLabel("Это пятая страница")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_back = QPushButton("Назад на главную.")
        btn_back.clicked.connect(self.go_to_first_page)

        layout.addWidget(label)
        layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)

        return page

    def on_toggle(self):
        """Метод, который вызывается при нажатии на кнопки с первой страницы."""


    def go_to_five_page(self):
        """Переключиться на вторую страницу (индекс 4)."""
        self.stacked_widget.setCurrentIndex(4)

    def go_to_fourth_page(self):
        """Переключиться на вторую страницу (индекс 3)."""
        self.stacked_widget.setCurrentIndex(3)

    def go_to_third_page(self):
        """Переключиться на вторую страницу (индекс 2)."""
        self.stacked_widget.setCurrentIndex(2)

    def go_to_second_page(self):
        """Переключиться на вторую страницу (индекс 1)."""
        self.stacked_widget.setCurrentIndex(1)

    def go_to_first_page(self):
        """Вернуться на первую страницу (индекс 0)."""
        self.stacked_widget.setCurrentIndex(0)


def main():
    app = QApplication(sys.argv)

    # 1) Загружаем шрифт (вернётся индекс шрифта, или -1, если не удалось)
    font_id = QFontDatabase.addApplicationFont("fonts/EtelkaLightPro.ttf")
    if font_id < 0:
        print("ERROR | Не удалось загрузить шрифт.")
        print("Warned | Применяется системный шрифт.")
    else:
        # Узнаем имя семейства шрифта, чтобы применять его
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        if font_families:
            custom_font_family = font_families[0]  # Берём первое имя (иногда их может быть несколько)

            # 2) Настраиваем шрифт для всего приложения (необязательно)
            app.setFont(QFont(custom_font_family, 15))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
