from django.urls import path
from .views import lista_carreras

app_name = 'gestion_carreras'

urlpatterns = [
    path('', lista_carreras, name='lista_carreras'),
]