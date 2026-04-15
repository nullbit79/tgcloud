[app]

title = TGCloud
package.name = tgcloud
package.domain = org.tgcloud

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

requirements = python3,kivy

orientation = portrait

# 🔥 ANDROID CONFIG (STABIL)
android.api = 31
android.minapi = 21

# 🔥 FIX ERROR SDL (WAJIB)
android.ndk = 25b
android.ndk_api = 21

# 🔥 PERMISSION DASAR
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# 🔥 ARCH
android.arch = arm64-v8a

# (biarkan kosong)
android.build_tools_version =
android.sdk =