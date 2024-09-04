@echo off

:start
::µ±Ç°Ä¿Â¼
set CURR_PATH=%cd%
set ETC=%CURR_PATH%\client_etc

echo Input project path:
set /p PROJECT_PATH=

rmdir /s/q %ETC%

echo Copy files from %PROJECT_PATH% to client_etc ...
xcopy /s/q %PROJECT_PATH%\res %ETC%\res\ /e
xcopy /s/q %PROJECT_PATH%\code %ETC%\code\ /e
copy %PROJECT_PATH%\shader.shr %ETC%\shader.shr

start fancy-dev.exe -d android_etc.lua

Press Enter to copy %ETC%\res to %PROJECT_PATH%\res_etc

pause

echo copy %ETC%\res to %PROJECT_PATH%\res_etc ...
rmdir /s/q %PROJECT_PATH%\res_etc
xcopy /s/q %ETC%\res %PROJECT_PATH%\res_etc\ /e

pause