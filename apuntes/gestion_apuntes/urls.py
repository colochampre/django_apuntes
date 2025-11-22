from django.urls import path
from .views import apuntes, subir_apunte, descargar_apunte, buscar_apunte

urlpatterns = [
    path('', apuntes, name='apuntes'),
    path('subir/', subir_apunte, name='subir_apunte'),
    path('buscar/', buscar_apunte, name='buscar_apunte'),
    path('descargar/<int:apunte_id>/', descargar_apunte, name='descargar_apunte'),
]
