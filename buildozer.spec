[app]

title = 智能班级管理
package.name = rollcall
package.domain = org.rollcall
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

orientation = portrait

android.api = 33
android.ndk = 25b
android.sdk = 24

android.add_assets = 
android.add_jars =
android.add_apk =

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

android.icon = %(source.dir)s/icon.png
android.app_name = 智能班级管理

android.buildtools = 33.0.0

requirements = python3,kivy==2.1.0

[buildozer]
log_level = 2
warn_on_root = 1
