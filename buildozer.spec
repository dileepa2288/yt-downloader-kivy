[app]
title = YouTube Downloader
package.name = youtubedownloader
package.domain = org.ryen
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = kivy==2.3.0,yt-dlp,pyjnius==1.4.0
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
android.archs = arm64-v8a,armeabi-v7a
