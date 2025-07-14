from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput as ScrollableText
from kivy.core.clipboard import Clipboard
from kivy.utils import platform
import os
import threading
from yt_dlp import YoutubeDL

# Android-specific paths
if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
    DOWNLOAD_DIR = "/storage/emulated/0/Download"
    FFMPEG_PATH = "ffmpeg"  # Buildozer will include ffmpeg in the APK
else:
    DOWNLOAD_DIR = os.path.expanduser("~/Downloads")
    FFMPEG_PATH = "/usr/bin/ffmpeg"  # Adjust for your local environment

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

class YouTubeDownloader(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10)

        # URL input
        self.add_widget(Label(text="YouTube URL:", size_hint_y=0.1))
        self.url_input = TextInput(multiline=False, size_hint_y=0.1)
        self.add_widget(self.url_input)

        # Paste button
        paste_btn = Button(text="Paste URL", size_hint_y=0.1)
        paste_btn.bind(on_press=self.paste_url)
        self.add_widget(paste_btn)

        # Download directory
        self.download_dir = DOWNLOAD_DIR
        self.dir_label = Label(text=f"Download Path: {self.download_dir}", size_hint_y=0.1)
        self.add_widget(self.dir_label)

        # Format selection
        self.format_choice = Spinner(
            text="Audio (MP3)",
            values=("Audio (MP3)", "Video (MP4)"),
            size_hint_y=0.1
        )
        self.format_choice.bind(text=self.update_options)
        self.add_widget(self.format_choice)

        # Resolution selection
        self.resolution_layout = BoxLayout(size_hint_y=0.1)
        self.resolution_label = Label(text="Video Resolution:", size_hint_x=0.4)
        self.resolution_choice = Spinner(
            text="720p",
            values=("360p", "480p", "720p", "1080p"),
            size_hint_x=0.6
        )
        self.resolution_layout.add_widget(self.resolution_label)
        self.resolution_layout.add_widget(self.resolution_choice)
        self.resolution_layout.visible = False
        self.add_widget(self.resolution_layout)

        # Bitrate selection
        self.bitrate_layout = BoxLayout(size_hint_y=0.1)
        self.bitrate_label = Label(text="MP3 Bitrate:", size_hint_x=0.4)
        self.bitrate_choice = Spinner(
            text="192k",
            values=("128k", "192k", "320k"),
            size_hint_x=0.6
        )
        self.bitrate_layout.add_widget(self.bitrate_label)
        self.bitrate_layout.add_widget(self.bitrate_choice)
        self.add_widget(self.bitrate_layout)

        # Download button
        download_btn = Button(text="Download", background_color=(0, 1, 0, 1), size_hint_y=0.1)
        download_btn.bind(on_press=self.start_download)
        self.add_widget(download_btn)

        # Status label
        self.status_label = Label(text="", size_hint_y=0.1)
        self.add_widget(self.status_label)

        # Terminal output
        scroll = ScrollView(size_hint_y=0.3)
        self.terminal_output = ScrollableText(readonly=True, size_hint=(1, None), height=150)
        scroll.add_widget(self.terminal_output)
        self.add_widget(scroll)

        # Show file path button
        self.show_path_btn = Button(text="Show File Location", size_hint_y=0.1)
        self.show_path_btn.bind(on_press=self.show_file_path)
        self.show_path_btn.visible = False
        self.add_widget(self.show_path_btn)

    def log_output(self, line):
        self.terminal_output.text += line + '\n'

    def paste_url(self, instance):
        try:
            self.url_input.text = Clipboard.paste()
        except Exception as e:
            self.show_popup("Error", "Unable to paste from clipboard.")

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()

    def update_options(self, spinner, text):
        self.resolution_layout.visible = (text == "Video (MP4)")
        self.bitrate_layout.visible = (text == "Audio (MP3)")
        if text == "Video (MP4)":
            if self.bitrate_layout in self.children:
                self.remove_widget(self.bitrate_layout)
            if self.resolution_layout not in self.children:
                self.add_widget(self.resolution_layout, index=4)
        else:
            if self.resolution_layout in self.children:
                self.remove_widget(self.resolution_layout)
            if self.bitrate_layout not in self.children:
                self.add_widget(self.bitrate_layout, index=4)

    def download_video(self, url, format_choice, resolution, bitrate):
        try:
            self.status_label.text = "Downloading..."
            self.show_path_btn.visible = False
            self.terminal_output.text = ""

            ydl_opts = {
                'outtmpl': f'{self.download_dir}/%(title)s.%(ext)s',
                'ignoreerrors': False,
                'ffmpeg_location': FFMPEG_PATH,
                'noplaylist': False
            }

            if format_choice == "Audio (MP3)":
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': bitrate.replace('k', ''),
                }]
            else:
                resolution_map = {
                    '1080p': 'best[height<=1080][ext=mp4]',
                    '720p': 'best[height<=720][ext=mp4]',
                    '480p': 'best[height<=480][ext=mp4]',
                    '360p': 'best[height<=360][ext=mp4]'
                }
                ydl_opts['format'] = resolution_map.get(resolution, 'best[ext=mp4]')

            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                if isinstance(info, dict) and 'entries' in info:
                    downloaded = len(info['entries'])
                    self.status_label.text = f"Playlist downloaded: {downloaded} items."
                    self.show_path_btn.path = self.download_dir
                else:
                    file_path = ydl.prepare_filename(info)
                    self.show_path_btn.path = file_path
                    if format_choice == "Audio (MP3)":
                        self.status_label.text = f"Download complete: MP3 saved (Bitrate: {bitrate})."
                    else:
                        self.status_label.text = f"Download complete: MP4 saved (Resolution: {resolution})."
                self.show_path_btn.visible = True
                self.add_widget(self.show_path_btn, index=0)

        except Exception as e:
            self.show_popup("Error", f"Download failed: {str(e)}")
            self.status_label.text = ""

    def start_download(self, instance):
        url = self.url_input.text.strip()
        format_choice = self.format_choice.text
        resolution = self.resolution_choice.text
        bitrate = self.bitrate_choice.text

        if not url:
            self.show_popup("Missing URL", "Please enter a YouTube URL.")
            return

        threading.Thread(target=self.download_video, args=(url, format_choice, resolution, bitrate)).start()

    def show_file_path(self, instance):
        path = getattr(self.show_path_btn, 'path', None)
        if path:
            self.show_popup("Saved File", f"Saved to:\n{path}")

class YouTubeDownloaderApp(App):
    def build(self):
        return YouTubeDownloader()

if __name__ == '__main__':
    YouTubeDownloaderApp().run()