@echo off

:start
::µ±Ç°Ä¿Â¼
set CURR_PATH=%cd%
set PVR=%CURR_PATH%\client_pvr

echo Input project path:
set /p PROJECT_PATH=

rmdir /s/q %PVR%

echo Copy files from %PROJECT_PATH% to client_pvr ...
xcopy /s/q %PROJECT_PATH%\res %PVR%\res\ /e
xcopy /s/q %PROJECT_PATH%\code %PVR%\code\ /e

start fancy-dev.exe -d ios_pvr1.lua

Press Enter to copy %PVR%\res to %PROJECT_PATH%\res_pvr1

pause

echo copy %PVR%\res to %PROJECT_PATH%\res_pvr ...
rmdir /s/q %PROJECT_PATH%\res_pvr1
xcopy /s/q %PVR%\res %PROJECT_PATH%\res_pvr1\ /e

pause