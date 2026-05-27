from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/',     admin.site.urls),
    path('usuarios/',  include('usuarios.urls')),
    path('pacientes/', include('pacientes.urls')),
    path('paciente/',  include('pacientes.urls_paciente')),
    path('medicos/',   include('medicos.urls')),
    path('',           include('dashboard.urls')),
    path('citas/', include('citas.urls')),
    path('empleados/',     include('empleados.urls')),
    path('inventario/',    include('inventario.urls')),
    path('facturas/',      include('facturas.urls')),
    path('historiaclinica/', include('historiaclinica.urls')),
    path('internacion/',   include('internacion.urls')),
]
