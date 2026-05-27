# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = ['webview', 'django', 'pyodbc', 'mssql', 'mssql.base']
hiddenimports += collect_submodules('django')
hiddenimports += collect_submodules('mssql')
hiddenimports += collect_submodules('usuarios')
hiddenimports += collect_submodules('pacientes')
hiddenimports += collect_submodules('medicos')
hiddenimports += collect_submodules('empleados')
hiddenimports += collect_submodules('citas')
hiddenimports += collect_submodules('dashboard')
hiddenimports += collect_submodules('historiaclinica')
hiddenimports += collect_submodules('internacion')
hiddenimports += collect_submodules('inventario')
hiddenimports += collect_submodules('facturas')
hiddenimports += collect_submodules('evolucion')


a = Analysis(
    ['start.py'],
    pathex=[],
    binaries=[],
    datas=[('hospital', 'hospital'), ('usuarios', 'usuarios'), ('pacientes', 'pacientes'), ('medicos', 'medicos'), ('empleados', 'empleados'), ('citas', 'citas'), ('dashboard', 'dashboard'), ('historiaclinica', 'historiaclinica'), ('internacion', 'internacion'), ('inventario', 'inventario'), ('facturas', 'facturas'), ('evolucion', 'evolucion')],
    hiddenimports=hiddenimports,
    hookspath=['hooks'],
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
    name='start',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
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
    name='start',
)
