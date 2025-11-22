from django.urls import path
from .views import apuntes, subir_apunte

urlpatterns = [
    path('', apuntes, name='apuntes'),
    path('subir/', subir_apunte, name='subir_apunte'),
]
