"""
Configuración de la aplicación gestion_materias.
"""

from django.apps import AppConfig


class GestionMateriasConfig(AppConfig):
    """
    Clase de configuración para la aplicación de gestión de materias.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestion_materias'
