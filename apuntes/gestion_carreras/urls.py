from django.urls import path
from .views import lista_carreras, eliminar_carrera

app_name = 'gestion_carreras'

urlpatterns = [
    path('', lista_carreras, name='lista_carreras'),
    path('eliminar/<int:carrera_id>/', eliminar_carrera, name='eliminar_carrera'),
]