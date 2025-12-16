"""
Configuración de la aplicación gestion_apuntes.
"""

from django.apps import AppConfig


class GestionApuntesConfig(AppConfig):
    """
    Clase de configuración para la aplicación de gestión de apuntes.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestion_apuntes'

    def ready(self):
        """
        Método que se ejecuta cuando la aplicación está lista.
        Importa las señales para asegurar que se registren.
        """
        import gestion_apuntes.signals
