[app]
title = YouTube Downloader
package.name = youtubedownloader
package.domain = org.ryen
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3==3.10, kivy==2.3.0, yt-dlp, pyjnius @ git+https://github.com/kivy/pyjnius.git@5a1b27d7d3bdee6cedb55440bfae9c4e66fb3c68
orientation = portrait
fullscreen = 0

# Permissions your app needs
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Set correct Android API and build tools
android.api = 34
android.minapi = 21
android.build_tools_version = 36.0.0

# Architectures (arm64-v8a for most phones)
android.archs = arm64-v8a,armeabi-v7a

# Don't touch this unless needed
android.ndk = 25b

# Optional icons (skip if you don't have)
# icon.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
warn_on_root = 1
