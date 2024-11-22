import os
from pytube import YouTube as yt
from pytube.cli import on_progress
from pydub import AudioSegment
import time
from multiprocessing import Process
import tempfile


class YoutubeAudioDownloader:
    def __init__(self,):
        self.url = None
        self.title = None
        self.file = None
        self.size = None
        self.thumbnail = None
        self.audio_segment = None

    def video_audio_download(self, url: str) -> None:
        self.url = url
        video_save_path = os.path.join(tempfile.gettempdir(), "videos")
        print(video_save_path)
        if not os.path.exists(video_save_path):
            os.makedirs(video_save_path)
        yt_video = yt(url, on_progress_callback=on_progress)
        streams = yt_video.streams
        self.thumbnail = yt_video.thumbnail_url.split("?")[0]
        audio = streams.get_audio_only()
        self.title = audio.title
        #self.title = self.title.replace("|", "-")
        self.size = audio.filesize_mb
        print(f"{self.title} | {self.size}mb")
        self.file = audio.download(video_save_path)
        self.audio_segment = AudioSegment.from_file(self.file)

    def audio_converter(self, title:str=None, thumbnail:str=None):
        if title is None:
            title = self.title
        if thumbnail is None:
            thumbnail = self.thumbnail
        audio_save_path = os.path.join(tempfile.gettempdir(), "audios")
        if not os.path.exists(audio_save_path):
            os.makedirs(audio_save_path)
        print("Converting to audio file...")
        audio_save_path = os.path.join(audio_save_path, title)
        self.audio_segment.export(f"{audio_save_path}.mp3", format="mp3", cover=thumbnail)
        with open(f"{audio_save_path}.mp3", "rb") as f:
            return f.read()

    def clear_files(self):
        print("chamou clear_files")
        if self.title:
            time.sleep(20)
            print(os.path.join("videos", self.title))
            os.remove(os.path.join(tempfile.gettempdir(), "videos", f"{self.title}.mp4"))
            os.remove(os.path.join(tempfile.gettempdir(), "audios", f"{self.title}.mp3"))
            print("limpooouuuu")

    def clean_routine(self):
        print("chamou exitinggg")
        p = Process(target=self.clear_files)
        p.start()
