from django.urls import path
from . import views

urlpatterns = [
    path('',                   views.lista_facturas,   name='lista_facturas'),
    path('nueva/',             views.nueva_factura,    name='nueva_factura'),
    path('<int:id>/',          views.ver_factura,      name='ver_factura'),
    path('editar/<int:id>/',   views.editar_factura,   name='editar_factura'),
    path('eliminar/<int:id>/', views.eliminar_factura, name='eliminar_factura'),
]