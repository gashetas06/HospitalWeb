import re
import datetime
from django import forms
from django.core.exceptions import ValidationError
from .models import Paciente


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            'cedula', 'nombre', 'apellido',
            'fechanacimiento', 'sexo', 'tiposangre',
            'telefono', 'email', 'direccion',
            'contactoemergencianombre', 'contactoemergenciatelefono',
            'activo'
        ]

    # CÉDULA → alfanumérico (letras y números)
    def clean_cedula(self):
        cedula = self.cleaned_data['cedula'].strip()
        if not re.fullmatch(r'[A-Za-z0-9]+', cedula):
            raise ValidationError('La cédula solo puede contener letras y números, sin espacios ni caracteres especiales.')
        return cedula.upper()

    # NOMBRE → solo letras
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip()
        if not re.fullmatch(r'[A-Za-zÁÉÍÓÚáéíóúÑñ ]+', nombre):
            raise ValidationError('El nombre solo puede contener letras.')
        return nombre.title()

    # APELLIDO → solo letras
    def clean_apellido(self):
        apellido = self.cleaned_data['apellido'].strip()
        if not re.fullmatch(r'[A-Za-zÁÉÍÓÚáéíóúÑñ ]+', apellido):
            raise ValidationError('El apellido solo puede contener letras.')
        return apellido.title()

    # FECHA DE NACIMIENTO → no futura, no más de 100 años atrás
    def clean_fechanacimiento(self):
        fecha = self.cleaned_data.get('fechanacimiento')
        if not fecha:
            return fecha
        hoy = datetime.date.today()
        hace_100 = hoy.replace(year=hoy.year - 100)
        if fecha > hoy:
            raise ValidationError('La fecha de nacimiento no puede ser una fecha futura.')
        if fecha < hace_100:
            raise ValidationError('La fecha de nacimiento no puede ser mayor a 100 años atrás.')
        return fecha

    # TELÉFONO → 000-000-0000
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono:
            return telefono
        telefono = telefono.strip()
        if not re.fullmatch(r'\d{3}-\d{3}-\d{4}', telefono):
            raise ValidationError('Formato inválido. Use: 000-000-0000')
        return telefono

    # DIRECCIÓN → letras, números y símbolos básicos
    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion')
        if not direccion:
            return direccion
        direccion = direccion.strip()
        if not re.fullmatch(r'[A-Za-zÁÉÍÓÚáéíóúÑñ0-9#.,\- ]+', direccion):
            raise ValidationError('La dirección contiene caracteres no permitidos.')
        return direccion

    # CONTACTO EMERGENCIA → solo letras
    def clean_contactoemergencianombre(self):
        nombre = self.cleaned_data.get('contactoemergencianombre')
        if not nombre:
            return nombre
        nombre = nombre.strip()
        if not re.fullmatch(r'[A-Za-zÁÉÍÓÚáéíóúÑñ ]+', nombre):
            raise ValidationError('El nombre del contacto solo puede contener letras.')
        return nombre.title()

    # TELÉFONO EMERGENCIA → 000-000-0000
    def clean_contactoemergenciatelefono(self):
        telefono = self.cleaned_data.get('contactoemergenciatelefono')
        if not telefono:
            return telefono
        telefono = telefono.strip()
        if not re.fullmatch(r'\d{3}-\d{3}-\d{4}', telefono):
            raise ValidationError('Formato inválido. Use: 000-000-0000')
        return telefono