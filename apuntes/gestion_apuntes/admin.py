"""
Configuración del panel de administración para la gestión de apuntes.

Este módulo define cómo se visualizan y gestionan los modelos Apunte y Puntuacion
en el panel de administración de Django.
"""

from django.contrib import admin
from .models import Apunte, Puntuacion

@admin.register(Apunte)
class ApunteAdmin(admin.ModelAdmin):
    """
    Configuración de la interfaz administrativa para el modelo Apunte.
    
    Define las columnas a mostrar, el ordenamiento y los filtros disponibles.
    """
    list_display = ("usuario", "titulo", "materia", "fecha_publicacion")
    ordering = ("fecha_publicacion", "materia")

@admin.register(Puntuacion)
class PuntuacionAdmin(admin.ModelAdmin):
    """
    Configuración de la interfaz administrativa para el modelo Puntuacion.
    
    Permite visualizar las puntuaciones otorgadas por los usuarios a los apuntes.
    """
    list_display = ("apunte", "usuario", "valor", "fecha")
    list_filter = ("valor", "fecha")
    ordering = ("-fecha",)