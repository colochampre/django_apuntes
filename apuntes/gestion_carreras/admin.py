"""
Configuración del panel de administración para la gestión de carreras.

Este módulo define cómo se visualiza y gestiona el modelo Carrera en el panel de administración de Django.
"""

from django.contrib import admin
from .models import Carrera

@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):
    """
    Configuración de la interfaz administrativa para el modelo Carrera.
    
    Permite visualizar las carreras, filtrar por materias y definir los campos editables.
    """
    list_display = ("nombre", "universidad", "get_materias")
    filter_horizontal = ("materias",)
    list_filter = ("materias",)
    fields = ["nombre", "universidad","materias"]
    
    def get_materias(self, obj):
        """
        Retorna una cadena con los nombres de las materias asociadas.

        Args:
            obj (Carrera): Instancia de la carrera.

        Returns:
            str: Nombres de las materias separados por comas.
        """
        return ", " .join ([materia.nombre for materia in obj.materias.all ()])
    get_materias.short_description = "materias"
   
