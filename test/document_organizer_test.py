import unittest
import spacy
from test.MockFS import *
from src.DocumentOrganizer import DocumentOrganizer


class MyTestCase(unittest.TestCase):
	def test_sort_files(self):
		npl = spacy.load("en_core_web_lg")
		generate_mock_folder()
		mock_dir = path.join(path.dirname(__file__), "mock")
		organizer = DocumentOrganizer(mock_dir, npl)
		for file in organizer.document_loader.files:
			organizer.sort_file(file)
		for category in organizer.categories:
			print(category.name)
			print([str(file) for file in category.files])


if __name__ == '__main__':
	unittest.main()
