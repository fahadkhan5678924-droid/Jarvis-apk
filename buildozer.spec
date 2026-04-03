[app]
title = JARVIS
package.name = jarvis
package.domain = org.fahad
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0
requirements = python3,kivy,groq,tavily-python,requests,certifi,charset-normalizer,idna,urllib3
orientation = portrait
osx.python_version = 3
osx.kivy_version = 1.9.1
fullscreen = 0
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,CAMERA,RECORD_AUDIO,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,CALL_PHONE,SEND_SMS,READ_SMS,RECEIVE_SMS,VIBRATE,FLASHLIGHT,CHANGE_WIFI_STATE,ACCESS_WIFI_STATE,CHANGE_NETWORK_STATE,ACCESS_NETWORK_STATE,BLUETOOTH,BLUETOOTH_ADMIN,RECEIVE_BOOT_COMPLETED,FOREGROUND_SERVICE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a
android.release_artifact = apk
log_level = 2
warn_on_root = 1

[buildozer]
log_level = 2
warn_on_root = 1
