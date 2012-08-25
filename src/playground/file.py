class ScanFile:
    name = ""
    hash = 0
    type = ""

    def __init__(self, name, hash, type):
        self.name = name
        self.hash = hash
        self.type = type

    def __repr__(self):
        return self.name
