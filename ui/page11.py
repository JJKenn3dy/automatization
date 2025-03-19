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
    main_layout = QVBoxLayout(page)
    main_layout.setContentsMargins(20, 20, 20, 20)
    main_layout.setSpacing(15)

    # Заголовок
    header_label = QLabel("Импорт данных Excel")
    header_label.setWordWrap(True)
    header_label.setStyleSheet("font-size: 20px; color: #76787A;")
    header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    main_layout.addWidget(header_label)

    btn_upload = QPushButton("1")
    btn_upload.clicked.connect(self.upload_file)
    main_layout.addWidget(btn_upload, alignment=Qt.AlignmentFlag.AlignCenter)

    btn_back = QPushButton("Назад на главную")
    btn_back.clicked.connect(self.go_to_first_page)
    main_layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)
    return page

