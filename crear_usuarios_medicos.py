import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital.settings')
django.setup()

from medicos.models import Medico
from usuarios.models import Usuario

medicos = Medico.objects.all()
creados = 0
existentes = 0

for medico in medicos:
    if not Usuario.objects.filter(cedula=medico.cedula).exists():
        u = Usuario(
            cedula=medico.cedula,
            nombre=f"{medico.nombre} {medico.apellido}",
            rol='medico',
            medico_id=medico.idmedico,
            is_staff=False,
            is_superuser=False,
        )
        u.set_password(medico.cedula)
        u.save()
        creados += 1
        print(f"Creado: {medico.nombre} {medico.apellido} | usuario: {medico.cedula}")
    else:
        existentes += 1
        print(f"Ya existe: {medico.cedula}")

print(f"\nResumen: {creados} creados, {existentes} ya existian")