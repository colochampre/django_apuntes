from django.db import models
from django.core.exceptions import ValidationError
from common import validadores as v

# Create your models here.
class Materia(models.Model):
    nombre = models.CharField(max_length=50, null=False, blank=False)
    anio = models.IntegerField(null=False, blank=False)

    class Meta:
        ordering = ['nombre', 'anio']

    def clean(self):
        if not v.es_anio_valido(self.anio):
            raise ValidationError('Año inválido')
        if not v.es_nombre_valido(self.nombre):
            raise ValidationError('Nombre inválido')

    def __str__(self):
        return f'{self.nombre} - {self.anio}'