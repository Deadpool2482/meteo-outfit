[app]

# (str) Title of your application
title = Meteo & Outfit

# (str) Package name
package.name = meteooutfit

# (str) Package domain (needed for android/ios packaging)
package.domain = org.meteo

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 2.0

# (list) Application requirements
# ABBIAMO RIMOSSO CYTHON SPECIFICO: Kivy 2.3.0 si gestirà da solo le dipendenze
requirements = python3,kivy==2.3.0,kivymd==1.1.1,requests,urllib3,chardet,idna,pillow

# (str) Icon of the application
icon.filename = %(source.dir)s/icon.png

# (list) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 34

# (int) Minimum API your APK / AAB will support.
android.minapi = 24

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android entry point, default is ok for Kivy-based app
android.entrypoint = org.kivy.android.PythonActivity

# (list) The Android archs to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (bool) If True, then automatically accept SDK license agreements.
# QUESTO È FONDAMENTALE PER EVITARE L'ERRORE "BROKEN PIPE"
android.accept_sdk_license = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
