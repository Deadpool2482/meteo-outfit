[app]
title = Meteo & Outfit
package.name = meteooutfit
package.domain = org.meteo
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 2.0

# REQUISITI PULITI: Abbiamo rimosso Cython da qui per evitare conflitti
requirements = python3,kivy==2.3.0,kivymd==1.1.1,requests,urllib3,chardet,idna,pillow

icon.filename = %(source.dir)s/icon.png
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 34
android.minapi = 24
android.private_storage = True
android.entrypoint = org.kivy.android.PythonActivity
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# ACCETTAZIONE LICENZE: Fondamentale per non bloccare la build
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
