[app]

title = Phone Inspector
package.name = phoneinspector
package.domain = org.local

source.dir = .
source.include_exts = py,kv,txt

version = 0.1

requirements = python3,kivy

orientation = portrait

fullscreen = 1

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

android.api = 33
android.minapi = 21

android.sdk = 33
android.ndk = 25b

android.accept_sdk_license = True

log_level = 2
