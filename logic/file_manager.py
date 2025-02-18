import os

from PyQt6.QtWidgets import QFileDialog


def fileManager():
    file_dialog = QFileDialog()
    file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
    file_dialog.setNameFilter("Excel Files (*.xlsx);;Text Files (*.txt);;Python Files (*.py)")
    if file_dialog.exec():
        selected_file = file_dialog.selectedFiles()[0]
        os.rename(selected_file, 'Журналы.xlsx')
