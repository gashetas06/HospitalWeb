import re
from decimal import Decimal

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Inventario, Categoriainventario


class InventarioForm(forms.ModelForm):

    idcategoria = forms.ModelChoiceField(
        queryset=Categoriainventario.objects.all(),
        label='Categoría',
        empty_label='-- Selecciona --'
    )

    class Meta:
        model = Inventario
        fields = [
            'idcategoria',
            'nombreproducto',
            'unidadmedida',
            'cantidaddisponible',
            'nivelcritico',
            'preciounitario',
            'proveedor',
            'fechaultimaentrada'
        ]

        widgets = {
            'fechaultimaentrada': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}
            ),
        }

        labels = {
            'nombreproducto': 'Nombre del Producto',
            'unidadmedida': 'Unidad de Medida',
            'cantidaddisponible': 'Cantidad Disponible',
            'nivelcritico': 'Nivel Crítico',
            'preciounitario': 'Precio Unitario',
            'proveedor': 'Proveedor',
            'fechaultimaentrada': 'Última Entrada',
        }

    def clean_nombreproducto(self):
        nombre = self.cleaned_data['nombreproducto'].strip()
        if not re.fullmatch(r'[A-Za-zÁÉÍÓÚáéíóúÑñ0-9().,%\- ]+', nombre):
            raise ValidationError("El nombre contiene caracteres no permitidos.")
        return nombre

    def clean_unidadmedida(self):
        unidad = self.cleaned_data['unidadmedida'].strip()
        if not re.fullmatch(r'[A-Za-zÁÉÍÓÚáéíóúÑñ ]+', unidad):
            raise ValidationError("La unidad de medida solo puede contener letras.")
        return unidad

    def clean_cantidaddisponible(self):
        cantidad = self.cleaned_data['cantidaddisponible']
        if cantidad < 0:
            raise ValidationError("La cantidad no puede ser negativa.")
        return cantidad

    def clean_nivelcritico(self):
        nivel = self.cleaned_data['nivelcritico']
        if nivel < 0:
            raise ValidationError("El nivel crítico no puede ser negativo.")
        return nivel

    def clean_preciounitario(self):
        precio = self.cleaned_data.get('preciounitario')
        if precio is None:
            return precio
        if precio < Decimal('0'):
            raise ValidationError("El precio no puede ser negativo.")
        return precio

    def clean_proveedor(self):
        proveedor = self.cleaned_data.get('proveedor')
        if not proveedor:
            return proveedor
        proveedor = proveedor.strip()
        if not re.fullmatch(r'[A-Za-zÁÉÍÓÚáéíóúÑñ0-9.,&\- ]+', proveedor):
            raise ValidationError("El proveedor contiene caracteres no permitidos.")
        return proveedor

    def clean_fechaultimaentrada(self):
        fecha = self.cleaned_data.get('fechaultimaentrada')
        if not fecha:
            return fecha
        if fecha > timezone.now():
            raise ValidationError("La fecha no puede ser futura.")
        return fecha

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombreproducto')
        unidad = cleaned_data.get('unidadmedida')
        cantidad = cleaned_data.get('cantidaddisponible')
        nivel = cleaned_data.get('nivelcritico')
        precio = cleaned_data.get('preciounitario')

        if nombre and not re.fullmatch(r'[A-Za-zÁÉÍÓÚáéíóúÑñ0-9().,%\- ]+', nombre.strip()):
            self.add_error('nombreproducto', 'Nombre inválido.')

        if unidad and not re.fullmatch(r'[A-Za-zÁÉÍÓÚáéíóúÑñ ]+', unidad.strip()):
            self.add_error('unidadmedida', 'Solo letras.')

        if cantidad is not None and cantidad < 0:
            self.add_error('cantidaddisponible', 'No puede ser negativo.')

        if nivel is not None and nivel < 0:
            self.add_error('nivelcritico', 'No puede ser negativo.')

        if precio is not None and precio < 0:
            self.add_error('preciounitario', 'No puede ser negativo.')

        if cantidad is not None and nivel is not None and nivel > cantidad:
            self.add_error('nivelcritico', 'No puede ser mayor al stock.')

        return cleaned_data