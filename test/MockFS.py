import os
import os.path as path
from shutil import rmtree
from json import loads


def generate_mock_folder():
	if path.exists(path.join(path.dirname(__file__), "mock")):
		rmtree("mock")
	os.mkdir("mock")
	with open("mock_files.json", "r") as json:
		files = loads(json.read())
	for file in files:
		with open(path.join("mock", file["name"]), "w") as stream:
			stream.write(file["content"])
