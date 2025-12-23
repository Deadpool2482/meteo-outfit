[app]
title = Meteo Outfit
package.name = meteooutfit
package.domain = org.meteo
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 2.2

# QUI ERA L'ERRORE: Ho aggiunto 'pillow' alla lista!
requirements = python3,kivy==2.3.0,kivymd,requests,certifi,urllib3,idna,chardet,pillow

orientation = portrait
fullscreen = 0
android.archs = arm64-v8a
android.api = 34
android.minapi = 21
android.ndk = 25b
android.enable_androidx = True
android.permissions = INTERNET, ACCESS_FINE_LOCATION, FOREGROUND_SERVICE

# Icona (se non hai il file icon.png, commenta questa riga con un # davanti)
# icon.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
warn_on_root = 1
