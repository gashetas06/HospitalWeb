import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital.settings')
django.setup()

from pacientes.models import Paciente
from usuarios.models import Usuario

pacientes = Paciente.objects.all()
creados = 0
existentes = 0

for paciente in pacientes:
    if not Usuario.objects.filter(cedula=paciente.cedula).exists():
        u = Usuario(
            cedula=paciente.cedula,
            nombre=f"{paciente.nombre} {paciente.apellido}",
            rol='paciente',
            paciente_id=paciente.idpaciente,
            is_staff=False,
            is_superuser=False,
        )
        u.set_password(paciente.cedula)
        u.save()
        creados += 1
        print(f"✓ Creado: {paciente.nombre} {paciente.apellido} | usuario: {paciente.cedula}")
    else:
        existentes += 1
        print(f"→ Ya existe: {paciente.cedula}")

try:
    pac100 = Paciente.objects.get(cedula='PAC100')
    if not Usuario.objects.filter(cedula='PAC100').exists():
        u = Usuario(
            cedula=pac100.cedula,
            nombre=f"{pac100.nombre} {pac100.apellido}",
            rol='paciente',
            paciente_id=pac100.idpaciente,
            is_staff=False,
            is_superuser=False,
        )
        u.set_password('PAC100')
        u.save()
        creados += 1
        print(f"✓ Creado: {pac100.nombre} {pac100.apellido} | usuario: PAC100")
    else:
        existentes += 1
        print(f"→ Ya existe: PAC100")
except Paciente.DoesNotExist:
    print("✗ Error: No se encontró ningún paciente con cédula PAC100")

print(f"\nResumen: {creados} creados, {existentes} ya existían")