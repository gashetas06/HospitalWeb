from django.db import models

class Empleado(models.Model):
    idempleado = models.AutoField(db_column='idEmpleado', primary_key=True)
    cedula = models.CharField(unique=True, max_length=20, db_collation='Modern_Spanish_CI_AS')
    nombre = models.CharField(max_length=100, db_collation='Modern_Spanish_CI_AS')
    apellido = models.CharField(max_length=100, db_collation='Modern_Spanish_CI_AS')
    cargo = models.CharField(max_length=100, db_collation='Modern_Spanish_CI_AS')
    iddepartamento_id = models.IntegerField(db_column='idDepartamento')
    salario = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    fechaingreso = models.DateField(db_column='fechaIngreso')
    activo = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'Empleado'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"