from assets.graphic import *
from assets.loger import *
from pytube import *
from pytube.cli import on_progress
from moviepy.editor import VideoFileClip, AudioFileClip
from time import sleep
from os import system, path
from threading import Thread

from tkinter.constants import END

class Application:
    def __init__(self):
        self.YTobject = None
        self.video = None
        self.video_stream = None
        self.audio_stream = None
        self.status = 0
        self.downloading = False
        self.download_stream = None
        self.UI = UI(self)
        self.savePath = "./Videos"
        self.res = ('1080p', '720p', '480p', '360p')
        self.option = 0
        self.loger = Loger(self, "URL")

    def check(self):
        url = self.UI.urlSearch.get()
        self.clean()
        try:
            yt = YouTube(url, on_progress_callback=on_progress, on_complete_callback=self.complete)
            self.YTobject = yt

        except:
            self.throwMessage(["Can't find URL!!!", "Please check url or network..."])
            self.YTobject = None

        if self.YTobject is not None:

            if not self.loger.include(url): self.loger.insert(url)

            self.throwMessage(["Title: " + self.YTobject.title, "Channel: " + self.YTobject.author])

            self.option = self.UI.optionVar.get()

            if self.option == 4:
                self.video = self.YTobject.streams.filter(only_audio=True).first()
                self.throwMessage(["Only audio ... OK", "File size : " + str(round(self.video.filesize / 1048576, 2)) + "MB"\
                    , "Ready to download!!!"])
                self.status = 1
                return 0

            video_stream = None
            audio_stream = None
            full_stream = self.YTobject.streams.filter(res=self.res[self.option], progressive=True).first()
            if full_stream is not None:
                self.video = full_stream
                self.throwMessage(["File size : " + str(round(full_stream.filesize / 1048576, 2)) + "MB"\
                    , "Resolusion " + self.res[self.option] + "...OK", "Audio ... OK", "(1) file. Ready to download!!!"])
                self.status = 1
            else:
                video_stream = self.YTobject.streams.filter(res=self.res[self.option]).first()
                if video_stream is None:
                    self.throwMessage(["Not found the resolusion " + self.res[self.option], "Please choose others...!!!"])
                else:
                    audio_stream = self.YTobject.streams.filter(only_audio=True).first()
                    self.throwMessage([f"Resolusion {self.res[self.option]} ...OK", "Audio ... OK", "Total size : " + \
                         str(round((audio_stream.filesize + video_stream.filesize) / 1048576, 2)) + "MB" \
                             , "(2) files. Ready to merge download !!!"])
                    self.video_stream = video_stream
                    self.audio_stream = audio_stream
                    self.status = 2


    def choosePath(self):
        choice = filedialog.askdirectory()
        if len(choice) != 0:
            self.savePath = choice
            self.UI.pathLabel.config(text=self.savePath)
        
    def complete(self):
        self.clean()
        self.throwMessage(["Download Done...!!!"])

    def download_callback(self):
        if self.downloading:
            self.clean()
            self.throwMessage(["Downloading. Please wait..."])
        else:
            self.download_stream = Thread(target=lambda: self.download())
            self.download_stream.start()

    def download(self):

        if self.status == 1:
            self.downloading = True
            
            if self.option == 4:
                if path.isfile("audio_file.mp4"): system(f"del \"audio_file.mp4\"")
                self.video.download(filename="audio_file")
                self.audioConvert("audio_file.mp4")
                self.clean()
                self.throwMessage(["Convert audio: Done...", "Download Successfully...!!!"])
            else:
                self.video.download(output_path=self.savePath)


            self.status = 0
            self.video = None
            self.downloading = False

        elif self.status == 2:
            self.downloading = True

            self.merge_download()
            self.downloading = False
            self.status = 0
            self.video = None
        else:
            self.clean()
            self.throwMessage(["Download not ready...", "Please check URL !!!"])
            self.download_stream = None

    def audioConvert(self, audname):
        audioFile = AudioFileClip(audname)
        name = self.YTobject.title
        expand = ".mp3"
        temp = "Undefined"
        audioFile.write_audiofile(temp + expand)

        system(f"ren \"{temp + expand}\" \"{name + expand}\"")
        system(f"move \"{name + expand}\" \"{self.savePath}\"")
        system(f"del \"{audname}\"")


    def merge_download(self):
        
        system("del audio_file.mp4")
        system("del video_file.mp4")
        system("del *wvf_snd.mp3")

        self.audio_stream.download(filename="audio_file")
        self.video_stream.download(filename="video_file")
        
        self.combine_audio("video_file.mp4", "audio_file.mp4")
        system("del audio_file.mp4")
        system("del video_file.mp4")
        self.throwMessage(["Clear cache successfully!!!"])
        
        self.video_stream = None
        self.audio_stream = None


    def combine_audio(self, vidname, audname, fps=23.98):
        my_clip = VideoFileClip(vidname)
        audio_background = AudioFileClip(audname)
        final_clip = my_clip.set_audio(audio_background)

        tempName = "Undefined"
        expand = ".mp4"
        name = self.YTobject.title
        final_clip.write_videofile(tempName + expand)

        system(f"ren \"{tempName + expand}\" \"{name + expand}\"")
        system(f"move \"{name + expand}\" \"{self.savePath}\"")

        self.clean()
        self.throwMessage(["Combine successfully...Done!!!"])

    def openCurrentFolder(self):
        currentFolder = self.savePath.replace('/', '\\')
        system(f"explorer \"{currentFolder}\"")

    def clean(self):
        self.UI.board.delete(0, END)

    def reset(self):
        self.UI.urlSearch.delete(0, END)
        self.clean()
        system("cls")

    def throwMessage(self, args):
        for message in args:
            self.UI.board.insert(END, message)

    def play(self):
        self.UI.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.loger.load()
        self.UI.mainloop()

    def on_closing(self):
        if self.download_stream:
            self.download_stream.join()
        self.UI.destroy()
