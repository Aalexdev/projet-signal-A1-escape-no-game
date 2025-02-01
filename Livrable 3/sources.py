class Source:
    def __init__(self):
        pass
    
    # returns the next char
    def next(self) -> str:
        pass

    def valid(self) -> bool:
        pass

class Message(Source):
    def __init__(self, message):
        self.message = message
        self.i = 0

    def next(self) -> str:
        self.i += 1
        return self.message[self.i-1]

    def valid(self) -> bool:
        return self.i != len(self.message)


# TODO
class File(Source):
    def __init__(self, path):
        self.path = path
        self.file = open(path)

    def next(self) -> str:
        return self.file.read()