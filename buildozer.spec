[app]
title = JARVIS
package.name = jarvis
package.domain = org.fahad
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0

# Critical Fix: No spaces after commas
requirements = python3,kivy,groq,tavily-python,requests,certifi,charset-normalizer,idna,urllib3

orientation = portrait
osx.python_version = 3
osx.kivy_version = 1.9.1
fullscreen = 0

# Android specific
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,RECORD_AUDIO
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.skip_update = False

# This is the line that failed in your screenshot - fixed to 'archs'
android.archs = arm64-v8a

android.release_artifact = apk
log_level = 2

[buildozer]
log_level = 2
warn_on_root = 1
