from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Internacion, Cama

try:
    from pacientes.models import Paciente
except ImportError:
    Paciente = None

try:
    from medicos.models import Medico
except ImportError:
    Medico = None


def _get_paciente(pid):
    if Paciente:
        try:
            return Paciente.objects.get(idpaciente=pid)
        except Paciente.DoesNotExist:
            pass
    return None


def _get_medico(mid):
    if Medico:
        try:
            return Medico.objects.get(idmedico=mid)
        except Medico.DoesNotExist:
            pass
    return None


def _enriquecer(qs):
    result = []
    for i in qs:
        result.append({
            'internacion': i,
            'paciente':    _get_paciente(i.idpaciente_id),
            'medico':      _get_medico(i.idmedicotratante_id),
        })
    return result


# ── LISTA (tab: activas / historial / estado camas) ───────────────────────────
@login_required
def lista_internaciones(request):
    todas = Internacion.objects.select_related(
        'idcama', 'idcama__iddepartamento', 'idcama__idtipo'
    ).order_by('-fechaingreso')

    activas   = todas.filter(fechaegreso__isnull=True)
    historial = todas.filter(fechaegreso__isnull=False)

    # Camas
    todas_las_camas = Cama.objects.select_related(
        'iddepartamento', 'idtipo'
    ).order_by('iddepartamento__nombre', 'numero')

    camas_libres   = todas_las_camas.filter(estado='Libre').count()
    camas_ocupadas = todas_las_camas.filter(estado='Ocupada').count()

    return render(request, 'internacion/lista.html', {
        'activas':         _enriquecer(activas),
        'historial':       _enriquecer(historial),
        'total_activas':   activas.count(),
        'total_historial': historial.count(),
        'todas_las_camas': todas_las_camas,
        'camas_libres':    camas_libres,
        'camas_ocupadas':  camas_ocupadas,
    })


# ── NUEVA INTERNACIÓN (admin: elige paciente + médico + cama) ─────────────────
@login_required
def nueva_internacion(request):
    camas_libres = Cama.objects.select_related(
        'iddepartamento', 'idtipo'
    ).filter(estado='Libre').order_by('iddepartamento__nombre', 'numero')

    pacientes = Paciente.objects.filter(activo=True).order_by('apellido') if Paciente else []
    medicos   = Medico.objects.filter(activo=True).order_by('apellido')   if Medico   else []

    if request.method == 'POST':
        paciente_id    = request.POST.get('idpaciente_id')
        medico_id      = request.POST.get('idmedicotratante_id')
        cama_id        = request.POST.get('idcama')
        motivo         = request.POST.get('motivoingreso', '').strip()

        # Validaciones
        if not all([paciente_id, medico_id, cama_id, motivo]):
            messages.error(request, 'Todos los campos son obligatorios.')
            return render(request, 'internacion/nuevo.html', {
                'camas_libres': camas_libres,
                'pacientes':    pacientes,
                'medicos':      medicos,
            })

        # Verificar que la cama sigue libre
        try:
            cama = Cama.objects.get(idcama=cama_id, estado='Libre')
        except Cama.DoesNotExist:
            messages.error(request, 'La cama seleccionada ya no está disponible. Elige otra.')
            return render(request, 'internacion/nuevo.html', {
                'camas_libres': camas_libres,
                'pacientes':    pacientes,
                'medicos':      medicos,
            })

        # Verificar que el paciente no esté ya internado
        ya_internado = Internacion.objects.filter(
            idpaciente_id=paciente_id,
            fechaegreso__isnull=True
        ).exists()
        if ya_internado:
            paciente_obj = _get_paciente(int(paciente_id))
            nombre = str(paciente_obj) if paciente_obj else f'ID {paciente_id}'
            messages.error(request, f'{nombre} ya tiene una internación activa.')
            return render(request, 'internacion/nuevo.html', {
                'camas_libres': camas_libres,
                'pacientes':    pacientes,
                'medicos':      medicos,
            })

        # Crear internación
        Internacion.objects.create(
            idpaciente_id=int(paciente_id),
            idcama=cama,
            idmedicotratante_id=int(medico_id),
            fechaingreso=timezone.now(),
            motivoingreso=motivo,
        )

        # El trigger SQL ocupa la cama, pero también lo hacemos desde Django
        cama.estado = 'Ocupada'
        cama.save()

        messages.success(request, f'Internación registrada. Cama {cama.numero} asignada.')
        return redirect('lista_internaciones')

    return render(request, 'internacion/nuevo.html', {
        'camas_libres': camas_libres,
        'pacientes':    pacientes,
        'medicos':      medicos,
    })


# ── DAR ALTA (admin: puede dar alta a CUALQUIER internación activa) ────────────
@login_required
def dar_alta_admin(request, id):
    internacion = get_object_or_404(Internacion, pk=id, fechaegreso__isnull=True)
    paciente    = _get_paciente(internacion.idpaciente_id)

    CONDICIONES = ['Alta médica', 'Alta voluntaria', 'Traslado', 'Fallecido']

    if request.method == 'POST':
        diagnostico = request.POST.get('diagnosticoegreso', '').strip() or None
        condicion   = request.POST.get('condicionegreso', 'Alta médica')

        if condicion not in CONDICIONES:
            condicion = 'Alta médica'

        internacion.fechaegreso       = timezone.now()
        internacion.diagnosticoegreso = diagnostico
        internacion.condicionegreso   = condicion
        internacion.save()

        cama = internacion.idcama
        cama.estado = 'Libre'
        cama.save()

        nombre = str(paciente) if paciente else f'ID {internacion.idpaciente_id}'
        messages.success(request, f'Alta registrada para {nombre}. Cama {cama.numero} liberada.')
        return redirect('lista_internaciones')

    return render(request, 'internacion/alta.html', {
        'internacion': internacion,
        'paciente':    paciente,
        'condiciones': CONDICIONES,
    })


# ── ELIMINAR (solo admin) ─────────────────────────────────────────────────────
@login_required
def eliminar_internacion(request, id):
    internacion = get_object_or_404(Internacion, pk=id)

    if internacion.fechaegreso is None:
        cama = internacion.idcama
        cama.estado = 'Libre'
        cama.save()

    internacion.delete()
    messages.success(request, 'Internación eliminada.')
    return redirect('lista_internaciones')