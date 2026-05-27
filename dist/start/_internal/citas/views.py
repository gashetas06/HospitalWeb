from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
from .models import Cita


@login_required
def lista_citas(request):
    filtro = request.GET.get('estado', 'todos')
    hoy = datetime.date.today()

    citas = Cita.objects.select_related('idpaciente', 'idmedico').order_by('-fecha', '-hora')

    if filtro == 'Programada':
        citas = citas.filter(estado='Programada')
    elif filtro == 'Confirmada':
        citas = citas.filter(estado='Confirmada')
    elif filtro == 'En curso':
        citas = citas.filter(estado='En curso')
    elif filtro == 'Completada':
        citas = citas.filter(estado='Completada')
    elif filtro == 'Cancelada':
        citas = citas.filter(estado='Cancelada')
    elif filtro == 'No asistió':
        citas = citas.filter(estado='No asistió')
    elif filtro == 'hoy':
        citas = citas.filter(fecha=hoy)

    total_hoy        = Cita.objects.filter(fecha=hoy).count()
    total_programadas = Cita.objects.filter(estado='Programada').count()
    total_completadas = Cita.objects.filter(estado='Completada').count()

    return render(request, 'citas/lista.html', {
        'citas': citas,
        'filtro': filtro,
        'total_hoy': total_hoy,
        'total_programadas': total_programadas,
        'total_completadas': total_completadas,
        'total': citas.count(),
    })


@login_required
def cancelar_cita(request, id):
    cita = get_object_or_404(Cita, pk=id)
    cita.estado = 'Cancelada'
    cita.save()
    messages.success(request, f'Cita #{id} cancelada.')
    return redirect('lista_citas')


@login_required
def completar_cita(request, id):
    cita = get_object_or_404(Cita, pk=id)
    cita.estado = 'Completada'
    cita.save()
    messages.success(request, f'Cita #{id} marcada como completada.')
    return redirect('lista_citas')