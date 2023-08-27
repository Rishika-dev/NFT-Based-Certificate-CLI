# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['D:/Major-Project/cli/CLI.py'],
    pathex=[],
    binaries=[],
    datas=[('D:/Major-Project/cli/.env', '.'), ('D:/Major-Project/cli/Courgette-Regular.ttf', '.'), ('D:/Major-Project/cli/generateCertificate.py', '.'), ('D:/Major-Project/cli/ipfsUpload.py', '.'), ('D:/Major-Project/cli/reqHandler.py', '.'), ('D:/Major-Project/cli/requirements.txt', '.'), ('D:/Major-Project/cli/textImage.py', '.'), ('D:/Major-Project/cli/images', 'images/')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CLI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['D:\\Major-Project\\icon.ico'],
)
