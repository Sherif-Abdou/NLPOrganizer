import os
import os.path as path
from shutil import rmtree
from json import loads, dump


def generate_mock_folder():
    if path.exists(path.join(path.dirname(__file__), "mock")):
        rmtree(path.join(path.dirname(__file__), "mock"))
    os.mkdir(path.join(path.dirname(__file__), "mock"))
    with open(path.join(path.dirname(__file__), "mock_files.json"), "r", encoding="utf8", errors="ignore") as json:
        files = loads(json.read())
    for file in files:
        with open(path.join(path.dirname(__file__), "mock", file["name"]), "w", encoding="utf8") as stream:
            stream.write(file["content"])


def generate_mock_json_from(folder):
    json = dict()
    for file in os.listdir(folder):
        if path.isdir(path.join(folder, file)):
            continue
        ext = file.split(".")
        ext = ext[len(ext)-1]
        if ext == "txt":
            with open(path.join(folder, file), "r") as stream:
                json[file] = stream.read()

    with open(path.join(path.dirname(__file__), "mock_files.json"), "w") as stream:
        dump(json, stream)