from django.urls import path
from . import views

urlpatterns = [
    path('',                        views.lista_citas,    name='lista_citas'),
    path('cancelar/<int:id>/',      views.cancelar_cita,  name='cancelar_cita'),
    path('completar/<int:id>/',     views.completar_cita, name='completar_cita'),
]