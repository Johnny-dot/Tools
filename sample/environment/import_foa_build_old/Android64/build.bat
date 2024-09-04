@echo off

:start
::当前目录
set CURR_PATH=%cd%
set PREBUILD=%CURR_PATH%\prebuild\
set ANDROID=%CURR_PATH%\android\
set TEMP=%CURR_PATH%\temp\

:menu
echo.
echo  select package type 
echo.
echo  [1] foa
echo  [2] apk
echo  [0] exit
echo.

:choice
set /P C=[Choice]: 
echo.
if %C%==1 goto foa
if %C%==2 goto apk
if %C%==0 exit

::项目路径不存在
:error1
echo [Error] The project path is not exist!
echo.
goto start

::获取项目所在路径
:foa
echo ----------foa start----------
set TIME=%date:~0,4%%date:~5,2%%date:~8,2%%time:~0,2%%time:~3,2%%time:~6,2%

echo Input project path:
set /p PROJECT_PATH=

echo version=%TIME%
set VERSION=%TIME%

echo time=%TIME%

echo svn=
set /p SVN=

echo desc=
set /p DESC=

goto foa_create_version

:foa_create_version
@echo svn = '%SVN%' > version.lua
@echo time = '%TIME%' >> version.lua
@echo desc =  ' : %DESC%  ' >> version.lua
@echo version = '%TIME%' >> version.lua
@echo versionName = '' >> version.lua
@echo mainPlugin = 'plugin.fob' >> version.lua
@echo name = 'rg' >> version.lua
@echo path = 'temp' >> version.lua
@echo out = 'output/' .. version >> version.lua
@echo code = 'code/main.lua' >> version.lua
goto foa_android

:foa_android
@echo foaName = 'afoa' >> version.lua

rmdir /s/q %TEMP%

echo Copy files from %PROJECT_PATH% to temp ...
xcopy /s/q %PROJECT_PATH%\res %TEMP%\res\ /e 
xcopy /s/q %PROJECT_PATH%\code %TEMP%\code\ /e 
copy %PROJECT_PATH%\shader.shr %TEMP%\shader.shr

rmdir /s/q jit
del /q luajit.exe
xcopy luajit200 %cd% /e

fancy-dev.exe
move version.lua output\%VERSION%\version.lua
@echo svn = '%SVN%' > version.lua
@echo time = '%TIME%' >> version.lua
@echo desc =  ' : %DESC%  ' >> version.lua
@echo version = '%TIME%' >> version.lua
@echo versionName = '' >> version.lua
@echo mainPlugin = 'plugin.fob' >> version.lua
@echo name = 'rg' >> version.lua
@echo path = 'temp' >> version.lua
@echo out = 'output/' .. version >> version.lua
@echo code = 'code/main.lua' >> version.lua
goto foa_ios

:foa_ios
@echo foaName = 'foa' >> version.lua

rmdir /s/q %TEMP%
echo Copy files from %PROJECT_PATH% to temp ...
xcopy /s/q %PROJECT_PATH%\res %TEMP%\res\ /e 
xcopy /s/q %PROJECT_PATH%\code %TEMP%\code\ /e 
copy %PROJECT_PATH%\shader.shr %TEMP%\shader.shr

rmdir /s/q jit
del /q luajit.exe
xcopy luajit201 %cd% /e

fancy-dev.exe
move version.lua output\%VERSION%\version.lua
@echo svn = '%SVN%' > version.lua
@echo time = '%TIME%' >> version.lua
@echo desc =  ' : %DESC%  ' >> version.lua
@echo version = '%TIME%' >> version.lua
@echo versionName = '' >> version.lua
@echo mainPlugin = 'plugin.fob' >> version.lua
@echo name = 'rg' >> version.lua
@echo path = 'temp' >> version.lua
@echo out = 'output/' .. version >> version.lua
@echo code = 'code/main.lua' >> version.lua
goto foa_end

:foa_end
echo ----------foa end----------
goto start

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

echo !!!!!!!!!please check fancy-dev.cfg !!!!!!!!!!!
set /p z=

echo !!!!!!!!!please check application name !!!!!!!!!!!
set /p z=

echo foa url = :
set /p FOA_URL=


@echo foaurl = '%FOA_URL%' > url.lua
@echo swfurl = 'loading.swf' >> url.lua
@echo fodname = 'rg' >> url.lua
@echo _sys.showVersion = false >> url.lua
@echo _sys.showStat = false >> url.lua
@echo _sys.showMemory = false >> url.lua
@echo mainurl = 'code/main.lua' >> url.lua

echo -------------------
echo foaurl = '%FOA_URL%'
echo swfurl = 'loading.swf'
echo fodname = 'rg'
echo mainurl = 'code/main.lua'
echo write to file url.lua
echo -------------------

echo Input package name:
set /p package=
set output=%package%.apk

echo package=%package% 
echo output=%output%

del /q %ANDROID%\assets\loader.fod\url.lua
move url.lua %ANDROID%\assets\loader.fod\url.lua

cd %ANDROID%

aapt package -f -M AndroidManifest.xml -I android.jar -S res -A assets --rename-manifest-package "com.Fancy.%package%" -F unsigned-%output%
aapt add -v unsigned-%output% "lib/armeabi-v7a/libtpnsSecurity.so" "lib/armeabi-v7a/libtpnsWatchdog.so" "lib/armeabi-v7a/libFancy3D.so" "lib/armeabi-v7a/libfmodex.so" classes.dex

jarsigner -verbose -digestalg SHA1 -sigalg MD5withRSA -keystore %storename%.keystore -keypass %keypass% -storepass %storepass% -signedjar unaligned-%output% unsigned-%output% %aliasname%
zipalign -v -f 4 unaligned-%output% %output%

del unsigned-%output%
del unaligned-%output%

del /q ..\output\%output%
move %output% ..\output\%output%

cd %CURR_PATH%

echo APK is OK
echo ----------Android apk end----------
goto start
