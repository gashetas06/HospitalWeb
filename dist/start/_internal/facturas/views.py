from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Factura
from .forms import FacturaForm

try:
    from pacientes.models import Paciente
except ImportError:
    Paciente = None


@login_required
def lista_facturas(request):
    facturas = Factura.objects.all().order_by('-fechaemision')
    total_pagadas = facturas.filter(estado='Pagada').count()
    total_pendientes = facturas.filter(estado='Pendiente').count()
    return render(request, 'facturas/lista.html', {
        'facturas': facturas,
        'total_pagadas': total_pagadas,
        'total_pendientes': total_pendientes,
    })


@login_required
def nueva_factura(request):
    if request.method == 'POST':
        form = FacturaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Factura creada correctamente.')
            return redirect('lista_facturas')
    else:
        form = FacturaForm()
    return render(request, 'facturas/nuevo.html', {'form': form})


@login_required
def editar_factura(request, id):
    factura = get_object_or_404(Factura, pk=id)
    if request.method == 'POST':
        form = FacturaForm(request.POST, instance=factura)
        if form.is_valid():
            form.save()
            messages.success(request, 'Factura actualizada.')
            return redirect('lista_facturas')
    else:
        form = FacturaForm(instance=factura)
    return render(request, 'facturas/editar.html', {'form': form, 'factura': factura})


@login_required
def eliminar_factura(request, id):
    factura = get_object_or_404(Factura, pk=id)
    factura.delete()
    messages.success(request, 'Factura eliminada.')
    return redirect('lista_facturas')


@login_required
def ver_factura(request, id):
    factura = get_object_or_404(Factura, pk=id)
    paciente = None
    if Paciente:
        try:
            paciente = Paciente.objects.get(idpaciente=factura.idpaciente_id)
        except Paciente.DoesNotExist:
            pass
    return render(request, 'facturas/ver.html', {
        'factura': factura,
        'paciente': paciente,
    })