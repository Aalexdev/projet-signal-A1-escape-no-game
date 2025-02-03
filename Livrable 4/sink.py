class Sink:
    def __init__(self):
        pass

    def write(self, chunk):
        pass

class Terminal:
    def __init__(self):
        pass

    def write(self, chunk):
        print(chunk)
    
class Buffer:
    def __init__(self):
        self.data = []
    
    def write(self, chunk):
        self.data.extend(chunk)