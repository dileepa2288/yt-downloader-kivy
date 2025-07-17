[app]
# (str) Title of your application
title = YouTube Downloader

# (str) Package name
package.name = youtubedownloader

# (str) Package domain (needed for Android/iOS packaging)
package.domain = org.ryen

# (str) Source code directory (relative to this file)
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,kv,png,jpg,jpeg,txt,md

# (str) Version of your application
version = 0.1

# (list) Application requirements
# Ensure compatibility with Kivy 2.3.0 and your dependencies
requirements = python3,kivy==2.3.0,yt-dlp,ffmpeg-python,pyjnius @ git+https://github.com/kivy/pyjnius.git@5a1b27d7d3bdee6cedb55440bfae9c4e66fb3c68

# (str) Supported orientation (one of portrait, landscape or all)
orientation = portrait

# (bool) Make the app fullscreen by default
fullscreen = 0

[buildozer]
# (int) Log level (0 = nothing, 1 = error, 2 = info, 3 = debug)
log_level = 2

# (bool) Display a warning if running as root (0 = no, 1 = yes)
warn_on_root = 1

[app.android]
# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Android API to use
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android SDK path (set by workflow, leave commented unless manual override)
# android.sdk_path = /home/runner/.buildozer/android/platform/android-sdk

# (str) Android NDK path (set by workflow, leave commented unless manual override)
# android.ndk_path = /home/runner/.buildozer/android/platform/android-ndk-r25b

# (list) Android archs to build (choose from arm64-v8a, armeabi-v7a, x86, x86_64)
android.archs = arm64-v8a,armeabi-v7a
