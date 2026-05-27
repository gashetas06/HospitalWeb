from django.db import models

class Cita(models.Model):
    idcita = models.AutoField(db_column='idCita', primary_key=True)
    idpaciente = models.ForeignKey(
        'pacientes.Paciente', models.DO_NOTHING, db_column='idPaciente'
    )
    idmedico = models.ForeignKey(
        'medicos.Medico', models.DO_NOTHING, db_column='idMedico'
    )
    idempleadoregistra_id = models.IntegerField(db_column='idEmpleadoRegistra', blank=True, null=True)
    fecha = models.DateField()
    hora = models.TimeField()
    duracionminutos = models.SmallIntegerField(db_column='duracionMinutos')
    tipocita = models.CharField(db_column='tipoCita', max_length=50, db_collation='Modern_Spanish_CI_AS')
    estado = models.CharField(max_length=30, db_collation='Modern_Spanish_CI_AS')
    motivocancelacion = models.CharField(db_column='motivoCancelacion', max_length=255, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    notas = models.CharField(max_length=500, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    fechacreacion = models.DateTimeField(db_column='fechaCreacion')

    class Meta:
        managed = False
        db_table = 'Cita'

    def __str__(self):
        return f"Cita {self.idcita}"