"""
Señales para la aplicación de gestión de apuntes.
Maneja la limpieza de archivos físicos al eliminar registros de la base de datos.
"""
import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Apunte

@receiver(post_delete, sender=Apunte)
def eliminar_archivo_apunte(sender, instance, **kwargs):
    """
    Elimina el archivo físico asociado al apunte cuando este es eliminado de la base de datos.
    
    Args:
        sender: El modelo que envía la señal (Apunte).
        instance: La instancia del modelo que está siendo eliminada.
        kwargs: Argumentos adicionales.
    """
    if instance.archivo:
        if os.path.isfile(instance.archivo.path):
            try:
                os.remove(instance.archivo.path)
            except Exception as e:
                # En producción se podría loguear este error
                print(f"Error al eliminar archivo: {e}")
