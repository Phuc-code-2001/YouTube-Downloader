from os import path, system

class Loger:
    def __init__(self, app, filename):
        self.app = app
        self.filename = filename
        self.box = []

    def load(self):
        if path.isfile(self.filename):
            with open(self.filename, 'r') as reader:
                for url in reader.read().split('\n'):
                    self.box.append(url.replace("\"", ""))
    
    def insert(self, url):
        system(f"echo \"{url}\" >> \"{self.filename}\"")
        self.box.append(url)
    
    def clear(self):
        if path.isfile(self.filename): system(f"del \"{self.filename}\"")
        self.box.clear()

    def include(self, url):
        return url in self.box