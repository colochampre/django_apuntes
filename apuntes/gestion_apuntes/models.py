from django.db import models
from django.db.models import Avg
from gestion_usuarios.models import Usuario
from gestion_materias.models import Materia

# Create your models here.
class Apunte(models.Model):
    titulo = models.CharField(max_length=100, null=False, blank=False)
    descripcion = models.TextField()
    archivo = models.FileField(upload_to='apuntes/')
    fecha_publicacion = models.DateField(auto_now_add=True)
    materia = models.ForeignKey(Materia, on_delete=models.SET_NULL, null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['titulo']
    
    def __str__(self):
        return (f'{self.titulo} - {self.fecha_publicacion} - '
                f'{self.usuario.user.username if self.usuario else "Anónimo"} - {self.fecha_publicacion}')
    
    def promedio_puntuacion(self):
        """Calcula el promedio de las puntuaciones del apunte."""
        promedio = self.puntuaciones.aggregate(Avg('valor'))['valor__avg']
        return round(promedio, 1) if promedio else None
    
    def total_puntuaciones(self):
        """Retorna el total de puntuaciones recibidas."""
        return self.puntuaciones.count()
    
    def puntuacion_usuario(self, usuario):
        """Retorna la puntuación que un usuario específico dio a este apunte."""
        try:
            puntuacion = self.puntuaciones.get(usuario=usuario)
            return puntuacion.valor
        except Puntuacion.DoesNotExist:
            return None


class Puntuacion(models.Model):
    """Modelo para almacenar las puntuaciones individuales de cada usuario a un apunte."""
    apunte = models.ForeignKey(Apunte, on_delete=models.CASCADE, related_name='puntuaciones')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    valor = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    fecha = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('apunte', 'usuario')  # Un usuario solo puede puntuar una vez cada apunte
        ordering = ['-fecha']
    
    def __str__(self):
        return f'{self.usuario.user.username} - {self.apunte.titulo} - {self.valor}★'

