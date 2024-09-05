@echo off

:: 检查并安装 Python 依赖
echo Installing Python dependencies from requirements.txt...
pip install -r requirements.txt

:: 检查是否已安装 Scoop
echo Checking if Scoop is installed...
where scoop >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Scoop is not installed. Installing Scoop...
    powershell -Command "Set-ExecutionPolicy RemoteSigned -scope CurrentUser"
    powershell -Command "iwr -useb get.scoop.sh | iex"
    
    :: 设置 Scoop 的路径
    set "SCOOP_PATH=%USERPROFILE%\scoop\shims"

    :: 手动添加 Scoop 路径，安装完成后需要用户重新运行脚本
    echo Scoop has been installed. Please close and reopen this command prompt, then run this script again to complete the Lua installation.
    pause
    exit /b 0
) else (
    echo Scoop is already installed.
)

:: 确保 Scoop 路径可用
set "SCOOP_PATH=%USERPROFILE%\scoop\shims"
if not exist "%SCOOP_PATH%\scoop.exe" (
    echo Scoop path not found. Please ensure that Scoop is installed correctly.
    pause
    exit /b 1
)

:: 更新 Scoop
echo Updating Scoop...
"%SCOOP_PATH%\scoop.exe" update

:: 检查是否已安装 Lua
echo Checking if Lua is installed...
where luac >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Lua is not installed. Installing Lua with Scoop...
    "%SCOOP_PATH%\scoop.exe" install lua
) else (
    echo Lua is already installed.
)

:: 完成
echo Installation complete.
pause
