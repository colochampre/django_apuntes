"""
Configuración del panel de administración para la gestión de usuarios.

Este módulo define cómo se visualiza y gestiona el modelo Usuario en el panel de administración de Django.
"""

from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    """
    Configuración de la interfaz administrativa para el modelo Usuario.

    Define las columnas a mostrar en la lista de usuarios y el ordenamiento predeterminado.
    Incluye un método auxiliar para visualizar las carreras asociadas.
    """
    list_display = ("user__username", "mostrar_carreras")
    ordering = ("carrera", "user__username")
    
    def mostrar_carreras(self, obj):
        """
        Retorna una cadena con los nombres de las carreras separadas por comas.
        
        Args:
            obj (Usuario): Instancia del usuario.
            
        Returns:
            str: Nombres de las carreras concatenados.
        """
        return ", " .join([c.nombre for c in obj.carrera.all()])
    mostrar_carreras.short_description = "carreras"