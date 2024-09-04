# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['E:\\kuangbao\\Tools2\\Main.py'],
             binaries=[],
             datas=[('E:\\kuangbao\\Tools2\\sample\\qt\\src', 'sample/qt/src')],
             pathex=['E:\\kuangbao\\Tools2\\sample'],
             hiddenimports=['sample.src_references.Main'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='KBTools',  # 指定输出路径
          icon='E:\\kuangbao\\Tools2\\sample\\qt\\res\\KBTools.ico',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,)