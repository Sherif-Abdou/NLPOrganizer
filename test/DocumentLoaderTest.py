import unittest

from test.MockFS import generate_mock_folder


class DocumentLoaderTest(unittest.TestCase):
	def test_data_collection(self):
		generate_mock_folder()


if __name__ == '__main__':
	unittest.main()
