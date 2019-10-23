import os
import os.path as path
from shutil import rmtree
from json import loads


def generate_mock_folder():
    if path.exists(path.join(path.dirname(__file__), "mock")):
        rmtree(path.join(path.dirname(__file__), "mock"))
    os.mkdir(path.join(path.dirname(__file__), "mock"))
    with open(path.join(path.dirname(__file__), "mock_files.json"), "r", encoding="utf8", errors="ignore") as json:
        files = loads(json.read())
    for file in files:
        with open(path.join(path.dirname(__file__), "mock", file["name"]), "w", encoding="utf8") as stream:
            stream.write(file["content"])
