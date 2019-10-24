import unittest
import spacy
from os import path
import os
from test.MockFS import generate_mock_folder
from src import DocumentSorter, DocumentLoader
from src.Category import Category


class document_sorter_test(unittest.TestCase):
    def test_similarity(self):
        os.environ["SPACY_WARNING_IGNORE"] = "W008"
        npl = spacy.load("en_core_web_lg")
        generate_mock_folder()
        mock_dir = path.join(path.dirname(__file__), "mock")
        loader = DocumentLoader(mock_dir)
        loader.load_files()
        sorter = DocumentSorter(loader.files, npl)

        print(sorter.check_for_similar(sorter.files[0].path, sorter.files[0].contents))

    def test_category(self):
        os.environ["SPACY_WARNING_IGNORE"] = "W008"
        npl = spacy.load("en_core_web_lg")
        generate_mock_folder()
        mock_dir = path.join(path.dirname(__file__), "mock")
        loader = DocumentLoader(mock_dir)
        loader.load_files()
        sorter = DocumentSorter(loader.files, npl)
        mock_category = Category("")
        mock_category.files.append(sorter.files[0])
        mock_category.files.append(sorter.files[1])
        print(sorter.category_name_for(mock_category))


if __name__ == '__main__':
    unittest.main()
