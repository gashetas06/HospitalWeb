from django.urls import path
from . import views_admin
from . import views_paciente

urlpatterns = [
    # ADMIN
    path('',                   views_admin.admin_lista_pacientes,   name='admin_lista_pacientes'),
    path('nuevo/',             views_admin.admin_nuevo_paciente,    name='admin_nuevo_paciente'),
    path('editar/<int:id>/',   views_admin.admin_editar_paciente,   name='admin_editar_paciente'),
    path('eliminar/<int:id>/', views_admin.admin_eliminar_paciente, name='admin_eliminar_paciente'),

    # PORTAL PACIENTE
    path('dashboard/',        views_paciente.dashboard_paciente,       name='dashboard_paciente'),
    path('mis-citas/',        views_paciente.mis_citas_paciente,        name='mis_citas_paciente'),
    path('mi-historia/',      views_paciente.mi_historia,               name='mi_historia'),
    path('cambiar-password/', views_paciente.cambiar_password_paciente, name='cambiar_password_paciente'),
]