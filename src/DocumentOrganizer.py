"""
Organizes all the files in a given directory based on DocumentSorter outputs
"""

from src.DocumentSorter import DocumentSorter
from src.DocumentLoader import DocumentLoader
from src.File import File
from src.Category import Category
from shutil import move
from os import path, mkdir


class DocumentOrganizer:
	def __init__(self, base_dir: str, nlp):
		self.base_dir = base_dir
		self.nlp = nlp
		self.document_loader = DocumentLoader(base_dir)
		self.document_loader.load_files()
		self.document_sorter = DocumentSorter(self.document_loader.files, self.nlp)
		self.categories = []

	def sort_file(self, file: File):
		if file.sorted:
			return
		for category in self.categories:
			similarity = 0
			for category_file in category.files:
				similarity += (self.nlp(file.contents).similarity(self.nlp(category_file.contents)))/len(category.files)
			if similarity >= DocumentSorter.threshold:
				category.files.append(file)
				file.sorted = True
				return
		similar_files = self.document_sorter.check_for_similar(file.path, file.contents)
		for other_file in similar_files:
			if other_file.sorted is False:
				category = self.document_sorter.category_name_for(file.contents, other_file.contents)
				file.sorted = True
				other_file.sorted = True
				category.files.append(file)
				category.files.append(other_file)
				self.categories.append(category)
				return

	def move_files(self):
		for category in self.categories:
			if not path.exists(path.join(self.base_dir, category.name)):
				mkdir(path.join(self.base_dir, category.name))
			for file in category.files:
				move(file.path, path.join(self.base_dir, category.name, path.basename(file.path)))
