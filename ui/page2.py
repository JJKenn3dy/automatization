import os
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QDialogButtonBox,
    QHeaderView, QVBoxLayout, QLineEdit, QInputDialog
)
from PyQt6.QtCore import Qt, QTimer, QDate
from openpyxl import Workbook, load_workbook  # Excel
from logic.database import database


def create_page2(self) -> QWidget:
    page = QWidget()
    layout = QVBoxLayout(page)

    database(self)

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