import sys
import os
import getpass
import PyQt6
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QSizePolicy,
    QLabel, QPushButton, QStackedWidget,
    QTableWidget, QTableWidgetItem, QSystemTrayIcon, QStyle, QDialog, QDialogButtonBox,
    QHeaderView, QFileDialog, QCalendarWidget, QVBoxLayout
)
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtCore import Qt, QTimer, QDate
from PyQt6.QtGui import QFont, QFontDatabase, QIcon
from openpyxl import Workbook, load_workbook  # Excel
from openpyxl.styles import PatternFill, Font  # Стилизация ячеек
from documents import Type1
import subprocess
from PyQt6 import QtWidgets

from ui.page1 import create_page1
from ui.page2 import create_page2
from ui.page3 import create_page3
from ui.page4 import create_page4
from ui.page5 import create_page5
from logic.file_manager import fileManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DOM RF")
        self.resize(1400, 800)

        # 1) Создаем QStackedWidget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # 2) Создаем и добавляем страницы
        self.page1 = create_page1(self)
        self.page2 = create_page2(self)
        self.page3 = create_page3(self)
        self.page4 = create_page4(self)
        self.page5 = create_page5(self)

        self.stacked_widget.addWidget(self.page1)  # Индекс 0
        self.stacked_widget.addWidget(self.page2)  # Индекс 1
        self.stacked_widget.addWidget(self.page3)  # Индекс 2
        self.stacked_widget.addWidget(self.page4)  # Индекс 3
        self.stacked_widget.addWidget(self.page5)  # Индекс 4

        # По умолчанию показываем первую страницу
        self.stacked_widget.setCurrentIndex(0)

    def showDate(self, date: QDate):
        """Обновляем метку выбранной даты."""
        self.cal_label.setText(date.toString())

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

    def accept(self):
        fileManager()

    def showDate(self, date):
        self.lbl.setText(date.toString())

    def _on_double_clicked(self, index):
        file_name = self.model.filePath(index)
        with open(file_name, encoding='utf-8') as f:
            text = f.read()
            self.textEdit.setPlainText(text)

    def reject(self):
        self.stacked_widget.setCurrentIndex(0)
