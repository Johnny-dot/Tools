@echo off

:start

:menu
echo.
echo  select dev type 
echo.
echo  [1] dev
echo  [2] test
echo  [3] neice
echo  [4] yinqing1
echo  [5] yinqing2
echo  [6] music
echo.

:choice
set /P C=[Choice]: 
echo.
if %C%==1 goto dev
if %C%==2 goto test
if %C%==3 goto neice
if %C%==4 goto yinqing1
if %C%==5 goto yinqing2
if %C%==6 goto music

:dev
php android.php dev
goto start

:test
php android.php test
goto start

:neice
php android.php neice
goto start

:yinqing1
php android.php yinqing1
goto start

:yinqing2
php android.php yinqing2
goto start

:music
php android.php music
goto start