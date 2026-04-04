# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path


def _discover_logo_datas():
    root = Path('.')
    files = []
    for pattern in ('*.png', '*.jpg', '*.jpeg', '*.webp', '*.ico'):
        files.extend(sorted(root.glob(pattern)))
    preferred = [
        path for path in files
        if any(keyword in path.name.lower() for keyword in ('logo', 'icon', 'brand'))
    ]
    selected = preferred[0] if preferred else (files[0] if len(files) == 1 else None)
    return [(str(selected), '.')] if selected else []


a = Analysis(
    ['trae_unlock.py'],
    pathex=[],
    binaries=[],
    datas=_discover_logo_datas(),
    hiddenimports=['customtkinter', 'traereset_core', 'traereset_ui'],
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
    a.binaries,
    a.datas,
    [],
    name='TraeReset',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
