[app]

# Titolo e metadati
title = Waiter Dashboard
package.name = waiterdashboard
package.domain = org.fedebosetti
version = 1.0

# Configurazione sorgenti
source.dir = .
source.include_exts = py,kv,json  # Solo estensioni necessarie

# Orientamento e display
orientation = landscape
fullscreen = 1

# Android specific
android.permissions = INTERNET,VIBRATE
android.minapi = 21
android.api = 31
android.ndk = 23b
android.arch = armeabi-v7a, arm64-v8a

# Requirements ottimizzati
requirements = 
    python3,
    kivy,
    websockets,
    asyncio,
    android

# Build settings
p4a.branch = master
log_level = 2

[buildozer]
log_level = 2
warn_on_root = 0