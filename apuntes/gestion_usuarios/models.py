from django.db import models
from gestion_carreras.models import Carrera
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    carrera = models.ManyToManyField(Carrera, related_name='usuarios')

    class Meta:
        ordering = ['user__first_name', 'user__last_name']
    
    def __str__(self):
        return f'{self.user.username}'

    def puntuacion_promedio(self):
        """
        Calcula el promedio de todas las puntuaciones recibidas en los apuntes del usuario.
        Retorna un valor entre 1-5 o None si no tiene puntuaciones.
        """
        from gestion_apuntes.models import Puntuacion
        
        # Obtener todas las puntuaciones de los apuntes del usuario
        puntuaciones = Puntuacion.objects.filter(apunte__usuario=self)
        promedio = puntuaciones.aggregate(Avg('valor'))['valor__avg']
        
        return round(promedio, 1) if promedio else None
    
    def total_puntuaciones_recibidas(self):
        """
        Cuenta el total de puntuaciones que han recibido todos los apuntes del usuario.
        """
        from gestion_apuntes.models import Puntuacion
        
        return Puntuacion.objects.filter(apunte__usuario=self).count()
    
    def nivel_reputacion(self):
        """
        Retorna un nivel de reputación basado en el promedio de puntuaciones.
        """
        promedio = self.puntuacion_promedio()
        
        if promedio is None:
            return "Nuevo"
        elif promedio >= 4.5:
            return "Experto"
        elif promedio >= 4.0:
            return "Avanzado"
        elif promedio >= 3.0:
            return "Intermedio"
        else:
            return "Principiante"

@receiver(post_save, sender=User)
def crear_usuario(sender, instance, created, **kwargs):
    if created:
        Usuario.objects.create(user=instance)

@receiver(post_save, sender=User)
def guardar_usuario(sender, instance, **kwargs):
    # Solo intentamos guardar si el usuario ya tiene un perfil asociado
    if hasattr(instance, 'usuario'):
        instance.usuario.save()