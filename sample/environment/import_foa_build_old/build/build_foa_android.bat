@echo off

:start
::当前目录
set CURR_PATH=%cd%
set TEMP=%CURR_PATH%\temp\

goto foa

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

echo desc=  !!!!!!(Must be English or pinyin)!!!!!!
set /p DESC=

echo outpath=%TIME%_%SVN%_%DESC%
set OUTPATH=%TIME%_%SVN%_%DESC%

goto foa_create_version

:foa_create_version
@echo svn = '%SVN%' > version.lua
@echo time = '%TIME%' >> version.lua
@echo desc =  ' : %DESC%  ' >> version.lua
@echo version = %SVN% >> version.lua
@echo outpath = '%OUTPATH%' >> version.lua
@echo versionName = '' >> version.lua
@echo mainPlugin = 'plugin.fob' >> version.lua
@echo name = 'rg' >> version.lua
@echo path = 'temp' >> version.lua
@echo out = 'output/' .. outpath >> version.lua
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
move version.lua output\%OUTPATH%\version.lua
@echo svn = '%SVN%' > version.lua
@echo time = '%TIME%' >> version.lua
@echo desc =  ' : %DESC%  ' >> version.lua
@echo version = %SVN% >> version.lua
@echo versionName = '' >> version.lua
@echo mainPlugin = 'plugin.fob' >> version.lua
@echo name = 'rg' >> version.lua
@echo path = 'temp' >> version.lua
@echo out = 'output/' .. version >> version.lua
@echo code = 'code/main.lua' >> version.lua
goto foa_end

:foa_end
echo ----------foa end----------