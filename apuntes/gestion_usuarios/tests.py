from django.test import TestCase
from django.contrib.auth.models import User
from .models import Usuario
from gestion_apuntes.models import Apunte, Puntuacion
from gestion_materias.models import Materia
from gestion_carreras.models import Carrera
from django.core.files.uploadedfile import SimpleUploadedFile

class UsuarioSignalTest(TestCase):
    """
    Pruebas para las señales (signals) del modelo Usuario.
    Verifica que se cree y actualice automáticamente el perfil de usuario.
    """
    def test_usuario_created_signal(self):
        """Prueba que al crear un User se crea automáticamente su perfil Usuario asociado."""
        user = User.objects.create_user(username='newuser', password='password')
        self.assertTrue(hasattr(user, 'usuario'))
        self.assertIsInstance(user.usuario, Usuario)

    def test_usuario_save_signal(self):
        """Prueba que al guardar el User se dispara la señal de guardado del perfil"""
        user = User.objects.create_user(username='saveuser', password='password')
        
        # Modificamos algo en el usuario para disparar el save
        user.first_name = "Pedro"
        user.save()
        
        # Verificamos que el perfil sigue accesible y consistente
        self.assertEqual(user.usuario.user.first_name, "Pedro")


class UsuarioReputationTest(TestCase):
    """
    Pruebas para la lógica de reputación del usuario.
    Verifica que el cálculo de niveles de reputación (Nuevo, Principiante, etc.) sea correcto
    basado en el promedio de puntuaciones recibidas.
    """
    def setUp(self):
        """Configura el entorno de prueba con usuario, apuntes y votantes."""
        self.user = User.objects.create_user(username='expert', password='password')
        self.carrera = Carrera.objects.create(nombre="Tecnicatura")
        self.materia = Materia.objects.create(nombre="Algo", anio=1)
        self.materia.carreras.add(self.carrera)
        
        file = SimpleUploadedFile("test.txt", b"content")
        self.apunte = Apunte.objects.create(
            titulo="Apunte Rep", descripcion="D", archivo=file,
            materia=self.materia, usuario=self.user.usuario
        )
        
        self.voter1 = User.objects.create_user(username='v1', password='p')
        self.voter2 = User.objects.create_user(username='v2', password='p')

    def test_reputation_levels(self):
        """
        Prueba que el nivel de reputación cambie correctamente según el promedio de puntuaciones.
        Verifica transiciones de Nuevo a Experto e Intermedio.
        """
        # Nuevo (sin votos)
        self.assertEqual(self.user.usuario.nivel_reputacion(), "Nuevo")
        
        # 5 estrellas -> Experto
        Puntuacion.objects.create(apunte=self.apunte, usuario=self.voter1.usuario, valor=5)
        self.assertEqual(self.user.usuario.nivel_reputacion(), "Experto")
        
        # (5+1)/2 = 3 -> Intermedio
        Puntuacion.objects.create(apunte=self.apunte, usuario=self.voter2.usuario, valor=1)
        self.assertEqual(self.user.usuario.nivel_reputacion(), "Intermedio")