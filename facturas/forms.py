import datetime
from decimal import Decimal

from django import forms
from django.core.exceptions import ValidationError

from .models import Factura


ESTADO_CHOICES = [
    ('', '-- Selecciona --'),
    ('Pendiente', 'Pendiente'),
    ('Pagada', 'Pagada'),
    ('Anulada', 'Anulada'),
]


METODO_CHOICES = [
    ('', '-- Selecciona --'),
    ('Efectivo', 'Efectivo'),
    ('Tarjeta', 'Tarjeta'),
    ('Transferencia', 'Transferencia'),
    ('Seguro', 'Seguro'),
]


class FacturaForm(forms.ModelForm):

    estado = forms.ChoiceField(
        choices=ESTADO_CHOICES
    )

    metodopago = forms.ChoiceField(
        choices=METODO_CHOICES,
        required=False
    )


    class Meta:

        model = Factura

        fields = [
            'idpaciente_id',
            'idcita_id',
            'idinternacion_id',
            'fechaemision',
            'subtotal',
            'impuesto',
            'descuento',
            'estado',
            'metodopago',
            'observaciones'
        ]

        widgets = {
            'fechaemision': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local'
                }
            ),
        }


    # ID PACIENTE
    def clean_idpaciente_id(self):

        paciente = self.cleaned_data.get(
            'idpaciente_id'
        )

        if paciente < 1:

            raise ValidationError(
                'El ID no puede ser negativo.'
            )

        if paciente > 999999:

            raise ValidationError(
                'El ID excede el límite permitido.'
            )

        return paciente


    # SUBTOTAL
    def clean_subtotal(self):

        subtotal = self.cleaned_data.get(
            'subtotal'
        )

        if subtotal < 0:

            raise ValidationError(
                'El subtotal no puede ser negativo.'
            )

        if subtotal > Decimal('999999.99'):

            raise ValidationError(
                'Subtotal demasiado elevado.'
            )

        return subtotal


    # IMPUESTO
    def clean_impuesto(self):

        impuesto = self.cleaned_data.get(
            'impuesto'
        )

        if impuesto < 0:

            raise ValidationError(
                'El impuesto no puede ser negativo.'
            )

        if impuesto > Decimal('999999.99'):

            raise ValidationError(
                'Impuesto demasiado elevado.'
            )

        return impuesto


    # DESCUENTO
    def clean_descuento(self):

        descuento = self.cleaned_data.get(
            'descuento'
        )

        if descuento is None:

            return descuento


        if descuento < 0:

            raise ValidationError(
                'El descuento no puede ser negativo.'
            )

        if descuento > Decimal('999999.99'):

            raise ValidationError(
                'Descuento demasiado elevado.'
            )

        return descuento


    # FECHA
    def clean_fechaemision(self):

        fecha = self.cleaned_data.get(
            'fechaemision'
        )

        hoy = datetime.datetime.now()

        hace_50 = hoy.replace(
            year=hoy.year - 50
        )

        if fecha > hoy:

            raise ValidationError(
                'La fecha no puede ser futura.'
            )

        if fecha < hace_50:

            raise ValidationError(
                'La fecha no puede superar 50 años.'
            )

        return fecha