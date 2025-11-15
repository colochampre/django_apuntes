from django.urls import path
from . import views

app_name = 'gestion_materias'

urlpatterns = [
    # URL para ver las materias filtradas por carrera
    # ej: /materias/por_carrera/1/
    path('por_carrera/<int:carrera_id>/', views.listar_materias_por_carrera, name='materias_por_carrera'),
    
    # (Opcional) Podrías tener también una URL para ver TODAS las materias sin filtrar
    # path('', views.listar_todas_las_materias, name='lista_completa_materias'),
]
