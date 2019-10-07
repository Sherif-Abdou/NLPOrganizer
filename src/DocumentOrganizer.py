"""
Organizes all the files in a given directory based on DocumentSorter outputs
"""

from src.DocumentSorter import DocumentSorter
from src.DocumentLoader import DocumentLoader
from shutil import move
from os import path


class DocumentOrganizer:
    def __init__(self, base_dir: str, nlp):
        self.base_dir = base_dir
        self.nlp = nlp
        self.document_loader = DocumentLoader(base_dir)
        self.document_loader.load_files()
        self.document_sorter = DocumentSorter(self.document_loader.files, self.nlp)

    def sort_file(self, file):
        pass
