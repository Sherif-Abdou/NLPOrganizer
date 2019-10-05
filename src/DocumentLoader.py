"""
Loads all Text and Word Documents in a Chosen Directory and stores them as Strings
"""
import os
import os.path as path


class DocumentLoader:
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

	def add_text_file(self, file_path):
		file = None
		try:
			file = open(file_path, "r")
			self.files[file_path] = file.read()
		except FileNotFoundError:
			print("Warning: File {} does not exist".format(file_path))
			return
		finally:
			if file is not None:
				file.close()
