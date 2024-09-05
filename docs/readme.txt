如何部署编译环境？

1. 首先需要安装 Python 环境，工具 Python 版本为 3.9.13；
   https://www.python.org/downloads/release/python-3913/

2. Lua 环境的安装：
   工具依赖于 Lua 解释器。`install.bat` 脚本会自动检查并安装 Lua 环境。如果你正在使用 Windows，`install.bat` 将会自动安装 Scoop 包管理器（如果尚未安装），并使用 Scoop 安装 Lua。请确保你的系统可以执行 PowerShell 脚本。
   
   对于其他操作系统，请参考以下安装指引：
   - **Linux**: 使用包管理工具安装 Lua，例如：
     ```bash
     sudo apt-get update
     sudo apt-get install lua5.3
     ```
   - **macOS**: 使用 Homebrew 来安装 Lua:
     ```bash
     brew install lua
     ```

3. 双击 `install.bat` 来安装 `requirements.txt` 中的库依赖，并同时自动安装 Scoop 和 Lua（仅限 Windows）。

4. 打开 `../Tools/sample/gui/mainwindow.spec` 文件，需留意其中的路径。在 QT 工程不新增子文件的情况下，只需要注意修改盘符路径为此电脑上工具路径即可。

5. 双击 `../Tools/sample/gui/rebuild.bat` 文件，构建后的 exe 将会输出到 `../Tools/sample/gui/dist` 文件夹中。

6. 将新构建的可执行程序放在 `Tools` 根目录下，否则会影响工具配置中对相对环境的判断错误。
