from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *

class UI(Tk):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.WIDTH = 850
        self.HEIGHT = 500
        self.X = 600
        self.Y = 150
        self.geometry(str(self.WIDTH) + 'x' +  str(self.HEIGHT) + '+' + str(self.X) + '+' + str(self.Y))
        self.title("Youtube Downloader")
        self.icon = PhotoImage(file="icon.png")
        self.iconphoto(False, self.icon)
        self.configure(background='#21AADD')
        self.resizable(1, 1)

        self.setLayout()

    def setLayout(self):
        self.TopLayout = LabelFrame(self, text="Tools", font="Constantia 12", bg=self['bg'])
        self.TopLayout.place(x=0, y=0, relwidth=1, relheight=0.5)

        self.urlSearch = Entry(self.TopLayout, font="Constantia 12")
        self.urlSearch.insert(0, "Enter the url here...")
        self.urlSearch.place(relx=0.025, y=12, relwidth=0.475, height=30)
      
        self.checkBtn = Button(self.TopLayout, text="Check", font="Constantia 12", command=lambda: self.app.check())
        self.dlBtn = Button(self.TopLayout, text="Download", font="Constantia 12", command=lambda: self.app.download_callback())
        self.openYTBtn = Button(self.TopLayout, text="YouTube", font="Constantia 12", command=lambda: self.app.openYouTube())
        self.pathBtn = Button(self.TopLayout, text="...", font="Constantia 12", command= lambda: self.setPath())
        self.clshtr = Button(self.TopLayout, text='Clear', font="Constantia 12", command=lambda: self.app.clearURL())
        self.openBtn = Button(self.TopLayout, text="Open", font="Constantia 12", command=lambda: self.app.openCurrentFolder())
        self.pathLabel = Label(self.TopLayout, text=": ./videos", font="Constantia 12", bg=self['bg'])


        self.pathBtn.place(relx=0.025, relwidth=0.05, y=50, height=20)
        self.pathLabel.place(relx=0.075, y=50, height=20)
        self.checkBtn.place(relx=0.025, y=80)
        self.dlBtn.place(relx=0.14, y=80)
        self.openYTBtn.place(relx=0.3, y=80)
        self.TopLayout.update()
        self.clshtr.place(relx=0.025, y=130, width=self.checkBtn.winfo_width())
        self.openBtn.place(relx=0.14, y=130)
        

        self.optionVar = IntVar()
        self.r1 = Radiobutton(self.TopLayout, text="1080p", variable=self.optionVar, value=0, font="Times 12", bg=self['bg'])
        self.r2 = Radiobutton(self.TopLayout, text="720p", variable=self.optionVar, value=1, font="Times 12", bg=self['bg'])
        self.r3 = Radiobutton(self.TopLayout, text="480p", variable=self.optionVar, value=2, font="Times 12", bg=self['bg'])
        self.r4 = Radiobutton(self.TopLayout, text="360p", variable=self.optionVar, value=3, font="Times 12", bg=self['bg'])
        self.r5 = Radiobutton(self.TopLayout, text="Audio", variable=self.optionVar, value=4, font="Times 12", bg=self['bg'])

        self.r1.place(relx=0.4, y=90, height=30)
        self.r2.place(relx=0.25, y=120, height=30)
        self.r3.place(relx=0.4, y=120, height=30)
        self.r4.place(relx=0.25, y=145, height=30)
        self.r5.place(relx=0.4, y=145, height=30)

        self.InfoLayout = LabelFrame(self.TopLayout, text="Info", font="Constantia 12", bg=self['bg'])
        self.InfoLayout.place(relx=0.525, y=0, relwidth=0.475, relheight=1)

        self.scrollbarX = Scrollbar(self.InfoLayout)
        self.board = Listbox(self.InfoLayout, selectmode="MULTIPLE", xscrollcommand=self.scrollbarX.set, height=6, width=30, font="Constantia 12", bg='#AABBAA')
        self.scrollbarX.config(command=self.board.xview, orient="horizontal")
        
        self.board.place(x=5, relwidth=0.95, relheight=0.85)
        self.scrollbarX.pack(fill='x', side='bottom')

        self.BottomLayout = LabelFrame(self, text="History", font="Constantia 12")
        self.BottomLayout.place(x=0, rely=0.5, relwidth=1, relheight=0.5)

        self.urlBefore = Listbox(self.BottomLayout, selectmode="SINGLE", height=5, font="Constantia 12")
        self.urlBefore.place(relx=0.05, relwidth=0.9, rely=0.1, relheight=0.8)

    def clean(self):
        self.board.delete(0, END)

    def print(self, message):
        for text in message:
            self.board.insert(END, text)

    def setPath(self):
        path = askdirectory()
        if path:
            self.app.savePath = path
            self.pathLabel.config(text=path)

    def load(self, urlbox):
        for url in urlbox:
            self.insert(url)
    
    def insert(self, url):
        self.urlBefore.insert(END, url)

    def clearURL(self):
        self.urlBefore.delete(0, END)
    