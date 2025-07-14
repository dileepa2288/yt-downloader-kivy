[app]
title = YouTube Downloader
package.name = youtubedownloader
package.domain = org.ryen
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy==2.3.0,yt-dlp,pyjnius @ git+https://github.com/kivy/pyjnius.git@5a1b27d7d3bdee6cedb55440bfae9c4e66fb3c68
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[app.android]
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.ndk = 25b

# Comment out these two lines unless you are using a self-hosted runner with these installed
# android.ndk_path = /home/ryen/.buildozer/android/platform/android-ndk-r25b
# android.sdk_path = /home/ryen/.buildozer/android/platform/android-sdk

android.archs = arm64-v8a,armeabi-v7a
