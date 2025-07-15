from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import platform

from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.segmentedbutton import MDSegmentedButton, MDSegmentedButtonItem

import os
import threading
from yt_dlp import YoutubeDL


# Set default Android download directory if on Android
if platform == "android":
    from android.storage import primary_external_storage_path
    DOWNLOAD_DIR = os.path.join(primary_external_storage_path(), "Download")
else:
    DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), "Downloads")


class TabAudio(MDBoxLayout, MDTabsBase):
    pass

class TabVideo(MDBoxLayout, MDTabsBase):
    pass


class YouTubeDownloaderApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(self.kv_string)

    def on_start(self):
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    def download_audio(self):
        url = self.root.ids.audio_url.text.strip()
        bitrate = self.root.ids.bitrate_group.get_items()[self.root.ids.bitrate_group.selected].text.replace("k", "")
        if not url:
            return

        ydl_opts = {
            'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
            'ffmpeg_location': 'ffmpeg',
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': bitrate,
            }],
        }

        threading.Thread(target=self.download_thread, args=(ydl_opts, url)).start()

    def download_video(self):
        url = self.root.ids.video_url.text.strip()
        resolution = self.root.ids.resolution_group.get_items()[self.root.ids.resolution_group.selected].text
        if not url:
            return

        resolution_map = {
            '360p': 'best[height<=360][ext=mp4]',
            '480p': 'best[height<=480][ext=mp4]',
            '720p': 'best[height<=720][ext=mp4]',
            '1080p': 'best[height<=1080][ext=mp4]'
        }

        ydl_opts = {
            'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
            'ffmpeg_location': 'ffmpeg',
            'format': resolution_map.get(resolution, 'best[ext=mp4]'),
        }

        threading.Thread(target=self.download_thread, args=(ydl_opts, url)).start()

    def download_thread(self, ydl_opts, url):
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            print(f"Download failed: {e}")

    @property
    def kv_string(self):
        return '''
MDScreen:
    MDTabs:
        id: tabs
        TabAudio:
            title: "Audio (MP3)"
            orientation: "vertical"
            spacing: "10dp"
            padding: "20dp"

            MDTextField:
                id: audio_url
                hint_text: "Enter YouTube URL"
                mode: "rectangle"

            MDLabel:
                text: "Bitrate"
                halign: "center"

            MDSegmentedButton:
                id: bitrate_group
                MDSegmentedButtonItem:
                    text: "128k"
                MDSegmentedButtonItem:
                    text: "192k"
                    selected: True
                MDSegmentedButtonItem:
                    text: "320k"

            MDRaisedButton:
                text: "Download MP3"
                pos_hint: {"center_x": 0.5}
                on_release: app.download_audio()

        TabVideo:
            title: "Video (MP4)"
            orientation: "vertical"
            spacing: "10dp"
            padding: "20dp"

            MDTextField:
                id: video_url
                hint_text: "Enter YouTube URL"
                mode: "rectangle"

            MDLabel:
                text: "Resolution"
                halign: "center"

            MDSegmentedButton:
                id: resolution_group
                MDSegmentedButtonItem:
                    text: "360p"
                MDSegmentedButtonItem:
                    text: "480p"
                MDSegmentedButtonItem:
                    text: "720p"
                    selected: True
                MDSegmentedButtonItem:
                    text: "1080p"

            MDRaisedButton:
                text: "Download MP4"
                pos_hint: {"center_x": 0.5}
                on_release: app.download_video()
'''


if __name__ == "__main__":
    YouTubeDownloaderApp().run()
