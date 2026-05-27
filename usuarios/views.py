from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def login_view(request):
    if request.user.is_authenticated:
        return redirect_by_rol(request.user)

    if request.method == 'POST':
        cedula   = request.POST.get('cedula')
        password = request.POST.get('password')
        user     = authenticate(request, cedula=cedula, password=password)

        if user is not None and user.activo:
            login(request, user)
            return redirect_by_rol(user)
        else:
            messages.error(request, 'Cédula o contraseña incorrecta.')

    return render(request, 'usuarios/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def redirect_by_rol(user):
    from django.shortcuts import redirect
    roles = {
        'admin':    '/',
        'medico':   '/medicos/dashboard/',
        'empleado': '/empleado/dashboard/',
        'paciente': '/pacientes/dashboard/',
    }
    return redirect(roles.get(user.rol, '/'))