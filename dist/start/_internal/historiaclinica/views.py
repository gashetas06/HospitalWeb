from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Historiaclinica
from .forms import HistoriaClinicaForm

try:
    from evolucion.models import Evolucionclinica
except ImportError:
    Evolucionclinica = None


@login_required
def lista_historias(request):
    historias = Historiaclinica.objects.select_related('idpaciente').order_by('-fechacreacion')
    return render(request, 'historiaclinica/lista.html', {
        'historias': historias,
        'total': historias.count(),
    })


@login_required
def nueva_historia(request):
    if request.method == 'POST':
        form = HistoriaClinicaForm(request.POST)
        if form.is_valid():
            historia = form.save(commit=False)
            historia.fechacreacion = timezone.now()
            historia.save()
            messages.success(request, 'Historia clínica creada.')
            return redirect('lista_historias')
    else:
        form = HistoriaClinicaForm()
    return render(request, 'historiaclinica/nuevo.html', {'form': form})


@login_required
def ver_historia(request, id):
    historia = get_object_or_404(Historiaclinica, pk=id)
    evoluciones = []
    if Evolucionclinica:
        evoluciones = Evolucionclinica.objects.filter(idhistoria=historia).order_by('-fecha')
    return render(request, 'historiaclinica/ver.html', {
        'historia': historia,
        'evoluciones': evoluciones,
    })


@login_required
def editar_historia(request, id):
    historia = get_object_or_404(Historiaclinica, pk=id)
    if request.method == 'POST':
        form = HistoriaClinicaForm(request.POST, instance=historia)
        if form.is_valid():
            historia = form.save(commit=False)
            historia.ultimaactualizacion = timezone.now()
            historia.save()
            messages.success(request, 'Historia clínica actualizada.')
            return redirect('ver_historia', id=id)
    else:
        form = HistoriaClinicaForm(instance=historia)
    return render(request, 'historiaclinica/editar.html', {'form': form, 'historia': historia})


@login_required
def eliminar_historia(request, id):
    historia = get_object_or_404(Historiaclinica, pk=id)
    historia.delete()
    messages.success(request, 'Historia clínica eliminada.')
    return redirect('lista_historias')