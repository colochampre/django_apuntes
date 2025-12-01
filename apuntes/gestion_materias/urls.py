from django.urls import path
from . import views

app_name = 'gestion_materias'

urlpatterns = [
    path('por_carrera/<int:carrera_id>/', views.listar_materias_por_carrera, name='materias_por_carrera'),
]