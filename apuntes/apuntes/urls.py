from django.contrib import admin
from django.urls import path, include
from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('usuarios/', include(('gestion_usuarios.urls', 'gestion_usuarios'), namespace='gestion_usuarios')),
    path('apuntes/', include(('gestion_apuntes.urls', 'gestion_apuntes'), namespace='gestion_apuntes')),
    path('carreras/', include(('gestion_carreras.urls', 'gestion_carreras'), namespace='gestion_carreras')),
    path('materias/', include(('gestion_materias.urls', 'gestion_materias'), namespace='gestion_materias')),
    
]
