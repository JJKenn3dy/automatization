import os
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QDialogButtonBox,
    QHeaderView, QVBoxLayout, QLineEdit, QInputDialog, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer, QDate
from openpyxl import Workbook, load_workbook  # Excel
from logic.database import database


def create_page2(self) -> QWidget:
    page = QWidget()
    layout = QVBoxLayout(page)

    database(self)

    # Текст
    text_label = QLabel("Програма для автоматизации\nпроцессов ИБ")
    text_label.setWordWrap(True)
    text_label.setStyleSheet("font-size: 25px; color: #76787A;")
    # Растягиваем текст по вертикали при необходимости
    text_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    layout.addWidget(text_label, alignment=Qt.AlignmentFlag.AlignTop)

    btn_input = QPushButton("Лицензии")
    btn_input.clicked.connect(self.go_to_six_page)
    layout.addWidget(btn_input)
    btn_input.setFixedSize(150, 50)
    btn_input.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    layout.addWidget(btn_input, alignment=Qt.AlignmentFlag.AlignCenter)

    btn_input2 = QPushButton("СКЗИ")
    btn_input2.clicked.connect(self.go_to_seven_page)
    layout.addWidget(btn_input2)
    btn_input2.setFixedSize(150, 50)
    btn_input2.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    layout.addWidget(btn_input2, alignment=Qt.AlignmentFlag.AlignCenter)

    btn_input3 = QPushButton("Ключи УКЭП")
    btn_input3.clicked.connect(self.go_to_eight_page)
    layout.addWidget(btn_input3)
    btn_input3.setFixedSize(150, 50)
    btn_input3.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    layout.addWidget(btn_input3, alignment=Qt.AlignmentFlag.AlignCenter)

    btn_input4 = QPushButton("КБР")
    btn_input4.clicked.connect(self.go_to_nine_page)
    layout.addWidget(btn_input4)
    btn_input4.setFixedSize(150, 50)
    btn_input4.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    layout.addWidget(btn_input4, alignment=Qt.AlignmentFlag.AlignCenter)

    btn_input5 = QPushButton("TLS")
    btn_input5.clicked.connect(self.go_to_ten_page)
    layout.addWidget(btn_input5)
    btn_input5.setFixedSize(150, 50)
    btn_input5.setStyleSheet('font-size: 15px; color: rgb(98, 150, 30);')
    layout.addWidget(btn_input5, alignment=Qt.AlignmentFlag.AlignCenter)

    btn_back = QPushButton("Назад")
    btn_back.clicked.connect(self.go_to_first_page)

    layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignLeft)


    return page


"""    if os.path.exists('Журналы.xlsx'):
        wb = load_workbook('Журналы.xlsx')
        ws = wb.active
        data = []

        # Считываем данные, принудительно задавая диапазон до 9 столбцов
        for row in ws.iter_rows(min_row=1, max_col=9, values_only=True):
            data.append(list(row))

        if data:
            headers = data[0]
            # Если заголовков меньше 9, дополняем пустыми строками
            if len(headers) < 9:
                headers += [""] * (9 - len(headers))
            rows = data[1:]

            table = QTableWidget()
            table.setColumnCount(9)  # Жестко задаем 9 столбцов
            table.setRowCount(len(rows))
            table.setHorizontalHeaderLabels(
                [str(header) if header is not None else "" for header in headers]
            )

            for row_index, row in enumerate(rows):
                # Если в строке меньше 5 ячеек, дополняем до 5 элементов
                if len(row) < 4:
                    row += [None] * (4 - len(row))
                for col_index, cell in enumerate(row):
                    item = QTableWidgetItem(str(cell) if cell is not None else "")
                    table.setItem(row_index, col_index, item)

            # Растягиваем столбцы, чтобы все 5 были видны равномерно
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            table.setMinimumSize(1200, 500)
            layout.addWidget(table, alignment=Qt.AlignmentFlag.AlignCenter)
    else:
        label = QLabel("Документ не был найден. Выбрать файл?")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox, alignment=Qt.AlignmentFlag.AlignCenter)"""