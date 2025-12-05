from django.urls import path
from .views import apuntes, subir_apunte, descargar_apunte, puntuar_apunte

urlpatterns = [
    path('', apuntes, name='apuntes'),
    path('subir/<int:materia_id>/', subir_apunte, name='subir_apunte'),
    path('descargar/<int:apunte_id>/', descargar_apunte, name='descargar_apunte'),
    path('puntuar/<int:apunte_id>/', puntuar_apunte, name='puntuar_apunte'),
]