"""
Configuración de la aplicación gestion_carreras.
"""

from django.apps import AppConfig


class GestionCarrerasConfig(AppConfig):
    """
    Clase de configuración para la aplicación de gestión de carreras.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestion_carreras'
