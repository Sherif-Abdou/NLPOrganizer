"""
Organizes all the files in a given directory based on DocumentSorter outputs
"""

from src.DocumentSorter import DocumentSorter
from src.DocumentLoader import DocumentLoader
from src.File import File
from src.Category import Category
from shutil import move
from os import path, mkdir
from click import echo, secho


class DocumentOrganizer:
    def __init__(self, base_dir: str, nlp, logging=True):
        self.base_dir = base_dir
        self.nlp = nlp
        self.logging = logging
        self.document_loader = DocumentLoader(base_dir)
        self.document_loader.load_files()
        self.document_sorter = DocumentSorter(
            self.document_loader.files, self.nlp)
        self.categories = []

    # Sorts a given file
    def sort_file(self, file: File):
        if self.logging:
            echo("Sorting file: {}".format(path.basename(file.path)))
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
                               ) / len(category.files)

            # Similarity should be above the similarity threshold to be considered in the same category
            if similarity >= DocumentSorter.threshold:
                category.files.append(file)
                file.sorted = True
                return

        # Checks to see if a file can be sorted into a new category with another file
        similar_files = self.document_sorter.check_for_similar(
            file.path, file.contents)

        # Looks for the most similar file above the similarity threshold
        top_similar = (None, float("-inf"))
        for other_file, similarity in similar_files:
            if other_file.sorted is False and similarity >= top_similar[1]:
                top_similar = (other_file, similarity)

        # If there is such file create a category
        if top_similar[0] is not None:
            category = Category("untitled")
            file.sorted = True
            top_similar[0].sorted = True
            category.files.append(file)
            category.files.append(top_similar[0])
            self.categories.append(category)
            return

    # Creates category names for each of the created categories
    def category_names(self, manual=False):
        if manual:
            for category in self.categories:
                name = self.__name(category)
                category.name = name
            return
        for category in self.categories:
            self.document_sorter.category_name_for(category)
            if self.logging:
                echo("Category {}: {}".format(category.name,
                                              ', '.join([path.basename(file.path) for file in category.files])))

    def __name(self, category):
        secho(str(category), color="blue")
        name = input("Category name: ")
        if name is None or name == "":
            secho("Invalid Name \n", err=True)
            return self.__name(category)
        else:
            return name

    # Moves the sorted files into their proper place
    def move_files(self):
        for category in self.categories:
            if not path.exists(path.join(self.base_dir, category.name)):
                mkdir(path.join(self.base_dir, category.name))
            for file in category.files:
                move(file.path, path.join(self.base_dir,
                                          category.name, path.basename(file.path)))
