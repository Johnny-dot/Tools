@echo off

:start
::µ±Ç°Ä¿Â¼
set CURR_PATH=%cd%
set TEMP=%CURR_PATH%\temp\

echo ----------foa start----------
set TIME=%date:~0,4%%date:~5,2%%date:~8,2%%time:~0,2%%time:~3,2%%time:~6,2%
echo %TIME%

echo Input project path:
set /p PROJECT_PATH=

echo desc=  !!!!!!(Must be English or pinyin)!!!!!!
set /p DESC=

:menu
echo.
echo  select ouput type
echo.
echo  [1] android   release     (output 2 foa)
echo  [2] android   debug       (output 1 foa)
echo  [3] ios       release     (output 2 foa)
echo  [4] ios       debug       (output 1 foa)
echo  [5] all       release     (output 4 foa)
echo  [6] all       debug       (output 2 foa)
echo.

:choice
set /P C=[Choice]: 
echo.
if %C%==1 goto ouput1
if %C%==2 goto ouput2
if %C%==3 goto ouput3
if %C%==4 goto ouput4
if %C%==5 goto ouput5
if %C%==6 goto ouput6

:ouput1
set DEV=android
set DEBUG=false
goto:menu2

:ouput2
set DEV=android
set DEBUG=true
goto:menu2

:ouput3
set DEV=ios
set DEBUG=false
goto:menu2

:ouput4
set DEV=ios
set DEBUG=true
goto:menu2

:ouput5
set DEV=all
set DEBUG=false
goto:menu2

:ouput6
set DEV=all
set DEBUG=true
goto:menu2

:menu2
:menu
echo.
echo  select dev type 
echo.
echo  [1] dev
echo  [2] test
echo  [3] neice
echo  [4] yinqing
echo  [5] kb
echo  [6] youzu
echo  [6] banshu
echo.

:choice
set /P C=[Choice]: 
echo.
if %C%==1 goto dev
if %C%==2 goto test
if %C%==3 goto neice
if %C%==4 goto yinqing
if %C%==5 goto kb
if %C%==6 goto youzu
if %C%==7 goto banshu

:dev
php build_foa.php dev %PROJECT_PATH% %DESC% %DEV% %DEBUG%
goto start

:test
php build_foa.php test %PROJECT_PATH% %DESC% %DEV% %DEBUG%
goto start

:neice
php build_foa.php neice %PROJECT_PATH% %DESC% %DEV% %DEBUG%
goto start

:yinqing
php build_foa.php yinqing %PROJECT_PATH% %DESC% %DEV% %DEBUG%
goto start

:kb
php build_foa.php kb %PROJECT_PATH% %DESC% %DEV% %DEBUG%
goto start

:youzu
php build_foa.php youzu %PROJECT_PATH% %DESC% %DEV% %DEBUG%
goto start

:banshu
php build_foa.php banshu %PROJECT_PATH% %DESC% %DEV% %DEBUG%
goto start
