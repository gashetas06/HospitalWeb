from django.db import models

class Historiaclinica(models.Model):
    idhistoria = models.AutoField(db_column='idHistoria', primary_key=True)
    idpaciente = models.OneToOneField('pacientes.Paciente', models.DO_NOTHING, db_column='idPaciente')
    alergias = models.CharField(max_length=500, blank=True, null=True)
    antecedentespersonales = models.TextField(db_column='antecedentesPersonales', blank=True, null=True)
    antecedentesfamiliares = models.TextField(db_column='antecedentesFamiliares', blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    fechacreacion = models.DateTimeField(db_column='fechaCreacion')
    ultimaactualizacion = models.DateTimeField(db_column='ultimaActualizacion', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'HistoriaClinica'

    def __str__(self):
        return f"Historia #{self.idhistoria}"