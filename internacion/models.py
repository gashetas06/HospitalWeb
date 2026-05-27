from django.db import models

class Departamento(models.Model):
    iddepartamento = models.AutoField(db_column='idDepartamento', primary_key=True)
    nombre = models.CharField(unique=True, max_length=100, db_collation='Modern_Spanish_CI_AS')
    piso = models.SmallIntegerField()
    telefono = models.CharField(max_length=20, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Departamento'

class Tipohabitacion(models.Model):
    idtipo = models.AutoField(db_column='idTipo', primary_key=True)
    descripcion = models.CharField(unique=True, max_length=100, db_collation='Modern_Spanish_CI_AS')
    costodiario = models.DecimalField(db_column='costoDiario', max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'TipoHabitacion'

class Cama(models.Model):
    idcama = models.AutoField(db_column='idCama', primary_key=True)
    numero = models.CharField(unique=True, max_length=10, db_collation='Modern_Spanish_CI_AS')
    iddepartamento = models.ForeignKey(Departamento, models.DO_NOTHING, db_column='idDepartamento')
    idtipo = models.ForeignKey(Tipohabitacion, models.DO_NOTHING, db_column='idTipo')
    estado = models.CharField(max_length=20, db_collation='Modern_Spanish_CI_AS')

    class Meta:
        managed = False
        db_table = 'Cama'

class Internacion(models.Model):
    idinternacion = models.AutoField(db_column='idInternacion', primary_key=True)
    idpaciente_id = models.IntegerField(db_column='idPaciente')
    idcama = models.ForeignKey(Cama, models.DO_NOTHING, db_column='idCama')
    idmedicotratante_id = models.IntegerField(db_column='idMedicoTratante')
    fechaingreso = models.DateTimeField(db_column='fechaIngreso')
    fechaegreso = models.DateTimeField(db_column='fechaEgreso', blank=True, null=True)
    motivoingreso = models.CharField(db_column='motivoIngreso', max_length=500, db_collation='Modern_Spanish_CI_AS')
    diagnosticoegreso = models.CharField(db_column='diagnosticoEgreso', max_length=500, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    condicionegreso = models.CharField(db_column='condicionEgreso', max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Internacion'