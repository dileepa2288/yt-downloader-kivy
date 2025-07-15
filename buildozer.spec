[app]
title = YouTubeDownloader
package.name = youtubedownloader
package.domain = org.example

source.dir = .
source.include_exts = py,kv,png,jpg,atlas
version = 1.0

requirements = python3,kivy==2.3.0,kivymd,yt-dlp,pyjnius

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a,armeabi-v7a

orientation = portrait

# (str) Application entry point
entrypoint = main.py

# Presplash
presplash.filename = %(source.dir)s/data/presplash.png

# Icon
icon.filename = %(source.dir)s/data/icon.png

# (bool) Copy library instead of making a libpymodules.so
copy_libs = 1

# Include .so files for yt-dlp and ffmpeg if needed (manual or via service)

[buildozer]
log_level = 2
warn_on_root = 1
