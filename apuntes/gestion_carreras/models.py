"""
Modelos de datos para la gestión de carreras.

Este módulo define el modelo Carrera, que representa un programa académico ofrecido por una universidad
y se relaciona con las materias que lo componen.
"""

from django.db import models
from django.core.exceptions import ValidationError
from gestion_materias.models import Materia
from common import validadores as v

# Crea tus modelos aquí.
class Carrera(models.Model):
    """
    Modelo que representa una carrera universitaria.

    Contiene información sobre el nombre de la carrera y la universidad que la dicta.
    Mantiene una relación de muchos a muchos con las materias.
    """
    nombre = models.CharField(max_length=100, null=False, blank=False)
    universidad = models.CharField(max_length=100, default='UTN')
    materias = models.ManyToManyField(Materia, related_name='carreras')
    
    class Meta:
        ordering = ['nombre', 'universidad']

    def clean(self):
        """
        Valida los campos del modelo antes de guardar.
        
        Verifica que el nombre y la universidad cumplan con los formatos permitidos.

        Raises:
            ValidationError: Si el nombre o la universidad contienen caracteres inválidos.
        """
        if not v.es_nombre_valido(self.nombre):
            raise ValidationError('Nombre de carrera inválido')
        if not v.es_nombre_valido(self.universidad):
            raise ValidationError('Nombre de universidad inválido')

    def __str__(self):
        return f'{self.nombre} - {self.universidad}'
    