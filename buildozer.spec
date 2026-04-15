[app]

title = TGCloud
package.name = tgcloud
package.domain = org.tgcloud

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

requirements = python3,kivy

orientation = portrait

# ✅ STABLE CONFIG
android.api = 31
android.minapi = 21

# ✅ NDK STABLE (PENTING)
android.ndk = 25b
android.ndk_api = 21

# ✅ PERMISSION
android.permissions = INTERNET

# ✅ ARCH
android.arch = arm64-v8a