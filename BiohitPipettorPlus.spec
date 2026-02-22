# -*- mode: python ; coding: utf-8 -*-

import os
import biohit_pipettor

pkg_dir = os.path.dirname(biohit_pipettor.__file__)
dll_path = os.path.join(pkg_dir, "include", "InstrumentLib.dll")

a = Analysis(
    ['src\\biohit_pipettor_plus\\bootstrap.py'],
    pathex=['src'],
    binaries=[(dll_path, '.')],
    datas=[('dotnet-runtime-installer.exe', '.'),  # <-- bundle the .NET installer
    ],
    hiddenimports=['biohit_pipettor_plus.gui.gui2'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='BiohitPipettorPlus',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='BiohitPipettorPlus',
)
