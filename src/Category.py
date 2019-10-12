from src.File import File


class Category:
    def __init__(self, name: str):
        self.name = name
        self.files = []
