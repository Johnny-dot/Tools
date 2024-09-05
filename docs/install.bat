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

    :: 手动更新环境变量以便立即识别 scoop 命令
    echo Refreshing environment variables...
    setx PATH "%USERPROFILE%\scoop\shims;%PATH%"

    :: 重新加载命令行环境
    echo Reloading command prompt...
    start "" /wait cmd /c "%~f0"
    pause
    goto :eof
) else (
    echo Scoop is already installed.
)

:: 更新 Scoop
echo Updating Scoop...
scoop update

:: 检查是否已安装 Lua
echo Checking if Lua is installed...
where luac >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Lua is not installed. Installing Lua with Scoop...
    scoop install lua
) else (
    echo Lua is already installed.
)

:: 完成
echo Installation complete.
pause
