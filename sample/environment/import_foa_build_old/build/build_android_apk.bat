set CURR_PATH=%cd%
set ANDROID=%CURR_PATH%/android/

cd %ANDROID%

aapt package -f -M AndroidManifest.xml -I android.jar -S res -A assets -F unsigned-xa.apk
aapt add -v unsigned-xa.apk "lib/armeabi-v7a/libtpnsSecurity.so" "lib/armeabi-v7a/libtpnsWatchdog.so" "lib/armeabi-v7a/libFancy3D.so" "lib/armeabi-v7a/libfmodex.so" classes.dex

jarsigner -verbose -digestalg SHA1 -sigalg MD5withRSA -keystore teayelp.keystore -keypass tcmj558dudu -storepass tcmj558dudu -signedjar unaligned-xa.apk unsigned-xa.apk teayelp
zipalign -v -f 4 unaligned-xa.apk xxx.apk

del unsigned-xa.apk
del unaligned-xa.apk

