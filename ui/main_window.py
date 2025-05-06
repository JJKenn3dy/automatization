import os
from datetime import datetime

import mariadb
import pandas as pd
import pymysql
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QSizePolicy,
    QLabel, QPushButton, QStackedWidget,
    QInputDialog, QMessageBox, QFileDialog, QDialog, QComboBox
)
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtCore import Qt, QTimer, QDate, QEvent
from PyQt6.QtGui import QFont, QFontDatabase, QIcon, QPalette, QColor
import re
import subprocess
from PyQt6 import QtWidgets
from PyQt6.QtGui import QShortcut, QKeySequence

from ui.page1 import create_page1
from ui.page2 import create_page2
from ui.page3 import create_page3
from ui.page4 import create_page4
from ui.page5 import create_page5
from ui.page6 import create_page6, on_row_double_clicked
from ui.page7 import create_page7
from ui.page8 import create_page8
from ui.page9 import create_page9
from ui.page10 import create_page10
from ui.page11 import create_page11
from logic.file_manager import fileManager
from logic.db import create_tables
from logic.readwritepdf import pdf_check
import sys, os


class MainWindow(QMainWindow):
    def __init__(self):

        super().__init__()
        self.setWindowTitle("DOM RF")
        self.resize(1500, 900)  # стартовые размеры
        self.setMinimumSize(1280, 800)

        # «полноэкран» по F11
        QShortcut(QKeySequence("F11"), self,
                  activated=lambda: self.showNormal() if self.isMaximized() else self.showMaximized())

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
        self.page11 = create_page11(self)

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
        self.stacked_widget.addWidget(self.page11)  # Индекс 10

        # По умолчанию показываем первую страницу
        self.stacked_widget.setCurrentIndex(0)

    create_tables()

    def pdf_check(self):
        pdf_check(self)

    def on_radio_selected(self):
        sender = self.sender()
        if sender.isChecked():
            self.temp_selection = sender.text()

        """Вызывается при выборе варианта, но не сохраняет окончательный выбор"""
        """sender = self.sender()
        if sender.isChecked():
            self.temp_selection = sender.text()"""



    def eventFilter(self, source, event):
        # Ждём именно двойного клика на viewport таблицы
        if source is self.table_widget.viewport() and event.type() == QEvent.Type.MouseButtonDblClick:
            # Правая кнопка → дублируем в поля
            if event.button() == Qt.MouseButton.RightButton:
                pos = event.position().toPoint()
                item = self.table_widget.itemAt(pos)
                if item:
                    on_row_double_clicked(self, item)
                return True  # событие обработано
            # Левая кнопка → возвращаем False, чтобы продолжилось обычное редактирование
            return False
        # Всё остальное — стандартная обработка
        return super().eventFilter(source, event)

    def export_all_sczy(self):
        # Диалог сохранения
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить все данные СКЗИ в Excel",
            "sczy_all.xlsx",
            "Excel Files (*.xlsx)"
        )
        if not path:
            return

        try:
            # Получаем все из БД
            con = pymysql.connect(
                host="localhost", port=3306,
                user="newuser", password="852456qaz",
                database="IB", charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor
            )
            cur = con.cursor()
            cur.execute("SELECT * FROM SCZY ORDER BY ID")
            rows = cur.fetchall()
            con.close()

            # Строим DataFrame
            df = pd.DataFrame(rows)

            # Сохраняем
            df.to_excel(path, index=False)
            QtWidgets.QMessageBox.information(self, "Готово", f"Выгрузка сохранена в:\n{path}")

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка экспорта", str(e))

    def export_filtered_sczy(self):
        # Диалог сохранения
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить отфильтрованные данные СКЗИ в Excel",
            "sczy_filtered.xlsx",
            "Excel Files (*.xlsx)"
        )
        if not path:
            return

        try:
            # Берём то, что в таблице
            table = self.table_widget7  # замените на реальное имя вашего QTableWidget
            headers = [table.horizontalHeaderItem(i).text() for i in range(table.columnCount())]
            data = []
            for r in range(table.rowCount()):
                row = {}
                for c, h in enumerate(headers):
                    item = table.item(r, c)
                    row[h] = item.text() if item else ""
                data.append(row)

            df = pd.DataFrame(data)

            df.to_excel(path, index=False)
            QtWidgets.QMessageBox.information(self, "Готово", f"Выгрузка сохранена в:\n{path}")

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка экспорта", str(e))

        # 2) Собираем данные из таблицы
        model = self.table_widget7  # или ваше имя виджета
        rows = []
        for r in range(model.rowCount()):
            row = {}
            for c in range(model.columnCount()):
                header = model.horizontalHeaderItem(c).text()
                item = model.item(r, c)
                row[header] = item.text() if item else ""
            rows.append(row)
        df = pd.DataFrame(rows)

        # 3) Сохраняем
        try:
            df.to_excel(path, index=False)
            QtWidgets.QMessageBox.information(self, "Экспорт выполнен", f"Выгрузка сохранена в {path}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка записи файла", str(e))

    def update_extra_fields_visibility(self):
        """
        Если нажата радиокнопка "Изьято", то показываем блок
        'Дополнительные сведения'. Иначе скрываем.
        """
        self.extra_group.setVisible(self.rb_taken.isChecked())

    def remove_unwanted_whitespace(self, value):
        if pd.isna(value):
            return None
        value_str = str(value)
        value_str = re.sub(r'[\r\n\t\u200b\u00a0]+', '', value_str)
        return value_str.strip()



    def import_excel(self, import_type: str) -> None:
        """
        Универсальный импортер Excel-файлов в одну из пяти таблиц:
          License, SCZY, KeysTable, CBR, TLS.
        ────────────────────────────────────────────────────────────────
        • import_type – ровно тот текст, который выбран в ComboBox
          («Импорт License», «Импорт SCZY», …).
        • Открывает диалог выбора *.xlsx*,
          приводит колонки, отбрасывает дубликаты
          и вставляет только новые строки.
        • Дубликат —- это:
            License   → (number_lic, name_of_soft)
            SCZY      → (number_license)
            KeysTable → (cert_serial_le)
            CBR       → (number_serial, number_key)
            TLS       → (number, DNS)
        """

        # ───────────────────────────────────────────────────────────────
        # 1. Конфигурация для каждого типа импорта
        # ───────────────────────────────────────────────────────────────
        CONFIG = {
            "Импорт License": dict(
                table="License",
                mapping={
                    "№ Заявки": "number",
                    "Наименование ПО СКЗИ": "name_of_soft",
                    "№ лицензии": "number_lic",
                    "Область применения / наименование ЭДО": "scop_using",
                    "Ф.И.О. пользователя": "fullname",
                    "Имя АРМ/IP": "name_apm",
                    "Дата установки": "date",
                    "Ф.И.О. сотрудника ИТ": "fullname_it",
                    "статус": "status",
                    "Отметка об изъятии/ уничтожении/ вывода из эксплуатации": "input_mark",
                    "Дата, расписка, номер акта об уничтожении": "input_date",
                },
                key_cols=["number_lic", "name_of_soft"],
                date_cols=["date"],
            ),
            "Импорт SCZY": dict(
                table="SCZY",
                mapping={
                    "Наименование СКЗИ": "name_of_SCZY",
                    "Тип ПО/ПАК": "sczy_type",
                    "Версия СКЗИ": "number_SCZY",
                    "Дата получения": "date",
                    "Регистрационный (серийный) номер": "number_license",
                    "Местонахождение": "location",
                    "Местонахождение ТОМ (текст)": "location_TOM_text",
                    "От кого получены": "owner",
                    "Дата и номер документа, сопроводительного письма": "date_and_number",
                    "Договор": "contract",
                    "ФИО владельца, бизнес процесс в рамках которого используется": "fullname_owner",
                    "Владельцы": "owners",
                    "Бизнес процессы": "buss_proc",
                    "Примечание": "additional",
                    "Дополнительно": "note",
                    "Сертификат": "number_certificate",
                    "Срок": "date_expired",
                },
                key_cols=["number_license"],
                date_cols=["date", "date_expired"],
            ),
            "Импорт Keys": dict(
                table="KeysTable",
                mapping={
                    "Статус да/нет": "status",
                    "Носитель (Серийный номер)": "type",
                    "Серийный номер сертификата": "cert_serial_le",
                    "ФИО владельца": "owner",
                    "Область действия / наименование ЭДО": "scope_using",
                    "Владелец ключа (ФИО)": "owner_fullname",
                    "VIP/ Critical": "VIP_Critical",
                    "Срок начала действия": "start_date",
                    "Срок окончания действия": "date_end",
                    "Дополнительно": "additional",
                    "Заявка/номер обращения": "number_request",
                    "Примечание": "note",
                },
                key_cols=["cert_serial_le"],
                date_cols=["start_date", "date_end"],
            ),
            "Импорт CBR": dict(
                table="CBR",
                mapping={
                    "Заявка/номер обращения": "number",
                    "Осталось дней": "status",
                    "Носитель (Серийный номер)": "number_serial",
                    "Номер ключа": "number_key",
                    "Выдавший УЦ": "owner",
                    "Область действия / наименование ЭДО": "scope_using",
                    "ФИО владельца": "fullname_owner",
                    "Срок начала действия": "date_start",
                    "Срок окончания действия": "date_end",
                    "Дополнительно": "additional",
                    "Примечание": "note",
                },
                key_cols=["number_serial", "number_key"],
                date_cols=["date_start", "date_end"],
            ),
            "Импорт TLS": dict(
                table="TLS",
                mapping={
                    "номер заявки": "number",
                    "Дата согласования заявки": "date",
                    "Среда": "environment",
                    "Доступ": "access",
                    "Выдавший УЦ": "issuer",
                    "Инициатор": "initiator",
                    "Владелец АС": "owner",
                    "тип сертификата": "algorithm",
                    "Область действия / наименование ЭДО": "scope",
                    "Сервис": "DNS",
                    "резолюция ИБ": "resolution",
                    "примечание (описание)": "note",
                },
                key_cols=["number", "DNS"],
                date_cols=["date"],
                # простые словари кодирования (по желанию)
                enum_maps=dict(
                    environment={"тест": "1", "продуктив": "2"},
                    access={"внешний": "1", "внутренний": "2"},
                    algorithm={"rsa": "1", "гост": "2"},
                    resolution={"уточнение": "1", "согласовано": "2", "отказано": "3"},
                ),
            ),
        }

        if import_type not in CONFIG:
            QMessageBox.warning(self, "Импорт", "Неизвестный тип импорта.")
            return

        cfg = CONFIG[import_type]

        # ───────────────────────────────────────────────────────────────
        # 2. Выбор файла
        # ───────────────────────────────────────────────────────────────
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите Excel-файл", "", "Excel Files (*.xlsx)"
        )
        if not file_path:
            return  # пользователь отменил

        # ───────────────────────────────────────────────────────────────
        # 3. Читаем Excel, оставляем и переименовываем нужные колонки
        # ───────────────────────────────────────────────────────────────
        df = pd.read_excel(file_path, header=0)
        df = df[[c for c in cfg["mapping"] if c in df.columns]].rename(
            columns=cfg["mapping"]
        )

        # ───────────────────────────────────────────────────────────────
        # 4. Приводим даты и чистим пробелы
        # ───────────────────────────────────────────────────────────────
        def _to_iso(v):
            if pd.isna(v):
                return None
            if isinstance(v, str):
                v = v.strip()
                d = pd.to_datetime(v, format="%d.%m.%Y", errors="coerce")
                if pd.isna(d):
                    d = pd.to_datetime(v, errors="coerce")
                return None if pd.isna(d) else d.strftime("%Y-%m-%d")
            if isinstance(v, (pd.Timestamp, datetime)):
                return v.strftime("%Y-%m-%d")
            return v

        for col in cfg["date_cols"]:
            if col in df.columns:
                df[col] = df[col].apply(_to_iso)

        # кастомные enum-карты (только для TLS)
        if "enum_maps" in cfg:
            for col, mp in cfg["enum_maps"].items():
                if col in df.columns:
                    df[col] = (
                        df[col]
                        .astype(str)
                        .str.lower()
                        .map(mp)
                        .fillna(df[col])  # если нет в словаре — оставляем как есть
                    )

        for c in df.columns:
            df[c] = df[c].apply(
                lambda x: " ".join(x.split()) if isinstance(x, str) else x
            )

        # ───────────────────────────────────────────────────────────────
        # 5. Подключение к БД и фильтрация дубликатов
        # ───────────────────────────────────────────────────────────────
        conn = pymysql.connect(
            host="localhost",
            port=3306,
            user="newuser",
            password="852456qaz",
            database="IB",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )
        try:
            with conn.cursor() as cur:
                cols_sql = ", ".join(cfg["key_cols"])
                cur.execute(f"SELECT {cols_sql} FROM {cfg['table']}")
                existing = {
                    tuple(row[k] for k in cfg["key_cols"]) for row in cur.fetchall()
                }

            df["_k"] = df.apply(lambda r: tuple(r[k] for k in cfg["key_cols"]), axis=1)
            df = df[~df["_k"].isin(existing)].drop(columns=["_k"])

            if df.empty:
                QMessageBox.information(
                    self, "Импорт", "Все записи уже присутствуют в базе."
                )
                return

            # ───────────────────────────────────────────────────────────
            # 6. Массовая вставка
            # ───────────────────────────────────────────────────────────
            db_cols = list(df.columns)  # порядок в INSERT возьмём из DataFrame
            col_sql = ", ".join(f"`{c}`" for c in db_cols)
            placeholders = ", ".join(["%s"] * len(db_cols))
            query = f"INSERT INTO {cfg['table']} ({col_sql}) VALUES ({placeholders})"

            payload = [
                tuple(None if pd.isna(v) else v for v in row)
                for row in df.itertuples(index=False, name=None)
            ]
            with conn.cursor() as cur:
                cur.executemany(query, payload)
                conn.commit()

            QMessageBox.information(
                self, "Импорт", f"Добавлено записей: {len(payload)}"
            )
        finally:
            conn.close()


    def showDate(self, date: QDate):
        """Обновляем метку выбранной даты."""
        self.cal_label.setText(date.toString())

    def on_toggle(self):
        """Метод, который вызывается при нажатии на кнопки с первой страницы."""

    def go_to_11_page(self):
        """Переключиться на 11 страницу (индекс 12)."""
        self.stacked_widget.setCurrentIndex(10)

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
        self.go_to_first_page(self)


    def upload_files(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Выберите тип импорта")

        layout = QVBoxLayout(dialog)

        # Небольшая подсказка
        label = QLabel("Выберите, что вы хотите импортировать:")
        layout.addWidget(label)

        # Варианты импорта в ComboBox
        combo = QComboBox()
        combo.addItems([
            "Импорт License",
            "Импорт SCZY",
            "Импорт Keys",
            "Импорт CBR",
            "Импорт TLS"
        ])
        layout.addWidget(combo)

        # Кнопки "ОК" и "Отмена"
        btn_layout = QHBoxLayout()
        btn_ok = QPushButton("ОК")
        btn_cancel = QPushButton("Отмена")
        btn_layout.addWidget(btn_ok)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)


        # Обработчик нажатия "ОК"
        def on_ok_clicked():
            self.import_excel(combo.currentText())
            dialog.accept()