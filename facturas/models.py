from django.db import models

class Factura(models.Model):
    idfactura = models.AutoField(db_column='idFactura', primary_key=True)
    idpaciente_id = models.IntegerField(db_column='idPaciente')
    idcita_id = models.IntegerField(db_column='idCita', blank=True, null=True)
    idinternacion_id = models.IntegerField(db_column='idInternacion', blank=True, null=True)
    fechaemision = models.DateTimeField(db_column='fechaEmision')
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    impuesto = models.DecimalField(max_digits=12, decimal_places=2)
    descuento = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    estado = models.CharField(max_length=20, db_collation='Modern_Spanish_CI_AS')
    metodopago = models.CharField(db_column='metodoPago', max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    observaciones = models.CharField(max_length=500, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Factura'

    def __str__(self):
        return f"Factura {self.idfactura}"