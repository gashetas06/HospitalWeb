from django.urls import path
from . import views

urlpatterns = [
    path('',                   views.lista_historias,  name='lista_historias'),
    path('nueva/',             views.nueva_historia,   name='nueva_historia'),
    path('ver/<int:id>/',          views.ver_historia,     name='ver_historia'),
    path('editar/<int:id>/',   views.editar_historia,  name='editar_historia'),
    path('eliminar/<int:id>/', views.eliminar_historia, name='eliminar_historia'),
]