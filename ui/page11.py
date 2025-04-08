from PyQt5.QtGui import QKeySequence
from PyQt6.QtGui import QShortcut
from PyQt6.QtWidgets import (
    QWidget,
    QLabel, QPushButton, QVBoxLayout, QFileDialog
)
from PyQt6.QtCore import Qt
import pandas as pd
import mariadb
import os


def create_page11(self) -> QWidget:
    page = QWidget()
    # Устанавливаем общий тёмный фон и белый текст для всей страницы
    page.setStyleSheet("background-color: #121212; color: white;")
    main_layout = QVBoxLayout(page)
    main_layout.setContentsMargins(20, 20, 20, 20)
    main_layout.setSpacing(15)

    # Кнопка "Назад на главную"
    btn_back = QPushButton("Назад на главную")
    btn_back.clicked.connect(self.go_to_first_page)
    btn_back.setStyleSheet(
        "background-color: #333333; color: white; font-size: 15px; "
        "border: 1px solid #555; border-radius: 4px; padding: 5px;"
    )
    btn_back.setMinimumSize(150, 30)
    main_layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignLeft)

    # Заголовок
    header_label = QLabel("Импорт данных Excel")
    header_label.setWordWrap(True)
    header_label.setStyleSheet("font-size: 20px; color: white;")
    header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    main_layout.addWidget(header_label)

    # Кнопка для импорта файла
    btn_upload = QPushButton("Импорт")
    btn_upload.clicked.connect(self.upload_file)
    btn_upload.setStyleSheet(
        "background-color: #333333; color: white; font-size: 15px; "
        "border: 1px solid #555; border-radius: 4px; padding: 5px;"
    )
    main_layout.addWidget(btn_upload, alignment=Qt.AlignmentFlag.AlignCenter)




    return page
