import re
import datetime
from django import forms
from django.core.exceptions import ValidationError
from .models import Empleado

CARGO_CHOICES = [
    ('', '-- Selecciona --'),
    ('Administrativo',  'Administrativo'),
    ('Enfermero/a',     'Enfermero/a'),
    ('Técnico',         'Técnico'),
    ('Limpieza',        'Limpieza'),
    ('Seguridad',       'Seguridad'),
    ('Recepcionista',   'Recepcionista'),
    ('Contador',        'Contador'),
    ('Farmacéutica',    'Farmacéutica'),
    ('Camillero',       'Camillero'),
    ('Técnico Lab.',    'Técnico Lab.'),
    ('Técnico Rayos X', 'Técnico Rayos X'),
    ('Otro',            'Otro'),
]


class EmpleadoForm(forms.ModelForm):
    cargo = forms.ChoiceField(choices=CARGO_CHOICES)

    class Meta:
        model = Empleado
        fields = [
            'cedula', 'nombre', 'apellido', 'cargo',
            'iddepartamento_id', 'salario', 'fechaingreso', 'activo'
        ]
        widgets = {
            'fechaingreso': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'cedula':            'Cédula',
            'nombre':            'Nombre',
            'apellido':          'Apellido',
            'cargo':             'Cargo',
            'iddepartamento_id': 'ID Departamento',
            'salario':           'Salario',
            'fechaingreso':      'Fecha de Ingreso',
            'activo':            'Activo',
        }

    # CÉDULA → alfanumérico
    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula', '').strip()
        if not re.fullmatch(r'[A-Za-z0-9]+', cedula):
            raise ValidationError('La cédula solo puede contener letras y números, sin espacios ni caracteres especiales.')
        return cedula.upper()

    # NOMBRE → solo letras
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if not re.fullmatch(r'[A-Za-záéíóúÁÉÍÓÚüÜñÑ\s]+', nombre):
            raise ValidationError('El nombre solo puede contener letras.')
        return nombre.title()

    # APELLIDO → solo letras
    def clean_apellido(self):
        apellido = self.cleaned_data.get('apellido', '').strip()
        if not re.fullmatch(r'[A-Za-záéíóúÁÉÍÓÚüÜñÑ\s]+', apellido):
            raise ValidationError('El apellido solo puede contener letras.')
        return apellido.title()

    # SALARIO → no negativo
    def clean_salario(self):
        salario = self.cleaned_data.get('salario')
        if salario is not None and salario < 0:
            raise ValidationError('El salario no puede ser negativo.')
        return salario

    # FECHA DE INGRESO → no futura, no más de 50 años atrás
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