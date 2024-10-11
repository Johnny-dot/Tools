@echo off

:: 激活虚拟环境
call venv\Scripts\activate

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

    :: 手动设置 Scoop 路径，避免依赖环境变量的延迟更新
    set "SCOOP_PATH=%USERPROFILE%\scoop\shims"
    if not exist "%SCOOP_PATH%\scoop.ps1" (
        echo Scoop installation failed. Please check and try again.
        pause
        exit /b 1
    )
    
    :: Scoop 安装完成，继续执行后续步骤
    echo Scoop installed successfully.
) else (
    echo Scoop is already installed.
    set "SCOOP_PATH=%USERPROFILE%\scoop\shims"
)

:: 调试：检查 Scoop 路径
echo SCOOP_PATH is set to: %SCOOP_PATH%

:: 更新 Scoop，手动指定路径来执行 scoop.ps1
echo Updating Scoop...
powershell -ExecutionPolicy RemoteSigned -File "%SCOOP_PATH%\scoop.ps1" update

:: 检查是否已安装 Lua，手动指定路径来执行 scoop.ps1
echo Checking if Lua is installed...
where luac >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Lua is not installed. Installing Lua with Scoop...
    powershell -ExecutionPolicy RemoteSigned -File "%SCOOP_PATH%\scoop.ps1" install lua
) else (
    echo Lua is already installed.
)

:: 检查是否已安装 SVN，手动指定路径来执行 scoop.ps1
echo Checking if SVN is installed...
where svn >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo SVN is not installed. Installing SVN with Scoop...
    powershell -ExecutionPolicy RemoteSigned -File "%SCOOP_PATH%\scoop.ps1" install svn
    
    :: 更新 PATH 环境变量，确保终端可以使用 SVN 命令
    setx PATH "%SCOOP_PATH%;%PATH%" /M
    
    echo SVN installed successfully and added to PATH.
) else (
    echo SVN is already installed and available in PATH.
)

:: 完成
echo Installation complete.
pause
