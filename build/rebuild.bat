@echo off
REM 切换到批处理文件所在目录
cd /d %~dp0

REM 返回到项目根目录
cd ..

REM 激活虚拟环境
call venv\Scripts\activate

REM 使用虚拟环境的 Python 解释器运行 PyInstaller
python build\AutoCollect.py

REM 使用虚拟环境的 Python 解释器打包
python -m PyInstaller --distpath "." build\mainwindow.spec

REM 提示完成
echo Build complete! Press any key to exit.
pause

