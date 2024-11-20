import pkgutil
import os
import re
from PyInstaller.utils.hooks import collect_submodules

# 获取项目根目录路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../"))

# 虚拟环境路径和 .spec 文件路径使用相对路径
venv_path = os.path.join(project_root, 'venv')
spec_file = os.path.join(current_dir, 'mainwindow.spec')

# 获取所有已安装的包的名称，包括项目目录
def get_installed_packages(venv_path, project_root):
    packages = []
    search_paths = [
        os.path.join(venv_path, 'Lib', 'site-packages'),
        project_root  # 添加项目根目录到搜索路径
    ]
    for search_path in search_paths:
        for _, name, _ in pkgutil.iter_modules([search_path]):
            packages.append(name)
    return packages

# 修改 .spec 文件中的 hiddenimports
def update_hiddenimports_in_spec_file(spec_file, hidden_imports):
    with open(spec_file, 'r', encoding='utf-8') as file:
        spec_content = file.read()

    # 将 hidden_imports 列表转换为字符串
    hidden_imports_str = repr(hidden_imports) + ','

    # 使用正则表达式匹配 hiddenimports= 的部分
    hiddenimports_pattern = r'(hiddenimports\s*=\s*\[.*?\],)'
    new_hiddenimports = f'hiddenimports={hidden_imports_str}'

    if re.search(hiddenimports_pattern, spec_content, re.DOTALL):
        # 替换已有的 hiddenimports
        spec_content = re.sub(hiddenimports_pattern, new_hiddenimports, spec_content, flags=re.DOTALL)
    else:
        # 没有找到，则在 a = Analysis( 之后插入
        analysis_pattern = r'(a\s*=\s*Analysis\()'
        spec_content = re.sub(analysis_pattern, r'\1\n    ' + new_hiddenimports, spec_content, count=1)

    with open(spec_file, 'w', encoding='utf-8') as file:
        file.write(spec_content)

# 更新 .spec 文件中的 datas 参数
def update_datas_in_spec_file(spec_file, datas_list):
    with open(spec_file, 'r', encoding='utf-8') as file:
        spec_content = file.read()

    # 构建 datas 字符串
    datas_items = []
    for src, dest in datas_list:
        # 替换反斜杠并添加到列表
        src_fixed = src.replace('\\', '/')
        dest_fixed = dest.replace('\\', '/')
        datas_items.append(f"('{src_fixed}', '{dest_fixed}')")
    datas_str = 'datas=[\n    ' + ',\n    '.join(datas_items) + '\n],'

    # 使用正则表达式匹配 datas= 的部分
    datas_pattern = r'(datas\s*=\s*\[.*?\],)'
    if re.search(datas_pattern, spec_content, re.DOTALL):
        # 替换已有的 datas
        spec_content = re.sub(datas_pattern, datas_str, spec_content, flags=re.DOTALL)
    else:
        # 没有找到，则在 a = Analysis( 之后插入
        analysis_pattern = r'(a\s*=\s*Analysis\()'
        spec_content = re.sub(analysis_pattern, r'\1\n    ' + datas_str, spec_content, count=1)

    with open(spec_file, 'w', encoding='utf-8') as file:
        file.write(spec_content)

# 定义函数，收集需要的文件并排除 .ui 文件
def get_datas_without_ui(source_dir, target_dir):
    datas = []
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if not file.endswith('.ui'):
                src_file = os.path.abspath(os.path.join(root, file))
                rel_path = os.path.relpath(root, source_dir)
                dest_dir = os.path.normpath(os.path.join(target_dir, rel_path))
                datas.append((src_file, dest_dir))
    return datas

# 获取所有安装的包，包括项目目录
hidden_imports = get_installed_packages(venv_path, project_root)

# # 显式添加 tkinter
# hidden_imports.append('tkinter')
# 显式添加 tkinter 及其子模块
hidden_imports.append('tkinter')
hidden_imports.append('tkinter.filedialog')
hidden_imports.append('tkinter.simpledialog')
hidden_imports.append('tkinter.messagebox')
hidden_imports.append('tkinter.ttk')
hidden_imports.append('tkinter.scrolledtext')


# 收集 sample.src_references 的所有子模块
hidden_imports += collect_submodules('sample.src_references')

# 更新 .spec 文件中的 hiddenimports
update_hiddenimports_in_spec_file(spec_file, hidden_imports)

# 收集需要的 datas（排除 .ui 文件）
qt_source_dir = os.path.abspath(os.path.join(current_dir, '../sample/qt'))
qt_target_dir = 'sample/qt'  # 相对于打包输出目录

qt_datas = get_datas_without_ui(qt_source_dir, qt_target_dir)

# 添加 '../src_references' 目录
src_references_dir = os.path.abspath(os.path.join(current_dir, '../sample/src_references'))
src_references_datas = [(src_references_dir.replace('\\', '/'), 'sample/src_references')]

# 合并 datas 列表
datas_list = qt_datas + src_references_datas

# 更新 .spec 文件中的 datas
update_datas_in_spec_file(spec_file, datas_list)

print("Spec file updated with hidden imports and datas.")
