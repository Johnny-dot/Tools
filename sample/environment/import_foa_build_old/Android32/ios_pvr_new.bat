@echo off

:start
::µ±Ç°Ä¿Â¼
set CURR_PATH=%cd%
set PVR=%CURR_PATH%\client_pvr_new

echo Input project path:
set /p PROJECT_PATH=

rmdir /s/q %PVR%\code

echo Copy files from %PROJECT_PATH% to client_pvr_new\code ...
xcopy /s/q %PROJECT_PATH%\code %PVR%\code\ /e

php %CURR_PATH%\resource_filter.php pvr %PROJECT_PATH%

start fancy-dev.exe -d ios_pvr_new.lua

echo Press Enter to copy %PVR%\res to %PROJECT_PATH%\res_pvr_new

pause

echo copy %PVR%\res to %PROJECT_PATH%\res_pvr_new ...
rmdir /s/q %PROJECT_PATH%\res_pvr_new
xcopy /s/q %PVR%\res %PROJECT_PATH%\res_pvr_new\ /e

pause