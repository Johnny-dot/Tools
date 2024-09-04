如何部署编译环境？
1.首先需要安装python环境，工具python版本为3.9.13；
https://www.python.org/downloads/release/python-3913/
2.双击install.bat来安装requirements.txt中的库依赖；
3.打开../Tools/sample/gui/mainwindow.spec文件，需留意其中的路径。在QT工程不新增子文件的情况下，只需要注意修改盘符路径为此电脑上工具路径即可；
4.双击../Tools/sample/gui/rebuild.bat文件，构建后的exe将会输出到../Tools/sample/gui/dist文件夹中；
5.将新构建的可执行程序放在Tools根目录下，否则会影响工具配置中，对相对环境的判断错误。