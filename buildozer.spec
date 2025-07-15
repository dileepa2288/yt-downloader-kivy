[app]
title = YouTube Downloader
package.name = youtubedownloader
package.domain = org.ryen
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy==2.3.0,kivymd,yt-dlp,pyjnius
orientation = portrait
fullscreen = 0
osx.kivy_version = 2.3.0

[buildozer]
log_level = 2
warn_on_root = 1
build_dir = .buildozer

[app.android]
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.ndk = 25b
android.archs = armeabi-v7a,arm64-v8a
android.gradle_dependencies = com.android.support:appcompat-v7:28.0.0
android.allow_backup = True
android.hardwareAccelerated = True

[app.android.ndk]
# For better performance, enable this
# use --private storage by default
