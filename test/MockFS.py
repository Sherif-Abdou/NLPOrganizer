import os
import os.path as path
from shutil import rmtree


def generate_mock_folder():
	if path.exists(path.join(path.dirname(__file__), "mock")):
		rmtree("mock")
	os.mkdir("mock")
	with open("mock/a.txt", "w") as a:
		a.write("Hello World this is a test document #1.\nIt's a pretty cool test document.")
	with open("mock/b.txt", "w") as b:
		b.write("Hello Land this is a test thing #2.\nIt's a pretty quality test thing.")
	with open("mock/c.ab.txt", "w") as b:
		b.write("Hello Land this is a test thing #3.\nIt's a pretty quality test thing.")
