[app]
title = JARVIS
package.name = jarvis
package.domain = org.fahad
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0

# Only use packages that p4a can handle
# groq and tavily installed via pip at runtime via requirements.txt
requirements = python3,kivy==2.2.1,openssl,requests

# Add pip packages that cant be compiled normally
android.pip = groq,tavily-python,httpx,anyio,sniffio,distro,pydantic

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,CAMERA,RECORD_AUDIO,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,CALL_PHONE,SEND_SMS,VIBRATE,CHANGE_WIFI_STATE,ACCESS_WIFI_STATE,CHANGE_NETWORK_STATE,ACCESS_NETWORK_STATE,BLUETOOTH,BLUETOOTH_ADMIN,FOREGROUND_SERVICE

android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.sdk = 33
android.accept_sdk_license = True
android.arch = arm64-v8a
android.release_artifact = apk

android.bootstrap = sdl2

log_level = 2
warn_on_root = 1

[buildozer]
log_level = 2
warn_on_root = 1
