
########################################
# Buildozer configuration
########################################

[buildozer]
log_level = 2
warn_on_root = 1


########################################
# Application configuration
########################################

[app]
# App title (shown on phone)
title = Android Network Scanner

# Package name (NO spaces, lowercase only)
package.name = networkscanner

# Package domain (reverse domain)
package.domain = org.example

# Source code directory
source.dir = .

# File types to include
source.include_exts = py,png,jpg,jpeg,kv,atlas,json

# App version
version = 0.1

# Python & libraries (KEEP SIMPLE FIRST)
requirements = python3,kivy

# App orientation
orientation = portrait

# Fullscreen mode
fullscreen = 0

# App icon (optional)
# icon.filename = icon.png


########################################
# Android-specific configuration
########################################

# Target architectures (UPDATED – no deprecated token)
android.archs = arm64-v8a,armeabi-v7a

# Android API levels
android.api = 33
android.minapi = 21

# Android NDK version (STABLE)
android.ndk = 25b

# Enable AndroidX
android.enable_androidx = True

# Permissions (add only what you need)
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE

# Optional: Keep logs visible for debugging
android.logcat_filters = *:S python:D

# Optional: Prevent stripping (helps debugging crashes)
android.debuggable = True


########################################
# Build options (safe defaults)
########################################

# Use Gradle (default)
android.gradle_dependencies = com.android.tools.build:gradle:8.1.1

# Do not clean automatically
android.skip_update = False
