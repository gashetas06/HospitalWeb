from django import forms
from django.core.exceptions import ValidationError
import re
import datetime
from .models import Medico, Especialidad, Departamento


class MedicoForm(forms.ModelForm):
    idespecialidad = forms.ModelChoiceField(
        queryset=Especialidad.objects.all(),
        label='Especialidad',
        empty_label='-- Selecciona --'
    )
    iddepartamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        label='Departamento',
        empty_label='-- Selecciona --'
    )

    class Meta:
        model = Medico
        fields = [
            'cedula', 'nombre', 'apellido',
            'idespecialidad', 'iddepartamento',
            'telefono', 'email', 'fechaingreso', 'activo'
        ]
        widgets = {
            'fechaingreso': forms.DateInput(attrs={'type': 'date'}),
        }

    # --- Cédula: alfanumérico ---
    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula', '').strip()
        if not re.match(r'^[A-Za-z0-9]+$', cedula):
            raise ValidationError('La cédula solo puede contener letras y números, sin espacios ni caracteres especiales.')
        return cedula.upper()

    # --- Nombre: solo letras y espacios ---
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if not re.match(r'^[A-Za-záéíóúÁÉÍÓÚüÜñÑ\s]+$', nombre):
            raise ValidationError('El nombre solo puede contener letras.')
        return nombre.title()

    # --- Apellido: solo letras y espacios ---
    def clean_apellido(self):
        apellido = self.cleaned_data.get('apellido', '').strip()
        if not re.match(r'^[A-Za-záéíóúÁÉÍÓÚüÜñÑ\s]+$', apellido):
            raise ValidationError('El apellido solo puede contener letras.')
        return apellido.title()

    # --- Teléfono: formato 000-000-0000 ---
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '')
        if not telefono:
            return telefono
        if not re.match(r'^\d{3}-\d{3}-\d{4}$', telefono):
            raise ValidationError('El teléfono debe tener el formato 000-000-0000.')
        return telefono

    # --- Fecha de ingreso: no futura, no más de 50 años atrás ---
    def clean_fechaingreso(self):
        fecha = self.cleaned_data.get('fechaingreso')
        if not fecha:
            return fecha
        hoy = datetime.date.today()
        hace_50 = hoy.replace(year=hoy.year - 50)
        if fecha > hoy:
            raise ValidationError('La fecha de ingreso no puede ser una fecha futura.')
        if fecha < hace_50:
            raise ValidationError('La fecha de ingreso no puede ser mayor a 50 años atrás.')
        return fecha