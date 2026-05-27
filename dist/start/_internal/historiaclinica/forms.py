### historiaclinica/forms.py ###

from django import forms
from .models import Historiaclinica

class HistoriaClinicaForm(forms.ModelForm):
    class Meta:
        model = Historiaclinica
        fields = [
            'idpaciente', 'alergias', 'antecedentespersonales',
            'antecedentesfamiliares', 'observaciones'
        ]
        widgets = {
            'alergias': forms.TextInput(),
            'antecedentespersonales': forms.Textarea(attrs={'rows': 3}),
            'antecedentesfamiliares': forms.Textarea(attrs={'rows': 3}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'idpaciente': 'Paciente',
            'alergias': 'Alergias',
            'antecedentespersonales': 'Antecedentes Personales',
            'antecedentesfamiliares': 'Antecedentes Familiares',
            'observaciones': 'Observaciones',
        }