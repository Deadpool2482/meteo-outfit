[app]
title = Meteo Outfit
package.name = meteooutfit
package.domain = org.meteo
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 2.1
requirements = python3,kivy==2.3.0,kivymd,requests,urllib3,certifi,chardet,idna
orientation = portrait
fullscreen = 0
android.archs = arm64-v8a
android.api = 34
android.minapi = 21
android.ndk_api = 21
android.enable_androidx = True
android.permissions = INTERNET, ACCESS_FINE_LOCATION, FOREGROUND_SERVICE
[buildozer]
log_level = 2
warn_on_root = 1
