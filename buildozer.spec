[app]

# App title and package
title = Network Security Scanner
package.name = networkscanner
package.domain = org.network.scanner

# Source code
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
source.exclude_exts = spec,pyc,pyo
source.exclude_dirs = tests, bin, .buildozer

# Version
version = 1.0

# Requirements
requirements = python3,kivy==2.1.0,psutil,requests

# Android specific
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE
android.api = 30
android.minapi = 21
android.sdk = 30
android.ndk = 23b
android.ndk_api = 21

# Build settings
android.arch = arm64-v8a,armeabi-v7a
p4a.branch = master
android.accept_sdk_license = True

# Orientation
orientation = portrait
fullscreen = 0

# Log level
log_level = 2

# Presplash
presplash.filename = %(source.dir)s/presplash.png
icon.filename = %(source.dir)s/icon.png

# Window size
window.size = 400, 700