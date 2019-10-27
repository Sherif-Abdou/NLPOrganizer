"""
A file category
"""

from src.File import File
from os.path import basename

class Category:
    def __init__(self, name: str):
        self.name = name
        self.files = []
    def __str__(self):
        files = " : ".join([basename(file.path) for file in self.files])
        return files