from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from .models import Apunte, Puntuacion
from gestion_materias.models import Materia
from gestion_carreras.models import Carrera
from gestion_usuarios.models import Usuario

class ApunteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        # Usuario profile should be created by signal
        self.carrera = Carrera.objects.create(nombre="Tecnicatura en Programación")
        self.materia = Materia.objects.create(nombre="Matemática", anio=1)
        self.materia.carreras.add(self.carrera)
        
    def test_apunte_creation(self):
        file = SimpleUploadedFile("test_file.txt", b"content", content_type="text/plain")
        apunte = Apunte.objects.create(
            titulo="Apunte Test",
            descripcion="Descripción Test",
            archivo=file,
            materia=self.materia,
            usuario=self.user.usuario
        )
        self.assertEqual(apunte.titulo, "Apunte Test")
        self.assertEqual(apunte.extension, "TXT")
        self.assertEqual(apunte.get_file_type(), "text")
        self.assertEqual(str(apunte).split(" - ")[0], "Apunte Test")

    def test_puntuacion_logic(self):
        file = SimpleUploadedFile("test_file.txt", b"content", content_type="text/plain")
        apunte = Apunte.objects.create(
            titulo="Apunte Puntuacion",
            descripcion="Desc",
            archivo=file,
            materia=self.materia,
            usuario=self.user.usuario
        )
        
        user2 = User.objects.create_user(username='voter', password='password')
        
        Puntuacion.objects.create(apunte=apunte, usuario=user2.usuario, valor=5)
        
        self.assertEqual(apunte.promedio_puntuacion(), 5.0)
        self.assertEqual(apunte.total_puntuaciones(), 1)
        self.assertEqual(apunte.puntuacion_usuario(user2.usuario), 5)

class ApunteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='author', password='password')
        self.user_voter = User.objects.create_user(username='voter', password='password')
        self.carrera = Carrera.objects.create(nombre="Tecnicatura")
        self.materia = Materia.objects.create(nombre="Programación 1", anio=1)
        self.materia.carreras.add(self.carrera)
        
        self.file = SimpleUploadedFile("test.pdf", b"pdf_content", content_type="application/pdf")
        self.apunte = Apunte.objects.create(
            titulo="Apunte View",
            descripcion="Desc View",
            archivo=self.file,
            materia=self.materia,
            usuario=self.user.usuario
        )

    def test_subir_apunte_view(self):
        self.client.login(username='author', password='password')
        url = reverse('gestion_apuntes:subir_apunte', args=[self.materia.id])
        
        new_file = SimpleUploadedFile("new.pdf", b"content", content_type="application/pdf")
        data = {
            'titulo': 'Nuevo Apunte',
            'descripcion': 'Nueva Desc',
            'archivo': new_file,
            'carrera_id': self.carrera.id
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302) # Redirect
        self.assertTrue(Apunte.objects.filter(titulo='Nuevo Apunte').exists())

    def test_puntuar_apunte_view(self):
        self.client.login(username='voter', password='password')
        url = reverse('gestion_apuntes:puntuar_apunte', args=[self.apunte.id])
        
        response = self.client.post(url, {'valor': 4})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['promedio'], 4.0)
        
        # Test updating score
        response = self.client.post(url, {'valor': 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['promedio'], 2.0)

    def test_eliminar_apunte_view_permission(self):
        # User voter tries to delete author's apunte
        self.client.login(username='voter', password='password')
        url = reverse('gestion_apuntes:eliminar_apunte', args=[self.apunte.id])
        
        response = self.client.get(url) # Eliminacion via GET/redirect usually, logic check
        # The view logic redirects to 'gestion_apuntes:apuntes' with error message on failure
        # Or redirects to 'materias_por_carrera' on success.
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Apunte.objects.filter(id=self.apunte.id).exists()) # Should still exist

        # Author deletes
        self.client.login(username='author', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Apunte.objects.filter(id=self.apunte.id).exists()) # Should be gone