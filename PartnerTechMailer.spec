# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('Correos.xlsx', '.'), ('Base_Mailing_V6_Nombres_Comerciales.xlsx', '.'), ('Logo_blanco_ver1.png', '.'), ('correo_brochure.html', '.'), ('correo_contacto_directo.html', '.'), ('correo_premium.html', '.'), ('correo_reunion_corta.html', '.'), ('correo_solo_brochure.html', '.'), ('correo_vacio.html', '.'), ('prueba_editor.html', '.')],
    hiddenimports=[],
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
    name='PartnerTechMailer',
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
    name='PartnerTechMailer',
)
