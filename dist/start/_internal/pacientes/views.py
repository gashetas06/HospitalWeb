from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from pacientes.models import Paciente
from citas.models import Cita
from historiaclinica.models import Historiaclinica
from evolucion.models import Evolucionclinica
from internacion.models import Internacion
from medicos.models import Medico


def paciente_required(view_func):
    """Decorador: verifica que el usuario tenga rol 'paciente' y perfil vinculado."""
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.rol != 'paciente' or not request.user.paciente_id:
            messages.error(request, 'Acceso restringido a pacientes.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def _get_paciente(request):
    """Helper: obtiene el objeto Paciente del usuario autenticado."""
    try:
        return Paciente.objects.get(idpaciente=request.user.paciente_id)
    except Paciente.DoesNotExist:
        return None

@paciente_required
def dashboard_paciente(request):
    paciente = _get_paciente(request)
    if not paciente:
        messages.error(request, 'No se encontró tu perfil de paciente.')
        return redirect('login')

    hoy = timezone.now().date()

    citas_qs = Cita.objects.filter(
        idpaciente=paciente
    ).select_related('idmedico', 'idmedico__idespecialidad').order_by('fecha', 'hora')

    proxima_cita = citas_qs.filter(
        fecha__gte=hoy,
        estado='Programada'
    ).first()

    citas_recientes = citas_qs.order_by('-fecha', '-hora')[:5]

    total_citas       = citas_qs.count()
    citas_completadas = citas_qs.filter(estado='Atendido').count()

    try:
        historia = Historiaclinica.objects.get(idpaciente=paciente)
    except Historiaclinica.DoesNotExist:
        historia = None

    # Última evolución (diagnóstico + tratamiento más reciente)
    ultima_evolucion = None
    if historia:
        ultima_evolucion = Evolucionclinica.objects.filter(
            idhistoria=historia
        ).select_related('idmedico').order_by('-fecha').first()

    ids_medicos = citas_qs.values_list('idmedico', flat=True).distinct()
    medicos_tratantes = Medico.objects.filter(
        idmedico__in=ids_medicos
    ).select_related('idespecialidad')[:6]

    internacion_activa = None
    try:
        internacion_activa = Internacion.objects.select_related(
            'idcama', 'idcama__iddepartamento', 'idmedicotratante_id'
        ).get(
            idpaciente_id=paciente.idpaciente,
            fechaegreso__isnull=True
        )
    except Internacion.DoesNotExist:
        pass

    context = {
        'paciente':           paciente,
        'proxima_cita':       proxima_cita,
        'citas_recientes':    citas_recientes,
        'total_citas':        total_citas,
        'citas_completadas':  citas_completadas,
        'historia':           historia,
        'ultima_evolucion':   ultima_evolucion,
        'medicos_tratantes':  medicos_tratantes,
        'internacion_activa': internacion_activa,
    }
    return render(request, 'paciente/dashboard_paciente.html', context)

@paciente_required
def mis_citas_paciente(request):
    paciente = _get_paciente(request)
    if not paciente:
        return redirect('login')

    filtro = request.GET.get('estado', 'todos')
    hoy    = timezone.now().date()

    citas = Cita.objects.filter(
        idpaciente=paciente
    ).select_related('idmedico', 'idmedico__idespecialidad').order_by('-fecha', '-hora')

    if filtro == 'pendiente':
        citas = citas.filter(estado='Programada')
    elif filtro == 'atendido':
        citas = citas.filter(estado='Atendido')
    elif filtro == 'cancelado':
        citas = citas.filter(estado='Cancelado')
    elif filtro == 'hoy':
        citas = citas.filter(fecha=hoy)

    context = {
        'paciente': paciente,
        'citas':    citas,
        'filtro':   filtro,
        'total':    citas.count(),
    }
    return render(request, 'paciente/mis_citas.html', context)

@paciente_required
def mi_historia(request):
    paciente = _get_paciente(request)
    if not paciente:
        return redirect('login')

    try:
        historia = Historiaclinica.objects.get(idpaciente=paciente)
    except Historiaclinica.DoesNotExist:
        historia = None

    evoluciones = []
    if historia:
        evoluciones = Evolucionclinica.objects.filter(
            idhistoria=historia
        ).select_related('idmedico').order_by('-fecha')

    context = {
        'paciente':   paciente,
        'historia':   historia,
        'evoluciones': evoluciones,
    }
    return render(request, 'paciente/mi_historia.html', context)

@paciente_required
def cambiar_password_paciente(request):
    if request.method == 'POST':
        actual   = request.POST.get('password_actual')
        nuevo    = request.POST.get('password_nuevo')
        confirm  = request.POST.get('password_confirm')

        if not request.user.check_password(actual):
            messages.error(request, 'La contraseña actual es incorrecta.')
        elif nuevo != confirm:
            messages.error(request, 'Las contraseñas nuevas no coinciden.')
        elif len(nuevo) < 6:
            messages.error(request, 'La contraseña debe tener al menos 6 caracteres.')
        else:
            request.user.set_password(nuevo)
            request.user.save()
            messages.success(request, 'Contraseña actualizada. Inicia sesión de nuevo.')
            return redirect('login')

    return render(request, 'paciente/cambiar_password.html', {
        'paciente': _get_paciente(request)
    })