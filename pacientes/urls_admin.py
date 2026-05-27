from django.urls import path
from . import views_admin
 
urlpatterns = [
    path('admin/',                    views_admin.admin_lista_pacientes,  name='admin_lista_pacientes'),
    path('admin/nuevo/',              views_admin.admin_nuevo_paciente,   name='admin_nuevo_paciente'),
    path('admin/editar/<int:id>/',    views_admin.admin_editar_paciente,  name='admin_editar_paciente'),
    path('admin/eliminar/<int:id>/',  views_admin.admin_eliminar_paciente, name='admin_eliminar_paciente'),
]