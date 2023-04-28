# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['serwis.py'],
    pathex=[],
    binaries=[],
    datas=[('Bot\\test.py', 'Bot'), ('Bot\\bilkom.py', 'Bot'), ('Bot\\Debbug.py', 'Bot'), ('templates\\index.html', 'templates'), ('Billkomdane.csv', '.'), ('dane.csv', '.'), ('config.ini', '.'), ('Log', 'Log'), ('Logi_Bot', 'Logi_Bot'), ('requirements.txt', '.'), ('1.wav', '.')],
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
    name='serwis',
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
)
