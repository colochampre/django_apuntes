from django.db import models
from common import validadores as v
from gestion_usuarios.models import Usuario
from gestion_materias.models import Materia
from django.core.exceptions import ValidationError

class Apunte(models.Model):
    """
    Representa un apunte o material de estudio subido por un usuario.
    """
    titulo = models.CharField(max_length=100, null=False, blank=False)
    descripcion = models.TextField()
    archivo = models.FileField(upload_to='apuntes/')
    fecha_publicacion = models.DateField(auto_now_add=True)
    materia = models.ForeignKey(Materia, on_delete=models.SET_NULL, null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['titulo']
    
    def clean(self):
        if not v.es_nombre_valido(self.titulo):
            raise ValidationError('Titulo inválido')
    
    def __str__(self):
        return (f'{self.titulo} - {self.fecha_publicacion} - '
                f'{self.usuario.user.username} - {self.fecha_publicacion}')

