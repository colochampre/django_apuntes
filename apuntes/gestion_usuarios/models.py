from django.db import models
from gestion_carreras.models import Carrera
from django.contrib.auth.models import User

# Create your models here.
class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    carrera = models.ManyToManyField(Carrera, related_name='usuarios')

    class Meta:
        ordering = ['user__first_name', 'user__last_name']
    
    def __str__(self):
        return f'{self.user.username}'