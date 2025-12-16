"""
Configuración del panel de administración para la gestión de materias.

Este módulo define cómo se visualiza y gestiona el modelo Materia en el panel de administración de Django.
"""

from django.contrib import admin
from .models import Materia

@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    """
    Configuración de la interfaz administrativa para el modelo Materia.
    
    Permite visualizar las materias ordenadas por año y nombre.
    """
    list_display = ("nombre", "anio")
    ordering = ("anio", "nombre")
    