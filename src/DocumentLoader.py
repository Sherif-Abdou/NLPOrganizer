"""
Loads all Text and Word Documents in a Chosen Directory and stores them as Strings
"""
import os
import os.path as path
import docx2txt
import PyPDF2
from src.File import File


class DocumentLoader:
    def __init__(self, directory: str):
        self.directory = directory
        self.files = []

    def load_files(self):
        files = os.listdir(self.directory)
        # Checks the file extension of each file
        for file in files:
            parts = file.split(".")
            ext = parts[len(parts) - 1]
            # Calls appropriate method for each file type
            if ext == "txt":
                self.add_text_file(path.join(self.directory, file))
            elif ext == "docx":
                self.add_word_file(path.join(self.directory, file))
            elif ext == "pdf":
                self.add_pdf_file(path.join(self.directory, file))

    def add_text_file(self, file_path):
        try:
            with open(file_path, "r") as file:
                text_file = File(file_path, file.read())
                self.files.append(text_file)
        except Exception as error:
            print("Couldn't Load {0}: {1}".format(file_path, error))
        return

    def add_word_file(self, file_path):
        try:
            text = docx2txt.process(file_path)
            file = File(file_path, text)
            self.files.append(file)
        except Exception as error:
            print("Couldn't Load {0}: {1}".format(file_path, error))
        return

    def add_pdf_file(self, file_path):
        try:
            with open(file_path, "rb") as raw_file:
                reader = PyPDF2.PdfFileReader(raw_file)
                pages = reader.numPages
                text = ""
                for i in range(pages):
                    page = reader.getPage(i)
                    text += page.extractText()
                file = File(file_path, text)
                self.files.append(file)
        except Exception as error:
            print("Couldn't Load {0}: {1}".format(file_path, error))
