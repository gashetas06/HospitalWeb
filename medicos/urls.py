from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_medicos, name='lista_medicos'),
    path('nuevo/', views.nuevo_medico, name='nuevo_medico'),
    path('editar/<int:id>/', views.editar_medico, name='editar_medico'),
    path('eliminar/<int:id>/', views.eliminar_medico, name='eliminar_medico'),
    path('dashboard/', views.dashboard_medico, name='dashboard_medico'),
    path('cambiar-password/', views.cambiar_password, name='cambiar_password'),
    path('mis-citas/', views.mis_citas, name='mis_citas'),
    path('cita/<int:id>/', views.ver_cita, name='ver_cita'),
    path('cita/<int:id>/atender/',  views.atender_cita,  name='atender_cita'),
    path('cita/<int:id>/cancelar/', views.cancelar_cita, name='cancelar_cita'),
    path('mis-pacientes/', views.mis_pacientes, name='mis_pacientes'),
    path('paciente/<int:id>/', views.ver_paciente, name='ver_paciente'),
    path('internaciones/', views.mis_internaciones,  name='mis_internaciones'),
    path('internar/', views.internar_paciente,  name='internar_paciente'),
    path('internar/<int:paciente_id>/', views.internar_paciente, name='internar_paciente_id'),
    path('alta/<int:internacion_id>/', views.dar_alta, name='dar_alta'),
]