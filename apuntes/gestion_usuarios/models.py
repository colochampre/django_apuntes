from django.db import models
from gestion_carreras.models import Carrera
from django.contrib.auth.models import User

class Usuario(models.Model):
    """
    Extiende el modelo de usuario por defecto de Django para incluir
    información específica de la aplicación, como la carrera del usuario.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    carrera = models.ManyToManyField(Carrera, related_name='usuarios')

    class Meta:
        ordering = ['user__first_name', 'user__last_name']
    
    def __str__(self):
        return f'{self.user.username}'