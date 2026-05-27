from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F
from .models import Inventario
from .forms import InventarioForm


@login_required
def lista_inventario(request):
    items = Inventario.objects.select_related('idcategoria').order_by('nombreproducto')
    criticos = items.filter(cantidaddisponible__lte=F('nivelcritico')).count()
    return render(request, 'inventario/lista.html', {
        'items': items,
        'total': items.count(),
        'criticos': criticos,
    })


@login_required
def nuevo_inventario(request):
    if request.method == 'POST':
        form = InventarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto agregado al inventario.')
            return redirect('lista_inventario')
    else:
        form = InventarioForm()
    return render(request, 'inventario/nuevo.html', {'form': form})

@login_required
def editar_inventario(request, id):
    item = get_object_or_404(Inventario, pk=id)
    if request.method == 'POST':
        form = InventarioForm(request.POST, instance=item)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.idinventario = id
            # Forzar UPDATE directo, evitando el INSERT de Django
            Inventario.objects.filter(pk=id).update(
                idcategoria=obj.idcategoria,
                nombreproducto=obj.nombreproducto,
                unidadmedida=obj.unidadmedida,
                cantidaddisponible=obj.cantidaddisponible,
                nivelcritico=obj.nivelcritico,
                preciounitario=obj.preciounitario,
                proveedor=obj.proveedor,
                fechaultimaentrada=obj.fechaultimaentrada,
            )
            messages.success(request, 'Producto actualizado.')
            return redirect('lista_inventario')
    else:
        form = InventarioForm(instance=item)
    return render(request, 'inventario/editar.html', {'form': form, 'item': item})
@login_required
def eliminar_inventario(request, id):
    item = get_object_or_404(Inventario, pk=id)
    item.delete()
    messages.success(request, 'Producto eliminado.')
    return redirect('lista_inventario')
