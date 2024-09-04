@echo off

:start
::当前目录
set CURR_PATH=%cd%
set ANDROID=%cd%

::打android安装包
:apk
set storename=teayelp
set storepass=tcmj558dudu
set aliasname=teayelp
set keypass=tcmj558dudu
set days=1000000
echo ----------Android apk start----------
echo storename=teayelp
echo storepass=tcmj558dudu
echo aliasname=teayelp
echo keypass=tcmj558dudu
echo days=1000000

cd %ANDROID%

echo Input package name:
set /p package=
set output=%package%.apk

echo package=%package% 
echo output=%output%

cd %ANDROID%

aapt package -f -M AndroidManifest.xml -I android.jar -S res -A assets --rename-manifest-package "com.fancy.%package%" -F unsigned-%output%
aapt add -v unsigned-%output% "lib/armeabi-v7a/libtpnsSecurity.so" "lib/armeabi-v7a/libtpnsWatchdog.so" "lib/armeabi-v7a/libFancy3D.so" "lib/armeabi-v7a/libfmodex.so" classes.dex

jarsigner -verbose -digestalg SHA1 -sigalg MD5withRSA -keystore %storename%.keystore -keypass %keypass% -storepass %storepass% -signedjar unaligned-%output% unsigned-%output% %aliasname%
zipalign -v -f 4 unaligned-%output% %output%

del unsigned-%output%
del unaligned-%output%

cd %CURR_PATH%

echo APK is OK
echo ----------Android apk end----------
