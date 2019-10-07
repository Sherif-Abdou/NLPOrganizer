

class File:
    def __init__(self, path, contents):
        self.path = path
        self.contents = contents

    def __str__(self):
        return "${0}: ${1}".format(self.path, self.contents)
