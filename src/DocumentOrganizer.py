"""
Organizes all the files in a given directory based on DocumentSorter outputs
"""

from src.DocumentSorter import DocumentSorter
from src.DocumentLoader import DocumentLoader
from src.File import File
from shutil import move
from os import path, mkdir


class DocumentOrganizer:
    def __init__(self, base_dir: str, nlp):
        self.base_dir = base_dir
        self.nlp = nlp
        self.document_loader = DocumentLoader(base_dir)
        self.document_loader.load_files()
        self.document_sorter = DocumentSorter(
            self.document_loader.files, self.nlp)
        self.categories = []

    def sort_file(self, file: File):
        if file.sorted:
            return
        # Check to see if a file can be sorted into a pre-existing category
        for category in self.categories:
            similarity = 0
            # Collects the average similarity to each document already in the category
            for category_file in category.files:
                file_doc_no_stop = self.nlp(
                    ' '.join([str(t) for t in self.nlp(file.contents) if not t.is_stop]))
                other_doc_no_stop = self.nlp(
                    ' '.join([str(t) for t in self.nlp(category_file.contents) if not t.is_stop]))
                similarity += (file_doc_no_stop.similarity(other_doc_no_stop)
                               )/len(category.files)
            if similarity >= DocumentSorter.threshold:
                category.files.append(file)
                file.sorted = True
                return

        # Checks to see if a file can be sorted into a new category with another file
        similar_files = self.document_sorter.check_for_similar(
            file.path, file.contents)
        for other_file in similar_files:
            if other_file.sorted is False:
                category = self.document_sorter.category_name_for(
                    file.contents, other_file.contents)
                file.sorted = True
                other_file.sorted = True
                category.files.append(file)
                category.files.append(other_file)
                self.categories.append(category)
                return

    # Moves the sorted files into their proper place
    def move_files(self):
        for category in self.categories:
            if not path.exists(path.join(self.base_dir, category.name)):
                mkdir(path.join(self.base_dir, category.name))
            for file in category.files:
                move(file.path, path.join(self.base_dir,
                                          category.name, path.basename(file.path)))
