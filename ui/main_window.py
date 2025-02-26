
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QSizePolicy,
    QLabel, QPushButton, QStackedWidget,
    QInputDialog, QMessageBox
)
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtCore import Qt, QTimer, QDate
from PyQt6.QtGui import QFont, QFontDatabase, QIcon

import subprocess
from PyQt6 import QtWidgets
import sqlite3
from ui.page1 import create_page1
from ui.page2 import create_page2
from ui.page3 import create_page3
from ui.page4 import create_page4
from ui.page5 import create_page5
from ui.page6 import create_page6, license3
from ui.page7 import create_page7
from ui.page8 import create_page8
from ui.page9 import create_page9
from ui.page10 import create_page10
from ui.page6 import license2
from logic.file_manager import fileManager
from logic.db import enter_fio
from logic.db import enter_variant
from logic.readwritepdf import pdf_check


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
        self.page6 = create_page6(self)
        self.page7 = create_page7(self)
        self.page8 = create_page8(self)
        self.page9 = create_page9(self)
        self.page10 = create_page10(self)
        self.license2 = license2(self)
        self.license3 = license3(self)

        self.stacked_widget.addWidget(self.page1)  # Индекс 0
        self.stacked_widget.addWidget(self.page2)  # Индекс 1
        self.stacked_widget.addWidget(self.page3)  # Индекс 2
        self.stacked_widget.addWidget(self.page4)  # Индекс 3
        self.stacked_widget.addWidget(self.page5)  # Индекс 4
        self.stacked_widget.addWidget(self.page6)  # Индекс 5
        self.stacked_widget.addWidget(self.page7)  # Индекс 6
        self.stacked_widget.addWidget(self.page8)  # Индекс 7
        self.stacked_widget.addWidget(self.page9)  # Индекс 8
        self.stacked_widget.addWidget(self.page10)  # Индекс 9
        self.stacked_widget.addWidget(self.license2)  # Индекс 10
        self.stacked_widget.addWidget(self.license3)  # Индекс 11

        # По умолчанию показываем первую страницу
        self.stacked_widget.setCurrentIndex(0)

    def pdf_check(self):
        pdf_check(self)

    def getandgo(self):
        text = self.get_text()
        self.go_to_license_2()

    def getandgo2(self):
        self.on_radio_selected()
        self.save_selection()
        self.go_to_license_3()

    def on_radio_selected(self):
        """Вызывается при выборе варианта, но не сохраняет окончательный выбор"""
        sender = self.sender()
        if sender.isChecked():
            self.temp_selection = sender.text()

    def save_selection(self):
        """Сохраняет окончательный выбор только при нажатии OK"""
        if hasattr(self, 'temp_selection'):
            self.selected_option = self.temp_selection
            variant = int(self.selected_option[0])
            enter_variant(variant)
        else:
            QMessageBox.warning(self, "Ошибка", "Вы не выбрали вариант!")

    def showDate(self, date: QDate):
        """Обновляем метку выбранной даты."""
        self.cal_label.setText(date.toString())

    def on_toggle(self):
        """Метод, который вызывается при нажатии на кнопки с первой страницы."""

    def go_to_license_3(self):
        """Переключиться на 10 страницу (индекс 10)."""
        self.stacked_widget.setCurrentIndex(11)

    def go_to_license_2(self):
        """Переключиться на 10 страницу (индекс 10)."""
        self.stacked_widget.setCurrentIndex(10)

    def go_to_ten_page(self):
        """Переключиться на 10 страницу (индекс 9)."""
        self.stacked_widget.setCurrentIndex(9)

    def go_to_nine_page(self):
        """Переключиться на 9 страницу (индекс 8)."""
        self.stacked_widget.setCurrentIndex(8)

    def go_to_eight_page(self):
        """Переключиться на 8 страницу (индекс 7)."""
        self.stacked_widget.setCurrentIndex(7)

    def go_to_seven_page(self):
        """Переключиться на 7 страницу (индекс 6)."""
        self.stacked_widget.setCurrentIndex(6)

    def go_to_six_page(self):
        """Переключиться на 6 страницу (индекс 5)."""
        self.stacked_widget.setCurrentIndex(5)

    def go_to_five_page(self):
        """Переключиться на 5 страницу (индекс 4)."""
        self.stacked_widget.setCurrentIndex(4)

    def go_to_fourth_page(self):
        """Переключиться на 4 страницу (индекс 3)."""
        self.stacked_widget.setCurrentIndex(3)

    def go_to_third_page(self):
        """Переключиться на 3 страницу (индекс 2)."""
        self.stacked_widget.setCurrentIndex(2)

    def go_to_second_page(self):
        """Переключиться на 2 страницу (индекс 1)."""
        self.stacked_widget.setCurrentIndex(1)

    def go_to_first_page(self):
        """Вернуться на 1 страницу (индекс 0)."""
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

    def show_name_dialog(self):
        """Показывает диалог ввода имени по требованию пользователя"""
        name, done = QInputDialog.getText(
            self,
            'Input Dialog',
            'Enter your name:'
        )
        if done and name:
            # Сохраняем или обрабатываем имя
            print(f"Введенное имя: {name}")

    def get_text(self):
        text = self.input_field.text()
        enter_fio(text)


