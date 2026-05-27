from django.db import models

class Paciente(models.Model):
    idpaciente = models.AutoField(db_column='idPaciente', primary_key=True)
    cedula = models.CharField(unique=True, max_length=20)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fechanacimiento = models.DateField(db_column='fechaNacimiento')
    sexo = models.CharField(max_length=1)
    tiposangre = models.CharField(db_column='tipoSangre', max_length=5, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    contactoemergencianombre = models.CharField(db_column='contactoEmergenciaNombre', max_length=150, blank=True, null=True)
    contactoemergenciatelefono = models.CharField(db_column='contactoEmergenciaTelefono', max_length=20, blank=True, null=True)
    activo = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'Paciente'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"