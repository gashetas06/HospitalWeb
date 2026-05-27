import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital.settings')
django.setup()

from usuarios.models import Usuario
from medicos.models import Medico
from pacientes.models import Paciente

creados = 0

# Médicos
for medico in Medico.objects.all():
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
        print(f"✓ Médico: {medico.cedula}")

# Pacientes
for paciente in Paciente.objects.all():
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
        print(f"✓ Paciente: {paciente.cedula}")

print(f"\nTotal creados: {creados}")