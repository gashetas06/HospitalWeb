from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Medico
from .forms import MedicoForm
from internacion.models import Internacion, Cama
from usuarios.models import Usuario
from citas.models import Cita
from pacientes.models import Paciente
from historiaclinica.models import Historiaclinica
from evolucion.models import Evolucionclinica

@login_required
def dashboard_medico(request):
    try:
        medico = Medico.objects.get(idmedico=request.user.medico_id)
    except Medico.DoesNotExist:
        messages.error(request, 'No se encontró tu perfil de médico.')
        return redirect('login')

    hoy = timezone.now().date()

    citas_pendientes = Cita.objects.filter(
        idmedico=medico,
        estado='Programada'
    ).select_related('idpaciente').order_by('fecha', 'hora')

    citas_hoy = citas_pendientes.filter(fecha=hoy)
    proxima_cita = citas_pendientes.filter(fecha__gte=hoy).first()

    ids_pacientes = Cita.objects.filter(
        idmedico=medico
    ).values_list('idpaciente', flat=True).distinct()

    total_pacientes = ids_pacientes.count()

    atendidos_hoy = Cita.objects.filter(
        idmedico=medico,
        fecha=hoy,
        estado='Atendido'
    ).count()

    context = {
        'medico': medico,
        'citas_pendientes': citas_pendientes,
        'total_citas_hoy': citas_hoy.count(),
        'total_pacientes': total_pacientes,
        'atendidos_hoy': atendidos_hoy,
        'proxima_cita': proxima_cita,
        'citas_pendientes_count': citas_pendientes.count(),
    }
    return render(request, 'medicos/dashboard_medico.html', context)


@login_required
def cambiar_password(request):
    if request.method == 'POST':
        password_actual  = request.POST.get('password_actual')
        password_nuevo   = request.POST.get('password_nuevo')
        password_confirm = request.POST.get('password_confirm')

        if not request.user.check_password(password_actual):
            messages.error(request, 'La contraseña actual es incorrecta.')
        elif password_nuevo != password_confirm:
            messages.error(request, 'Las contraseñas nuevas no coinciden.')
        elif len(password_nuevo) < 6:
            messages.error(request, 'La contraseña debe tener al menos 6 caracteres.')
        else:
            request.user.set_password(password_nuevo)
            request.user.save()
            messages.success(request, 'Contraseña actualizada. Inicia sesión de nuevo.')
            return redirect('login')

    return render(request, 'medicos/cambiar_password.html')


@login_required
def lista_medicos(request):
    medicos = Medico.objects.all()
    total_activos = medicos.filter(activo=True).count()
    return render(request, 'medicos/lista.html', {
        'medicos': medicos,
        'total_activos': total_activos,
    })


@login_required
def mis_citas(request):
    try:
        medico = Medico.objects.get(idmedico=request.user.medico_id)
    except Medico.DoesNotExist:
        return redirect('login')

    filtro = request.GET.get('estado', 'todos')
    hoy = timezone.now().date()

    citas = Cita.objects.filter(
        idmedico=medico
    ).select_related('idpaciente').order_by('-fecha', '-hora')

    if filtro == 'pendiente':
        citas = citas.filter(estado='Programada')
    elif filtro == 'atendido':
        citas = citas.filter(estado='Atendido')
    elif filtro == 'cancelado':
        citas = citas.filter(estado='Cancelado')
    elif filtro == 'hoy':
        citas = citas.filter(fecha=hoy)

    context = {
        'medico': medico,
        'citas': citas,
        'filtro': filtro,
        'total': citas.count(),
    }
    return render(request, 'medicos/mis_citas.html', context)


@login_required
def ver_cita(request, id):
    try:
        medico = Medico.objects.get(idmedico=request.user.medico_id)
    except Medico.DoesNotExist:
        return redirect('login')

    cita = get_object_or_404(Cita, pk=id, idmedico=medico)
    paciente = cita.idpaciente

    try:
        historia = Historiaclinica.objects.get(idpaciente=paciente)
    except Historiaclinica.DoesNotExist:
        historia = None

    evoluciones = []
    if historia:
        evoluciones = Evolucionclinica.objects.filter(
            idhistoria=historia
        ).order_by('-fecha')

    if request.method == 'POST':
        if historia is None:
            messages.error(request, 'El paciente no tiene historia clínica. Contacte al administrador.')
            return redirect('ver_cita', id=id)

        ev = Evolucionclinica(
            idhistoria=historia,
            idmedico=medico,
            fecha=timezone.now(),
            motivoconsulta=request.POST.get('motivoconsulta', ''),
            exploracionfisica=request.POST.get('exploracionfisica', '') or None,
            diagnostico=request.POST.get('diagnostico', '') or None,
            tratamiento=request.POST.get('tratamiento', '') or None,
            receta=request.POST.get('receta', '') or None,
            proximarevision=request.POST.get('proximarevision') or None,
        )
        ev.save()

        if request.POST.get('marcar_atendido'):
            cita.estado = 'Atendido'
            cita.save()
            messages.success(request, 'Evolución guardada y cita marcada como Atendida.')
        else:
            messages.success(request, 'Evolución guardada correctamente.')

        return redirect('ver_cita', id=id)

    context = {
        'medico': medico,
        'cita': cita,
        'paciente': paciente,
        'historia': historia,
        'evoluciones': evoluciones,
    }
    return render(request, 'medicos/ver_cita.html', context)


@login_required
def atender_cita(request, id):
    try:
        medico = Medico.objects.get(idmedico=request.user.medico_id)
    except Medico.DoesNotExist:
        return redirect('login')

    cita = get_object_or_404(Cita, pk=id, idmedico=medico)
    cita.estado = 'Atendido'
    cita.save()
    messages.success(request, 'Cita marcada como Atendida.')
    return redirect('mis_citas')


@login_required
def cancelar_cita(request, id):
    try:
        medico = Medico.objects.get(idmedico=request.user.medico_id)
    except Medico.DoesNotExist:
        return redirect('login')

    cita = get_object_or_404(Cita, pk=id, idmedico=medico)
    cita.estado = 'Cancelado'
    cita.save()
    messages.success(request, 'Cita cancelada.')
    return redirect('mis_citas')


@login_required
def mis_pacientes(request):
    try:
        medico = Medico.objects.get(idmedico=request.user.medico_id)
    except Medico.DoesNotExist:
        return redirect('login')

    ids_pacientes = Cita.objects.filter(
        idmedico=medico
    ).values_list('idpaciente', flat=True).distinct()

    pacientes = Paciente.objects.filter(idpaciente__in=ids_pacientes)

    context = {
        'medico': medico,
        'pacientes': pacientes,
        'total': pacientes.count(),
    }
    return render(request, 'medicos/mis_pacientes.html', context)


@login_required
def ver_paciente(request, id):
    try:
        medico = Medico.objects.get(idmedico=request.user.medico_id)
    except Medico.DoesNotExist:
        return redirect('login')

    paciente = get_object_or_404(Paciente, pk=id)

    tiene_citas = Cita.objects.filter(idmedico=medico, idpaciente=paciente).exists()
    if not tiene_citas:
        messages.error(request, 'No tienes acceso a este paciente.')
        return redirect('mis_pacientes')

    try:
        historia = Historiaclinica.objects.get(idpaciente=paciente)
    except Historiaclinica.DoesNotExist:
        historia = None

    evoluciones = []
    if historia:
        evoluciones = Evolucionclinica.objects.filter(
            idhistoria=historia
        ).order_by('-fecha')

    citas_paciente = Cita.objects.filter(
        idmedico=medico,
        idpaciente=paciente
    ).order_by('-fecha', '-hora')

    context = {
        'medico': medico,
        'paciente': paciente,
        'historia': historia,
        'evoluciones': evoluciones,
        'citas': citas_paciente,
    }
    return render(request, 'medicos/ver_paciente.html', context)

@login_required
def mis_internaciones(request):
    """Lista de internaciones activas e historial del médico."""
    try:
        medico = Medico.objects.get(idmedico=request.user.medico_id)
    except Medico.DoesNotExist:
        return redirect('login')
 
    # Internaciones activas (sin fecha de egreso)
    activas = Internacion.objects.filter(
        idmedicotratante_id=medico.idmedico,
        fechaegreso__isnull=True
    ).select_related('idcama', 'idcama__iddepartamento', 'idcama__idtipo').order_by('-fechaingreso')
 
    # Historial (con egreso)
    historial = Internacion.objects.filter(
        idmedicotratante_id=medico.idmedico,
        fechaegreso__isnull=False
    ).select_related('idcama', 'idcama__iddepartamento', 'idcama__idtipo').order_by('-fechaegreso')[:20]
 
    # Enriquecer con datos de paciente
    def enriquecer(qs):
        result = []
        for intern in qs:
            try:
                paciente = Paciente.objects.get(idpaciente=intern.idpaciente_id)
            except Paciente.DoesNotExist:
                paciente = None
            result.append({'internacion': intern, 'paciente': paciente})
        return result
 
    context = {
        'medico': medico,
        'activas': enriquecer(activas),
        'historial': enriquecer(historial),
        'total_activas': activas.count(),
    }
    return render(request, 'medicos/mis_internaciones.html', context)
 
 
@login_required
def internar_paciente(request, paciente_id=None):
    """Formulario para internar un paciente — solo médicos."""
    try:
        medico = Medico.objects.get(idmedico=request.user.medico_id)
    except Medico.DoesNotExist:
        return redirect('login')
 
    # Camas disponibles (estado = 'Libre')
    camas_libres = Cama.objects.filter(
        estado='Libre'
    ).select_related('iddepartamento', 'idtipo').order_by('iddepartamento__nombre', 'numero')
 
    # Si viene con paciente_id preseleccionado (desde ver_paciente)
    paciente_preseleccionado = None
    if paciente_id:
        paciente_preseleccionado = get_object_or_404(Paciente, pk=paciente_id)
 
    if request.method == 'POST':
        p_id        = request.POST.get('idpaciente')
        cama_id     = request.POST.get('idcama')
        motivo      = request.POST.get('motivoingreso', '').strip()
 
        # Validaciones básicas
        if not p_id or not cama_id or not motivo:
            messages.error(request, 'Todos los campos son obligatorios.')
            return redirect(request.path)
 
        # Verificar que la cama sigue libre
        try:
            cama = Cama.objects.get(idcama=cama_id, estado='Libre')
        except Cama.DoesNotExist:
            messages.error(request, 'La cama seleccionada ya no está disponible.')
            return redirect(request.path)
 
        # Verificar que el paciente existe
        try:
            paciente = Paciente.objects.get(idpaciente=p_id)
        except Paciente.DoesNotExist:
            messages.error(request, 'Paciente no encontrado.')
            return redirect(request.path)
 
        # Verificar que el paciente no esté ya internado
        ya_internado = Internacion.objects.filter(
            idpaciente_id=paciente.idpaciente,
            fechaegreso__isnull=True
        ).exists()
        if ya_internado:
            messages.error(request, f'{paciente} ya tiene una internación activa.')
            return redirect(request.path)
 
        # Crear internación — el trigger SQL ocupa la cama automáticamente
        Internacion.objects.create(
            idpaciente_id=paciente.idpaciente,
            idcama=cama,
            idmedicotratante_id=medico.idmedico,
            fechaingreso=timezone.now(),
            motivoingreso=motivo,
        )
 
        messages.success(
            request,
            f'Paciente {paciente} internado en cama {cama.numero} correctamente.'
        )
        return redirect('mis_internaciones')
 
    # Listado de pacientes del médico para el select
    ids_pacientes = Cita.objects.filter(
        idmedico=medico
    ).values_list('idpaciente', flat=True).distinct()
    pacientes = Paciente.objects.filter(idpaciente__in=ids_pacientes, activo=True).order_by('apellido')
 
    context = {
        'medico': medico,
        'camas_libres': camas_libres,
        'pacientes': pacientes,
        'paciente_preseleccionado': paciente_preseleccionado,
    }
    return render(request, 'medicos/internar_paciente.html', context)
 
 
@login_required
def dar_alta(request, internacion_id):
    """El médico da el alta a un paciente internado."""
    try:
        medico = Medico.objects.get(idmedico=request.user.medico_id)
    except Medico.DoesNotExist:
        return redirect('login')
 
    internacion = get_object_or_404(
        Internacion,
        idinternacion=internacion_id,
        idmedicotratante_id=medico.idmedico,
        fechaegreso__isnull=True   # solo activas
    )
 
    if request.method == 'POST':
        diagnostico = request.POST.get('diagnosticoegreso', '').strip() or None
        condicion   = request.POST.get('condicionegreso', 'Alta médica')
 
        CONDICIONES_VALIDAS = ['Alta voluntaria', 'Alta médica', 'Traslado', 'Fallecido']
        if condicion not in CONDICIONES_VALIDAS:
            condicion = 'Alta médica'
 
        # Registrar egreso
        internacion.fechaegreso      = timezone.now()
        internacion.diagnosticoegreso = diagnostico
        internacion.condicionegreso   = condicion
        internacion.save()
 
        # Liberar la cama manualmente (el SP de SQL lo hace,
        # pero desde Django también lo actualizamos)
        cama = internacion.idcama
        cama.estado = 'Libre'
        cama.save()
 
        try:
            paciente = Paciente.objects.get(idpaciente=internacion.idpaciente_id)
            nombre_p = str(paciente)
        except Paciente.DoesNotExist:
            nombre_p = f'ID {internacion.idpaciente_id}'
 
        messages.success(request, f'Alta registrada para {nombre_p}. Cama {cama.numero} liberada.')
        return redirect('mis_internaciones')
 
    # GET — mostrar formulario de alta
    try:
        paciente = Paciente.objects.get(idpaciente=internacion.idpaciente_id)
    except Paciente.DoesNotExist:
        paciente = None
 
    context = {
        'medico': medico,
        'internacion': internacion,
        'paciente': paciente,
        'condiciones': ['Alta médica', 'Alta voluntaria', 'Traslado', 'Fallecido'],
    }
    return render(request, 'medicos/dar_alta.html', context)

@login_required
def nuevo_medico(request):
    if request.method == 'POST':
        form = MedicoForm(request.POST)
        if form.is_valid():
            medico = form.save()
            cedula = medico.cedula
            if not Usuario.objects.filter(cedula=cedula).exists():
                u = Usuario(
                    cedula=cedula,
                    nombre=f"{medico.nombre} {medico.apellido}",
                    rol='medico',
                    medico_id=medico.idmedico,
                    is_staff=False,
                    is_superuser=False,
                )
                u.set_password(cedula)
                u.save()
                messages.success(request, f'Médico creado. Usuario: {cedula} | Contraseña inicial: {cedula}')
            else:
                messages.warning(request, f'Médico creado pero ya existía un usuario con cédula {cedula}.')
            return redirect('lista_medicos')
    else:
        form = MedicoForm()
    return render(request, 'medicos/nuevo.html', {'form': form})


@login_required
def editar_medico(request, id):
    medico = get_object_or_404(Medico, pk=id)
    if request.method == 'POST':
        form = MedicoForm(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            messages.success(request, 'Médico actualizado correctamente.')
            return redirect('lista_medicos')
    else:
        form = MedicoForm(instance=medico)
    return render(request, 'medicos/editar.html', {'form': form})


@login_required
def eliminar_medico(request, id):
    medico = get_object_or_404(Medico, pk=id)
    Usuario.objects.filter(cedula=medico.cedula).delete()
    medico.delete()
    messages.success(request, 'Médico eliminado correctamente.')
    return redirect('lista_medicos')