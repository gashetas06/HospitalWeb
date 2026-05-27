from django.db import models

class Evolucionclinica(models.Model):
    idevolucion = models.AutoField(db_column='idEvolucion', primary_key=True)
    idhistoria = models.ForeignKey('historiaclinica.Historiaclinica', models.DO_NOTHING, db_column='idHistoria')
    idmedico = models.ForeignKey('medicos.Medico', models.DO_NOTHING, db_column='idMedico')
    fecha = models.DateTimeField()
    motivoconsulta = models.CharField(db_column='motivoConsulta', max_length=500)
    exploracionfisica = models.TextField(db_column='exploracionFisica', blank=True, null=True)
    diagnostico = models.TextField(blank=True, null=True)
    tratamiento = models.TextField(blank=True, null=True)
    receta = models.TextField(blank=True, null=True)
    proximarevision = models.DateField(db_column='proximaRevision', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'EvolucionClinica'

    def __str__(self):
        return f"Evolución #{self.idevolucion}"