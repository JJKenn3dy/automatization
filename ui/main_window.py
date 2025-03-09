from datetime import datetime

import mariadb
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
from ui.page6 import create_page6
from ui.page7 import create_page7
from ui.page8 import create_page8
from ui.page9 import create_page9
from ui.page10 import create_page10
from logic.file_manager import fileManager
from logic.db import enter_fio, create_tables
from logic.db import enter_variant
from logic.readwritepdf import pdf_check
from logic.db import enter_license

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

        # По умолчанию показываем первую страницу
        self.stacked_widget.setCurrentIndex(0)

    create_tables()

    def save_values8(self):
        status_cb = self.status_cb.currentText()
        nositel_type_cb = self.nositel_type_cb.currentText()
        serial_le = self.serial_le.text()
        cert_serial_le = self.cert_serial_le.text()
        issuer_cb = self.issuer_cb.currentText()
        scope_cb = self.scope_cb.currentText()
        owner_cb = self.owner_cb.currentText()
        vip_cb = self.vip_cb.currentText()
        dateedit1 = self.dateedit1.date()
        dateedit2 = self.dateedit2.date()
        additional_cb = self.additional_cb.currentText()
        request_let = self.request_let.text()
        note_le = self.note_le.text()

        # Преобразуем в строку в формате "день.месяц.год"
        date_str = dateedit1.toString("dd.MM.yyyy")
        dateedit2 = dateedit2.toString("dd.MM.yyyy")


        # Можно собрать значения в словарь для дальнейшей обработки
        data = {
            "status_cb": status_cb,
            "nositel_type_cb": nositel_type_cb,
            "serial_le": serial_le,
            "cert_serial_le": cert_serial_le,
            "issuer_cb": issuer_cb,
            "scope_cb": scope_cb,
            "owner_cb": owner_cb,
            "dateedit1": date_str,
            "dateedit2": vip_cb,
            "additional_cb": additional_cb,
            "request_let": request_let,
            "note_le": note_le,

        }
        print("Сохранённые данные:", data)
        # Здесь можно добавить дополнительную логику для работы с данными

    def save_values7(self):
        skzi_value = self.skzi_name_cb.currentText()
        skzi_type = self.skzi_type.currentText()
        skzi_version = self.skzi_version_cb.currentText()
        current_date = self.dateedit.date()
        doc_info_le = self.doc_info_le.text()
        owner_fio_le = self.owner_fio_le.text()
        reg_number_le = self.reg_number_le.text()
        from_whom_cb = self.from_whom_cb.currentText()
        note_cb = self.note_cb.currentText()
        additional_le = self.additional_le.text()
        certnum_le = self.certnum_le.text()
        dateedit2 = self.dateedit2.date()
        # Преобразуем в строку в формате "день.месяц.год"
        date_str = current_date.toString("dd.MM.yyyy")
        dateedit2 = current_date.toString("dd.MM.yyyy")


        # Можно собрать значения в словарь для дальнейшей обработки
        data = {
            "skzi_name": skzi_value,
            "skzi_type": skzi_type,
            "skzi_version": skzi_version,
            "date": date_str,
            "doc_info_le": doc_info_le,
            "owner_fio_le": owner_fio_le,
            "reg_number_le": reg_number_le,
            "from_whom_cb": from_whom_cb,
            "note_cb": note_cb,
            "additional_le": additional_le,
            "certnum_le": certnum_le,
            "dateedit2": dateedit2,
        }
        print("Сохранённые данные:", data)
        # Здесь можно добавить дополнительную логику для работы с данными


    def pdf_check(self):
        pdf_check(self)

    def getandgo(self):
        text = self.input_field.text()
        enter_fio(text)
        self.go_to_license_2()

    def getandgo2(self):
        checked_button = self.radio_group.checkedButton()
        if not checked_button:
            QMessageBox.warning(self, "Ошибка", "Вы не выбрали вариант!")
            return
        self.selected_option = checked_button.text()
        try:
            variant = int(self.selected_option[0])
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Неверный формат выбранного варианта!")
            return
        enter_variant(variant)
        self.go_to_license_3()

    def on_radio_selected(self):
        sender = self.sender()
        if sender.isChecked():
            self.temp_selection = sender.text()

        """Вызывается при выборе варианта, но не сохраняет окончательный выбор"""
        """sender = self.sender()
        if sender.isChecked():
            self.temp_selection = sender.text()"""

    def update_extra_fields_visibility(self):
        """
        Если нажата радиокнопка "Изьято", то показываем блок
        'Дополнительные сведения'. Иначе скрываем.
        """
        self.extra_group.setVisible(self.rb_taken.isChecked())

    def save_selection(self):
        """Сохраняет окончательный выбор только при нажатии OK"""
        if hasattr(self, 'temp_selection'):
            self.selected_option = self.temp_selection
            try:
                variant = int(self.selected_option[0])
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Неверный формат варианта!")
                return False
            enter_variant(variant)
            return True
        else:
            QMessageBox.warning(self, "Ошибка", "Вы не выбрали вариант!")
            return False

    def showDate(self, date: QDate):
        """Обновляем метку выбранной даты."""
        self.cal_label.setText(date.toString())

    def on_toggle(self):
        """Метод, который вызывается при нажатии на кнопки с первой страницы."""

    def create_page11(self):
        """Переключиться на 10 страницу (индекс 12)."""
        self.stacked_widget.setCurrentIndex(12)

    def go_to_license_3(self):
        """Переключиться на 10 страницу (индекс 11)."""
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

    def get_license_key(self):

            conn = mariadb.connect(
                host="localhost",
                port=3306,
                user="newuser",
                password="852456qaz",
                database="IB",
                autocommit=True
            )
            cur = conn.cursor()
            # Предполагаем, что в таблице License есть столбцы number (ключ) и status (0 - свободен, 1 - занят)
            cur.execute("SELECT number FROM keying WHERE status IS NULL OR status = ''")
            result = cur.fetchone()
            if result is None:
                key_value = None
            else:
                key_value = result[0]
                insert_query = f"UPDATE keying SET status = 1 WHERE number = (?)"
                cur.execute(insert_query, result)

            return key_value



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






