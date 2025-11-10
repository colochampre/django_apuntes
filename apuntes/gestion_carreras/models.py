from django.db import models
from django.core.exceptions import ValidationError
from gestion_materias.models import Materia
from common import validadores as v

# Create your models here.
class Carrera(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False)
    universidad = models.CharField(max_length=100, default='UTN')
    materias = models.ManyToManyField(Materia, related_name='carreras')
    
    class Meta:
        ordering = ['nombre', 'universidad']

    def clean(self):
        if not v.es_nombre_valido(self.nombre):
            raise ValidationError('Nombre de carrera inválido')
        if not v.es_nombre_valido(self.universidad):
            raise ValidationError('Nombre de universidad inválido')

    def __str__(self):
        return f'{self.nombre} - {self.universidad}'
    