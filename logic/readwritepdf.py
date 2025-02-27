import docx
import pdfplumber
from PyQt6.QtWidgets import QMessageBox
from docx import Document
from docx.shared import Inches
from docx import Document

def pdf_check(self):
    try:
        # Открытие PDF-файла
        with pdfplumber.open("test.pdf") as pdf:

            # Извлечение текста из PDF
            text = ""
            for page in pdf.pages:
                text += page.extract_text()

        # Создание нового документа Word
        document = Document()

        # Добавление абзаца в Word, содержащего текст
        document.add_paragraph(text)

        # Сохранение документа Word
        document.save("output.docx")

        getText("output.docx")
    except FileNotFoundError:
        QMessageBox.warning(self, "Ошибка", "PDF с ключами не был найден")


def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)


    return '\n'.join(fullText)
