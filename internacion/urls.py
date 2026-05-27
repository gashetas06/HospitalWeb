from django.urls import path
from . import views

urlpatterns = [
    path('',                    views.lista_internaciones, name='lista_internaciones'),
    path('nuevo/',              views.nueva_internacion,   name='nueva_internacion'),
    path('alta/<int:id>/',      views.dar_alta_admin,      name='dar_alta_admin'),
    path('eliminar/<int:id>/',  views.eliminar_internacion, name='eliminar_internacion'),
    # Las rutas del médico ya están en medicos/urls.py
]