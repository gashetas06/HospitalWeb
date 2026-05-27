from django.db import models

class Especialidad(models.Model):
    idespecialidad = models.AutoField(db_column='idEspecialidad', primary_key=True)
    nombre = models.CharField(unique=True, max_length=100, db_collation='Modern_Spanish_CI_AS')
    descripcion = models.CharField(max_length=255, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Especialidad'

    def __str__(self):
        return self.nombre  # ← esto arregla "object(1)"


class Departamento(models.Model):
    iddepartamento = models.AutoField(db_column='idDepartamento', primary_key=True)
    nombre = models.CharField(unique=True, max_length=100, db_collation='Modern_Spanish_CI_AS')
    piso = models.SmallIntegerField()
    telefono = models.CharField(max_length=20, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Departamento'

    def __str__(self):
        return self.nombre  # ← esto es lo que falta


class Medico(models.Model):
    idmedico = models.AutoField(db_column='idMedico', primary_key=True)
    cedula = models.CharField(unique=True, max_length=20, db_collation='Modern_Spanish_CI_AS')
    nombre = models.CharField(max_length=100, db_collation='Modern_Spanish_CI_AS')
    apellido = models.CharField(max_length=100, db_collation='Modern_Spanish_CI_AS')
    idespecialidad = models.ForeignKey(Especialidad, models.DO_NOTHING, db_column='idEspecialidad')
    iddepartamento = models.ForeignKey(Departamento, models.DO_NOTHING, db_column='idDepartamento')
    telefono = models.CharField(max_length=20, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    email = models.CharField(max_length=150, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    fechaingreso = models.DateField(db_column='fechaIngreso')
    activo = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'Medico'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"