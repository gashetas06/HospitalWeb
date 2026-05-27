from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db import models
import datetime
from pacientes.models import Paciente
from medicos.models import Medico
from citas.models import Cita
from inventario.models import Inventario
from empleados.models import Empleado
from internacion.models import Internacion, Cama
from facturas.models import Factura

@login_required
def dashboard_admin(request):
    hoy = datetime.date.today()
    context = {
        'pacientes_activos':   Paciente.objects.filter(activo=True).count(),
        'medicos_activos':     Medico.objects.filter(activo=True).count(),
        'empleados_activos':   Empleado.objects.filter(activo=True).count(),
        'citas_hoy':           Cita.objects.filter(fecha=hoy).count(),
        'internados':          Internacion.objects.filter(fechaegreso__isnull=True).count(),
        'camas_libres':        Cama.objects.filter(estado='Libre').count(),
        'productos_criticos':  Inventario.objects.filter(cantidaddisponible__lte=models.F('nivelcritico')).count(),
        'facturas_pendientes': Factura.objects.filter(estado='Pendiente').count(),
    }
    return render(request, 'dashboard/dashboard.html', context)