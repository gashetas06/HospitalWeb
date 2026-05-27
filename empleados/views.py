from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Empleado
from .forms import EmpleadoForm


@login_required
def lista_empleados(request):
    empleados = Empleado.objects.all().order_by('apellido')
    total_activos = empleados.filter(activo=True).count()
    return render(request, 'empleados/lista.html', {
        'empleados': empleados,
        'total_activos': total_activos,
    })


@login_required
def nuevo_empleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado creado correctamente.')
            return redirect('lista_empleados')
    else:
        form = EmpleadoForm()
    return render(request, 'empleados/nuevo.html', {'form': form})


@login_required
def editar_empleado(request, id):
    empleado = get_object_or_404(Empleado, pk=id)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado actualizado correctamente.')
            return redirect('lista_empleados')
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, 'empleados/editar.html', {'form': form, 'empleado': empleado})


@login_required
def eliminar_empleado(request, id):
    empleado = get_object_or_404(Empleado, pk=id)
    empleado.delete()
    messages.success(request, 'Empleado eliminado correctamente.')
    return redirect('lista_empleados')