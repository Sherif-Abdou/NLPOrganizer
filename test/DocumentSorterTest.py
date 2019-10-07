import unittest
import spacy
from os import path

from test.MockFS import generate_mock_folder
from src import DocumentSorter, DocumentLoader


class DocumentSorterTest(unittest.TestCase):
	def test_similarity(self):
		npl = spacy.load("en_core_web_lg")
		generate_mock_folder()
		mock_dir = path.join(path.dirname(__file__), "mock")
		loader = DocumentLoader(mock_dir)
		loader.load_files()
		sorter = DocumentSorter(loader.files, npl)
		print(sorter.check_for_similar(path.join(mock_dir, "a.txt"), sorter.files[path.join(mock_dir, "a.txt")]))

	def test_category(self):
		npl = spacy.load("en_core_web_lg")
		generate_mock_folder()
		mock_dir = path.join(path.dirname(__file__), "mock")
		loader = DocumentLoader(mock_dir)
		loader.load_files()
		sorter = DocumentSorter(loader.files, npl)
		print(sorter.category_name_for(sorter.files[path.join(mock_dir, "a.txt")],
								 sorter.files[path.join(mock_dir, "b.txt")]))


if __name__ == '__main__':
	unittest.main()
