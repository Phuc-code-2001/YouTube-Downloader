from pytube import *
from pytube.cli import on_progress
from moviepy.editor import VideoFileClip, AudioFileClip
from os import system, path
from threading import Thread
import webbrowser
import time

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
        self.savePath = "./videos"
        self.res = ('1080p', '720p', '480p', '360p')
        self.option = 0

        self.loger = Loger(self, "URL")
        self.chromeDriver = None

    def check(self):
        url = self.UI.urlSearch.get()
        self.UI.clean()
        try:
            yt = YouTube(url, on_progress_callback=on_progress)
            self.YTobject = yt

        except:
            self.UI.print(["Can't find URL!!!", "Please check url or network..."])
            self.YTobject = None

        if self.YTobject != None:

            self.insert(url)

            self.UI.print(["Title: " + self.YTobject.title, "Channel: " + self.YTobject.author])

            self.option = self.UI.optionVar.get()

            if self.option == 4:
                self.video = self.YTobject.streams.filter(only_audio=True).first()
                self.UI.print(["Only audio...OK", f"File size : {round(self.video.filesize / 1048576, 2)}MB", "Ready to download!!!"])
                self.status = 1

            else:
                full_stream = self.YTobject.streams.filter(res=self.res[self.option], progressive=True).first()
                if full_stream != None:
                    self.video = full_stream
                    self.UI.print([f"Resolusion {self.res[self.option]}...OK", "Audio ... OK", f"File size : {round(full_stream.filesize / 1048576, 2)}MB", "(1) file. Ready to download!!!"])
                    self.status = 1
                else:
                    self.video = None
                    video_stream = self.YTobject.streams.filter(res=self.res[self.option]).first()
                    audio_stream = self.YTobject.streams.filter(only_audio=True).first()

                    if video_stream is None:
                        self.UI.print(["Not found the resolusion " + self.res[self.option], "Please choose others...!!!"])
                    else:
                        self.UI.print([f"Resolusion {self.res[self.option]} ...OK", "Audio ... OK", f"Total size : {round((audio_stream.filesize + video_stream.filesize) / 1048576, 2)}MB", "(2) files. Ready to merge download !!!"])
                        self.video_stream = video_stream
                        self.audio_stream = audio_stream
                        self.status = 2

    def download_callback(self):
        if self.downloading:
            self.UI.clean()
            self.UI.print(["Downloading", f"Video: {self.YTobject.title}", "Please wait..."])
        else:
            self.download_stream = Thread(target=lambda: self.download())
            self.download_stream.start()

    def download(self):
        self.downloading = True
        if self.status == 1:
            if self.option == 4:
                if path.isfile("audio_file.mp4"): system(f"del \"audio_file.mp4\"")
                self.video.download(filename="audio_file")
                self.audioConvert("audio_file.mp4")
                self.UI.clean()
                self.UI.print(["Convert audio: Done...", "Download Successfully...!!!"])
            else:
                self.video.download(output_path=self.savePath)
                self.UI.clean()
                self.UI.print(["Downloaded Succesfully..."])

        elif self.status == 2:
            self.merge_download()

        else:
            self.UI.clean()
            self.UI.print(["Download not ready...", "Please check URL !!!"])

        self.status = 0
        self.video = None
        self.downloading = False
        self.download_stream = None

    def audioConvert(self, audname):
        audioFile = AudioFileClip(audname)
        name = self.format(self.YTobject.title)
        expand = ".mp3"
        temp = "Undefined"
        audioFile.write_audiofile(temp + expand)

        system(f"ren \"{temp + expand}\" \"{name + expand}\"")
        system(f"move \"{name + expand}\" \"{self.savePath}\"")
        system(f"del \"{audname}\"")


    def merge_download(self):
        
        if path.isfile("audio_file.mp4"): system("del audio_file.mp4")
        if path.isfile("video_file.mp4"): system("del video_file.mp4")
        if path.isfile("*wvf_snd.mp3"): system("del *wvf_snd.mp3")

        self.audio_stream.download(filename="audio_file")
        self.video_stream.download(filename="video_file")
        
        self.combine_audio("video_file.mp4", "audio_file.mp4")
        system("del audio_file.mp4")
        system("del video_file.mp4")
        
        self.video_stream = None
        self.audio_stream = None


    def combine_audio(self, vidname, audname, fps=23.98):
        my_clip = VideoFileClip(vidname)
        audio_background = AudioFileClip(audname)
        final_clip = my_clip.set_audio(audio_background)

        tempName = "Undefined"
        expand = ".mp4"
        name = self.format(self.YTobject.title)
        final_clip.write_videofile(tempName + expand)

        system(f"ren \"{tempName + expand}\" \"{name + expand}\"")
        system(f"move \"{name + expand}\" \"{self.savePath}\"")

        self.UI.clean()
        self.UI.print(["Combine successfully...Done!!!"])

    def openCurrentFolder(self):
        currentFolder = self.savePath.replace('/', '\\')
        system(f"explorer \"{currentFolder}\"")

    def openYouTube(self):
        #check Google chrome
        
        if self.chromeDriver is None:
            if path.isfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"):
                self.chromeDriver = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            elif path.isfile("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"):
                self.chromeDriver = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        
        if self.chromeDriver != None:
            webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(self.chromeDriver))
            webbrowser.get('chrome').open("https://youtube.com")
        else:
            self.UI.print(["Can't find Google Chrome", "Please install Google Chrome to use this function!!!"])

    def format(self, name):
        target = ""
        for r in name:
            if r in ['\\', '/', ':','*', '?', '"', '<', '>', '|']:
                target += '_'
            else:
                target += r
        return target

    def load(self):
        self.loger.load()
        self.UI.load(self.loger.box)
    
    def insert(self, url):
        if self.loger.include(url):
            ...
        else:
            self.loger.insert(url)
            self.UI.insert(url)
    
    def clearURL(self):
        if askokcancel("Clear", "Do you really to clear all URLs in history?"):
            self.loger.clear()
            self.UI.clearURL()

    def setDefaultSavePath(self):
        if path.isdir(self.savePath):
            ...
        else:
            system(f"mkdir \"{self.savePath}\"")

        # self.savePath = path._getfullpathname(self.savePath)
        # self.UI.pathLabel.config(text=self.savePath)
        

    def play(self):
        self.UI.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.load()
        self.setDefaultSavePath()
        self.UI.mainloop()

    def on_closing(self):
        if self.download_stream != None:
            _exit = askyesno("Exit", f"You are downloading {self.YTobject.title}, \nDo you want to quit anyway?")
            if _exit:
                self.download_stream.join()
                self.UI.destroy()
        else:
            self.UI.destroy()

if __name__ == "__main__":
    from graphic import *
    from loger import *
    app = Application()
    app.play()
else:
    from assets.graphic import *
    from assets.loger import *