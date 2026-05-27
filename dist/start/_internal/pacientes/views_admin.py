# pacientes/views_admin.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Paciente
from usuarios.models import Usuario


def admin_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.rol != 'admin':
            messages.error(request, 'Acceso restringido a administradores.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def _paciente_a_values(p):
    """Convierte un objeto Paciente a dict para el template."""
    return {
        'cedula':                     p.cedula,
        'nombre':                     p.nombre,
        'apellido':                   p.apellido,
        'fechanacimiento':            str(p.fechanacimiento),
        'sexo':                       p.sexo,
        'tiposangre':                 p.tiposangre or '',
        'telefono':                   p.telefono or '',
        'email':                      p.email or '',
        'direccion':                  p.direccion or '',
        'contactoemergencianombre':   p.contactoemergencianombre or '',
        'contactoemergenciatelefono': p.contactoemergenciatelefono or '',
        'activo':                     '1' if p.activo else '0',
    }


# ── LISTA ──────────────────────────────────────────────────────────────────────
@admin_required
def admin_lista_pacientes(request):
    pacientes = Paciente.objects.all().order_by('apellido', 'nombre')
    return render(request, 'pacientes/admin_lista.html', {
        'pacientes':     pacientes,
        'total_activos': pacientes.filter(activo=True).count(),
    })


# ── NUEVO ──────────────────────────────────────────────────────────────────────
@admin_required
def admin_nuevo_paciente(request):
    if request.method == 'POST':
        cedula    = request.POST.get('cedula', '').strip()
        nombre    = request.POST.get('nombre', '').strip()
        apellido  = request.POST.get('apellido', '').strip()
        fechanac  = request.POST.get('fechanacimiento', '').strip()
        sexo      = request.POST.get('sexo', '').strip()
        sangre    = request.POST.get('tiposangre', '').strip() or None
        telefono  = request.POST.get('telefono', '').strip() or None
        email     = request.POST.get('email', '').strip() or None
        direccion = request.POST.get('direccion', '').strip() or None
        cnt_nom   = request.POST.get('contactoemergencianombre', '').strip() or None
        cnt_tel   = request.POST.get('contactoemergenciatelefono', '').strip() or None
        activo    = request.POST.get('activo') == '1'

        if not cedula or not nombre or not apellido or not fechanac or not sexo:
            messages.error(request, 'Cédula, nombre, apellido, fecha de nacimiento y sexo son obligatorios.')
            return render(request, 'pacientes/admin_form.html', {
                'paciente': None,
                'values': request.POST,
            })

        if Paciente.objects.filter(cedula=cedula).exists():
            messages.error(request, f'Ya existe un paciente con la cédula {cedula}.')
            return render(request, 'pacientes/admin_form.html', {
                'paciente': None,
                'values': request.POST,
            })

        paciente = Paciente(
            cedula=cedula, nombre=nombre, apellido=apellido,
            fechanacimiento=fechanac, sexo=sexo, tiposangre=sangre,
            telefono=telefono, email=email, direccion=direccion,
            contactoemergencianombre=cnt_nom,
            contactoemergenciatelefono=cnt_tel,
            activo=activo,
        )
        paciente.save()

        if not Usuario.objects.filter(cedula=cedula).exists():
            u = Usuario(
                cedula=cedula,
                nombre=f"{nombre} {apellido}",
                rol='paciente',
                paciente_id=paciente.idpaciente,
                is_staff=False,
                is_superuser=False,
            )
            u.set_password(cedula)
            u.save()
            messages.success(request, f'Paciente creado. Usuario: {cedula} | Contraseña inicial: {cedula}')
        else:
            messages.success(request, f'Paciente {nombre} {apellido} registrado correctamente.')

        return redirect('admin_lista_pacientes')

    # GET — formulario vacío
    return render(request, 'pacientes/admin_form.html', {
        'paciente': None,
        'values': {
            'cedula': '', 'nombre': '', 'apellido': '',
            'fechanacimiento': '', 'sexo': '', 'tiposangre': '',
            'telefono': '', 'email': '', 'direccion': '',
            'contactoemergencianombre': '', 'contactoemergenciatelefono': '',
            'activo': '1',
        }
    })


# ── EDITAR ─────────────────────────────────────────────────────────────────────
@admin_required
def admin_editar_paciente(request, id):
    paciente = get_object_or_404(Paciente, pk=id)

    if request.method == 'POST':
        nombre    = request.POST.get('nombre', '').strip()
        apellido  = request.POST.get('apellido', '').strip()
        fechanac  = request.POST.get('fechanacimiento', '').strip()
        sexo      = request.POST.get('sexo', '').strip()
        sangre    = request.POST.get('tiposangre', '').strip() or None
        telefono  = request.POST.get('telefono', '').strip() or None
        email     = request.POST.get('email', '').strip() or None
        direccion = request.POST.get('direccion', '').strip() or None
        cnt_nom   = request.POST.get('contactoemergencianombre', '').strip() or None
        cnt_tel   = request.POST.get('contactoemergenciatelefono', '').strip() or None
        activo    = request.POST.get('activo') == '1'

        if not nombre or not apellido or not fechanac or not sexo:
            messages.error(request, 'Nombre, apellido, fecha de nacimiento y sexo son obligatorios.')
            return render(request, 'pacientes/admin_form.html', {
                'paciente': paciente,
                'values': request.POST,
            })

        paciente.nombre    = nombre
        paciente.apellido  = apellido
        paciente.fechanacimiento = fechanac
        paciente.sexo      = sexo
        paciente.tiposangre = sangre
        paciente.telefono  = telefono
        paciente.email     = email
        paciente.direccion = direccion
        paciente.contactoemergencianombre   = cnt_nom
        paciente.contactoemergenciatelefono = cnt_tel
        paciente.activo    = activo
        paciente.save()

        Usuario.objects.filter(cedula=paciente.cedula).update(nombre=f"{nombre} {apellido}")
        messages.success(request, f'Paciente {nombre} {apellido} actualizado correctamente.')
        return redirect('admin_lista_pacientes')

    # GET — rellena values con datos del paciente
    return render(request, 'pacientes/admin_form.html', {
        'paciente': paciente,
        'values':   _paciente_a_values(paciente),
    })


# ── ELIMINAR ───────────────────────────────────────────────────────────────────
@admin_required
def admin_eliminar_paciente(request, id):
    paciente = get_object_or_404(Paciente, pk=id)
    nombre = str(paciente)
    Usuario.objects.filter(cedula=paciente.cedula).delete()
    paciente.delete()
    messages.success(request, f'Paciente {nombre} eliminado correctamente.')
    return redirect('admin_lista_pacientes')