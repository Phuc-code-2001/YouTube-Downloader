from os import path
from tkinter.constants import END

class Loger:
    def __init__(self, app, filename):
        self.app = app
        self.filename = filename
        self.box = []

    def load(self):
        if path.isfile(self.filename):
            with open(self.filename, 'r') as reader:
                for url in reader.read().split('\n'):
                    self.box.append(url)
                    self.app.UI.urlBefore.insert(END, url)
    
    def insert(self, url):
        system(f"echo {url} >> \"{self.filename}\"")
        self.box.append(url)
        self.app.UI.urlBefore.insert(END, url)
    
    def clear(self):
        system(f"del \"{self.filename}\"")
        self.app.UI.urlBefore.delete(0, END)
        self.box.clear()

    def include(self, url):
        return url in self.box