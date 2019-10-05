"""
Loads all Text and Word Documents in a Chosen Directory and stores them as Strings
"""
import os
import os.path as path

class DocumentLoader():
	def __init__(self, directory: str):
		self.directory = directory
		self.files = dict()

	def load_text_files(self):
		files = os.listdir(self.directory)
		for file in files:
			parts = file.split(".")
			ext = parts[len(parts)-1]
			if ext == "txt":
				self.add_text_file(path.join(self.directory, file))
