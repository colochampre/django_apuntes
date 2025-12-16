"""
Configuración de la aplicación gestion_usuarios.
"""

from django.apps import AppConfig


class GestionUsuariosConfig(AppConfig):
    """
    Clase de configuración para la aplicación de gestión de usuarios.
    
    Define el campo automático por defecto y el nombre de la aplicación.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestion_usuarios'
