@echo off

:start
::µ±Ç°Ä¿Â¼
set CURR_PATH=%cd%
set ETC=%CURR_PATH%\client_etc_new

echo Input project path:
set /p PROJECT_PATH=

rmdir /s/q %ETC%\code

echo Copy files from %PROJECT_PATH% to client_etc_new ...
xcopy /s/q %PROJECT_PATH%\code %ETC%\code\ /e
copy %PROJECT_PATH%\shader.shr %ETC%\shader.shr

php %CURR_PATH%\resource_filter.php etc

start fancy-dev.exe -d android_etc_new.lua

echo Press Enter to copy %ETC%\res to %PROJECT_PATH%\res_etc_new

pause

echo copy %ETC%\res to %PROJECT_PATH%\res_etc_new ...
rmdir /s/q %PROJECT_PATH%\res_etc_new
xcopy /s/q %ETC%\res %PROJECT_PATH%\res_etc_new\ /e

pause