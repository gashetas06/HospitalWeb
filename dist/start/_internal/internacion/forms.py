### internacion/forms.py ###

from django import forms
from .models import Internacion, Cama

CONDICION_CHOICES = [
    ('', '-- Selecciona --'),
    ('Alta médica', 'Alta médica'),
    ('Alta voluntaria', 'Alta voluntaria'),
    ('Traslado', 'Traslado'),
    ('Fallecido', 'Fallecido'),
]

class InternacionForm(forms.ModelForm):
    idcama = forms.ModelChoiceField(
        queryset=Cama.objects.filter(estado='Libre'),
        label='Cama',
        empty_label='-- Selecciona cama libre --'
    )

    class Meta:
        model = Internacion
        fields = [
            'idpaciente_id', 'idcama', 'idmedicotratante_id',
            'fechaingreso', 'motivoingreso'
        ]
        widgets = {
            'fechaingreso': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        labels = {
            'idpaciente_id': 'ID Paciente',
            'idmedicotratante_id': 'ID Médico Tratante',
            'fechaingreso': 'Fecha de Ingreso',
            'motivoingreso': 'Motivo de Ingreso',
        }


class AltaForm(forms.ModelForm):
    condicionegreso = forms.ChoiceField(choices=CONDICION_CHOICES, label='Condición de Egreso')

    class Meta:
        model = Internacion
        fields = ['fechaegreso', 'diagnosticoegreso', 'condicionegreso']
        widgets = {
            'fechaegreso': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        labels = {
            'fechaegreso': 'Fecha de Egreso',
            'diagnosticoegreso': 'Diagnóstico de Egreso',
        }