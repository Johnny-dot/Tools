# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['../Main.py'],
    binaries=[],
    datas=[
    ('E:/kuangbao/Tools2/sample/qt/res/KBTools.ico', 'sample/qt/res'),
    ('E:/kuangbao/Tools2/sample/qt/src/ui_mainwindow.py', 'sample/qt/src'),
    ('E:/kuangbao/Tools2/sample/qt/src/common/Enum.py', 'sample/qt/src/common'),
    ('E:/kuangbao/Tools2/sample/qt/src/common/__pycache__/Enum.cpython-39.pyc', 'sample/qt/src/common/__pycache__'),
    ('E:/kuangbao/Tools2/sample/qt/src/common/__pycache__/Worker.cpython-39.pyc', 'sample/qt/src/common/__pycache__'),
    ('E:/kuangbao/Tools2/sample/qt/src/pyui/BatchBuildDialog.py', 'sample/qt/src/pyui'),
    ('E:/kuangbao/Tools2/sample/qt/src/pyui/DragListWidget.py', 'sample/qt/src/pyui'),
    ('E:/kuangbao/Tools2/sample/qt/src/pyui/GridProgressBar.py', 'sample/qt/src/pyui'),
    ('E:/kuangbao/Tools2/sample/qt/src/pyui/QTextEditLogger.py', 'sample/qt/src/pyui'),
    ('E:/kuangbao/Tools2/sample/qt/src/pyui/__pycache__/BatchBuildDialog.cpython-39.pyc', 'sample/qt/src/pyui/__pycache__'),
    ('E:/kuangbao/Tools2/sample/qt/src/pyui/__pycache__/DragListWidget.cpython-39.pyc', 'sample/qt/src/pyui/__pycache__'),
    ('E:/kuangbao/Tools2/sample/qt/src/pyui/__pycache__/GridProgressBar.cpython-39.pyc', 'sample/qt/src/pyui/__pycache__'),
    ('E:/kuangbao/Tools2/sample/qt/src/pyui/__pycache__/QTextEditLogger.cpython-39.pyc', 'sample/qt/src/pyui/__pycache__'),
    ('E:/kuangbao/Tools2/sample/qt/src/widget/BranchCoverWidget.py', 'sample/qt/src/widget'),
    ('E:/kuangbao/Tools2/sample/qt/src/widget/DebugAnalysisWidget.py', 'sample/qt/src/widget'),
    ('E:/kuangbao/Tools2/sample/qt/src/widget/DetectDuplicateFilesWidget.py', 'sample/qt/src/widget'),
    ('E:/kuangbao/Tools2/sample/qt/src/widget/FilesMD5Snapshot.py', 'sample/qt/src/widget'),
    ('E:/kuangbao/Tools2/sample/qt/src/widget/FoaBuildWidget.py', 'sample/qt/src/widget'),
    ('E:/kuangbao/Tools2/sample/qt/src/widget/FoaDetectWidget.py', 'sample/qt/src/widget'),
    ('E:/kuangbao/Tools2/sample/qt/src/widget/QuicParasAddTips.py', 'sample/qt/src/widget'),
    ('E:/kuangbao/Tools2/sample/qt/src/widget/ResConvertWidget.py', 'sample/qt/src/widget'),
    ('E:/kuangbao/Tools2/sample/qt/src/widget/ui_BranchCoverWidget.py', 'sample/qt/src/widget'),
    ('E:/kuangbao/Tools2/sample/qt/src/widget/ui_DebugAnalysisWidget.py', 'sample/qt/src/widget'),
    ('E:/kuangbao/Tools2/sample/qt/src/widget/ui_DetectDuplicateFilesWidget.py', 'sample/qt/src/widget'),
    ('E:/kuangbao/Tools2/sample/qt/src/widget/ui_FilesMD5Snapshot.py', 'sample/qt/src/widget'),
    ('E:/kuangbao/Tools2/sample/qt/src/widget/ui_FoaBuildWidget.py', 'sample/qt/src/widget'),
    ('E:/kuangbao/Tools2/sample/qt/src/widget/ui_FoaDetectWidget.py', 'sample/qt/src/widget'),
    ('E:/kuangbao/Tools2/sample/qt/src/widget/ui_QuicParasAddTips.py', 'sample/qt/src/widget'),
    ('E:/kuangbao/Tools2/sample/qt/src/widget/ui_ResConvertWidget.py', 'sample/qt/src/widget'),
    ('E:/kuangbao/Tools2/sample/qt/src/widget/__pycache__/BranchCoverWidget.cpython-39.pyc', 'sample/qt/src/widget/__pycache__'),
    ('E:/kuangbao/Tools2/sample/qt/src/widget/__pycache__/DebugAnalysisWidget.cpython-39.pyc', 'sample/qt/src/widget/__pycache__'),
    ('E:/kuangbao/Tools2/sample/qt/src/widget/__pycache__/DetectDuplicateFilesWidget.cpython-39.pyc', 'sample/qt/src/widget/__pycache__'),
    ('E:/kuangbao/Tools2/sample/qt/src/widget/__pycache__/FilesMD5Snapshot.cpython-39.pyc', 'sample/qt/src/widget/__pycache__'),
    ('E:/kuangbao/Tools2/sample/qt/src/widget/__pycache__/FoaBuildWidget.cpython-39.pyc', 'sample/qt/src/widget/__pycache__'),
    ('E:/kuangbao/Tools2/sample/qt/src/widget/__pycache__/FoaDetectWidget.cpython-39.pyc', 'sample/qt/src/widget/__pycache__'),
    ('E:/kuangbao/Tools2/sample/qt/src/widget/__pycache__/QuicParasAddTips.cpython-39.pyc', 'sample/qt/src/widget/__pycache__'),
    ('E:/kuangbao/Tools2/sample/qt/src/widget/__pycache__/ResConvertWidget.cpython-39.pyc', 'sample/qt/src/widget/__pycache__'),
    ('E:/kuangbao/Tools2/sample/qt/src/widget/__pycache__/ui_BranchCoverWidget.cpython-39.pyc', 'sample/qt/src/widget/__pycache__'),
    ('E:/kuangbao/Tools2/sample/qt/src/widget/__pycache__/ui_DebugAnalysisWidget.cpython-39.pyc', 'sample/qt/src/widget/__pycache__'),
    ('E:/kuangbao/Tools2/sample/qt/src/widget/__pycache__/ui_DetectDuplicateFilesWidget.cpython-39.pyc', 'sample/qt/src/widget/__pycache__'),
    ('E:/kuangbao/Tools2/sample/qt/src/widget/__pycache__/ui_FilesMD5Snapshot.cpython-39.pyc', 'sample/qt/src/widget/__pycache__'),
    ('E:/kuangbao/Tools2/sample/qt/src/widget/__pycache__/ui_FoaBuildWidget.cpython-39.pyc', 'sample/qt/src/widget/__pycache__'),
    ('E:/kuangbao/Tools2/sample/qt/src/widget/__pycache__/ui_FoaDetectWidget.cpython-39.pyc', 'sample/qt/src/widget/__pycache__'),
    ('E:/kuangbao/Tools2/sample/qt/src/widget/__pycache__/ui_QuicParasAddTips.cpython-39.pyc', 'sample/qt/src/widget/__pycache__'),
    ('E:/kuangbao/Tools2/sample/qt/src/widget/__pycache__/ui_ResConvertWidget.cpython-39.pyc', 'sample/qt/src/widget/__pycache__'),
    ('E:/kuangbao/Tools2/sample/qt/src/__pycache__/ui_mainwindow.cpython-39.pyc', 'sample/qt/src/__pycache__'),
    ('E:/kuangbao/Tools2/sample/src_references', 'sample/src_references')
],
    pathex=['../..'],  # 项目根目录作为 pathex
    hiddenimports=['Levenshtein', 'PyInstaller', 'PySide6', '_distutils_hack', '_pyinstaller_hooks_contrib', 'altgraph', 'dateutil', 'et_xmlfile', 'fuzz', 'fuzzywuzzy', 'importlib_metadata', 'numpy', 'openpyxl', 'ordlookup', 'packaging', 'pandas', 'pefile', 'peutils', 'pip', 'pkg_resources', 'pyperclip', 'pytz', 'rapidfuzz', 'setuptools', 'shiboken6', 'six', 'tzdata', 'win32ctypes', 'zipp'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='KBTools',  # 指定输出路径
    icon='../sample/qt/res/KBTools.ico',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True
)
