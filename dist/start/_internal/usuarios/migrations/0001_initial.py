from django.db import migrations, models
import django.contrib.auth.models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ('auth', '0001_initial'),
]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False)),
                ('cedula', models.CharField(max_length=20, unique=True)),
                ('nombre', models.CharField(max_length=200)),
                ('rol', models.CharField(choices=[('admin','Administrador'),('medico','Médico'),('empleado','Empleado'),('paciente','Paciente')], default='empleado', max_length=20)),
                ('activo', models.BooleanField(default=True)),
                ('medico_id', models.IntegerField(blank=True, null=True)),
                ('empleado_id', models.IntegerField(blank=True, null=True)),
                ('paciente_id', models.IntegerField(blank=True, null=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, related_name='usuario_set', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='usuario_set', to='auth.permission')),
            ],
            options={
                'db_table': 'usuarios_usuario',
            },
        ),
    ]