from django.db import models
from gestion_usuarios.models import Usuario
from gestion_materias.models import Materia

PUNTUACION = {
    ("1", "☆"),
    ("2", "☆☆"),
    ("3", "☆☆☆"),
    ("4", "☆☆☆☆"),
    ("5", "☆☆☆☆☆"),
}

# Create your models here.
class Apunte(models.Model):
    titulo = models.CharField(max_length=100, null=False, blank=False)
    descripcion = models.TextField()
    archivo = models.FileField(upload_to='apuntes/')
    fecha_publicacion = models.DateField(auto_now_add=True)
    materia = models.ForeignKey(Materia, on_delete=models.SET_NULL, null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    puntuacion = models.CharField(max_length=3, choices= PUNTUACION, null= True, blank=True)
    
    class Meta:
        ordering = ['titulo']
    
    def __str__(self):
        return (f'{self.titulo} - {self.fecha_publicacion} - '
                f'{self.usuario.user.username} - {self.fecha_publicacion} - {self.get_puntuacion_display()}')

