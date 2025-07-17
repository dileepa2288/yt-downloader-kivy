from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import platform
from kivy.uix.screen import Screen

from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.segmentedbutton import MDSegmentedButton, MDSegmentedButtonItem
from kivymd.uix.label import MDLabel

import os
import threading
from yt_dlp import YoutubeDL

# Set default Android download directory if on Android
if platform == "android":
    from android.storage import primary_external_storage_path
    DOWNLOAD_DIR = os.path.join(primary_external_storage_path(), "Download")
else:
    DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), "Downloads")

# KV string with Screen wrapper for KivyMD compatibility
kv_string = '''
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

            MDLabel:
                id: status_label
                text: "Status: Idle"
                halign: "center"
'''

class TabAudio(MDBoxLayout, MDTabsBase):
    pass

class TabVideo(MDBoxLayout, MDTabsBase):
    pass

class YouTubeDownloaderApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(kv_string)

    def on_start(self):
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    def download_audio(self, instance):
        url = self.root.ids.audio_url.text.strip()
        bitrate = self.root.ids.bitrate_group.get_items()[self.root.ids.bitrate_group.selected].text.replace("k", "")
        if not url:
            self.root.ids.status_label.text = "Status: Please enter a URL"
            return

        self.root.ids.status_label.text = "Status: Downloading..."
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': bitrate,
            }],
        }
        threading.Thread(target=self.download_thread, args=(ydl_opts, url, "audio")).start()

    def download_video(self, instance):
        url = self.root.ids.video_url.text.strip()
        resolution = self.root.ids.resolution_group.get_items()[self.root.ids.resolution_group.selected].text
        if not url:
            self.root.ids.status_label.text = "Status: Please enter a URL"
            return

        self.root.ids.status_label.text = "Status: Downloading..."
        resolution_map = {
            '360p': 'best[height<=360][ext=mp4]',
            '480p': 'best[height<=480][ext=mp4]',
            '720p': 'best[height<=720][ext=mp4]',
            '1080p': 'best[height<=1080][ext=mp4]'
        }
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
            'format': resolution_map.get(resolution, 'best[ext=mp4]'),
        }
        threading.Thread(target=self.download_thread, args=(ydl_opts, url, "video")).start()

    def download_thread(self, ydl_opts, url, media_type):
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.root.ids.status_label.text = f"Status: {media_type.capitalize()} download completed!"
        except Exception as e:
            self.root.ids.status_label.text = f"Status: Error - {str(e)}"

if __name__ == "__main__":
    YouTubeDownloaderApp().run()
