[app]
# Application name
title = YouTube Downloader

# Package name
package.name = youtubedownloader

# Package domain (can be anything you want, reversed like a domain)
package.domain = org.ryen

# Source directory
source.dir = .

# File types to include
source.include_exts = py,png,jpg,kv,atlas

# Application version
version = 0.1

# Requirements (Kivy, KivyMD, yt-dlp)
requirements = kivy==2.3.0,kivymd,yt-dlp

# Orientation (portrait, landscape, or all)
orientation = portrait

# Fullscreen mode
fullscreen = 0

# Icon (optional): place your icon.png in the root directory
# icon.filename = %(source.dir)s/icon.png

# Presplash (optional): place your presplash.png in the root directory
# presplash.filename = %(source.dir)s/presplash.png

# Supported architectures (modern Android phones use these)
android.archs = arm64-v8a,armeabi-v7a

# Entry point
# If your main file is not main.py, change this
entrypoint = main.py

# Include .kv files even if not explicitly loaded (optional)
# android.include_exts = kv

# (Optional) Add extra Java classes if needed
# android.add_src =

# Additional Python packages from a custom source (optional)
# p4a.source_dir =

[buildozer]
# Verbosity level (0 = quiet, 2 = very verbose)
log_level = 2

# Don't warn when building as root
warn_on_root = 1

# (Optional) Uncomment for faster builds by skipping updates
# update_always = 0

[app.android]
# Android permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Minimum and target SDK versions
android.minapi = 21
android.api = 31

# NDK version
android.ndk = 25b

# Optional: force a specific build tool version (can help with some crashes)
# android.build_tools_version = 34.0.0

# Optional: enable/disable logcat filter for Android
# android.logcat_filters = *:S python:D

# Optional: Java heap size
# android.extra_jvm_args = -Xmx4g

# Optional: extra p4a arguments (if needed)
# p4a.extra_args = --no-copy-libs

# Optional: enable AndroidX (if using newer KivyMD or libraries that require it)
# android.enable_androidx = 1
