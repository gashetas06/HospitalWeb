from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UsuarioManager(BaseUserManager):
    def create_user(self, cedula, password=None, **extra_fields):
        if not cedula:
            raise ValueError('La cédula es obligatoria')
        user = self.model(cedula=cedula, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cedula, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', 'admin')
        return self.create_user(cedula, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    ROL_CHOICES = [
        ('admin',    'Administrador'),
        ('medico',   'Médico'),
        ('empleado', 'Empleado'),
        ('paciente', 'Paciente'),
    ]

    cedula       = models.CharField(max_length=20, unique=True)
    nombre       = models.CharField(max_length=200)
    rol          = models.CharField(max_length=20, choices=ROL_CHOICES, default='empleado')
    activo       = models.BooleanField(default=True)

    # Referencia opcional al registro real (para médico/empleado/paciente)
    medico_id    = models.IntegerField(null=True, blank=True)
    empleado_id  = models.IntegerField(null=True, blank=True)
    paciente_id  = models.IntegerField(null=True, blank=True)

    is_staff     = models.BooleanField(default=False)
    is_active    = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    objects = UsuarioManager()

    USERNAME_FIELD  = 'cedula'
    REQUIRED_FIELDS = ['nombre']

    class Meta:
        db_table = 'usuarios_usuario'

    def __str__(self):
        return f"{self.nombre} ({self.rol})"