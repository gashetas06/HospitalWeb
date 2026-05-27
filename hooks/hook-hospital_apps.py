# hooks/hook-hospital_apps.py
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

apps = [
    'usuarios',
    'pacientes',
    'medicos',
    'empleados',
    'citas',
    'dashboard',
    'historiaclinica',
    'internacion',
    'inventario',
    'facturas',
    'evolucion',
]

hiddenimports = []
datas = []

for app in apps:
    hiddenimports += collect_submodules(app)
    datas += collect_data_files(app)