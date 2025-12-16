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

    def test_invalid_file_extension(self):
        """Prueba que no se permitan extensiones peligrosas como .exe"""
        from django.core.exceptions import ValidationError
        
        file = SimpleUploadedFile("virus.exe", b"malware", content_type="application/x-msdownload")
        
        apunte = Apunte(
            titulo="Virus",
            descripcion="No descargar",
            archivo=file,
            materia=self.materia,
            usuario=self.user.usuario
        )
        
        # La validación ocurre al llamar a full_clean()
        with self.assertRaises(ValidationError):
            apunte.full_clean()

    def test_file_size_limit(self):
        """Prueba que no se permitan archivos mayores a 10MB"""
        from django.core.exceptions import ValidationError
        
        # Simulamos un archivo de 11MB
        # No creamos 11MB reales de datos para no llenar memoria, usamos un mock o un archivo sparse
        # Pero SimpleUploadedFile crea en memoria. Para el test simple, usaremos un truco:
        # Sobreescribir el atributo size del archivo envuelto antes de validar
        
        file = SimpleUploadedFile("large.pdf", b"dummy content", content_type="application/pdf")
        file.size = 11 * 1024 * 1024  # 11 MB
        
        apunte = Apunte(
            titulo="Archivo Grande",
            descripcion="Muy pesado",
            archivo=file,
            materia=self.materia,
            usuario=self.user.usuario
        )
        
        with self.assertRaisesRegex(ValidationError, "El archivo no puede superar 10MB"):
            apunte.full_clean()

    def test_file_cleanup_on_delete(self):
        """Prueba que el archivo físico se elimina al borrar el apunte"""
        import os
        
        file_content = b"content to be deleted"
        file = SimpleUploadedFile("delete_me.txt", file_content, content_type="text/plain")
        
        apunte = Apunte.objects.create(
            titulo="Apunte Borrar",
            descripcion="Para borrar",
            archivo=file,
            materia=self.materia,
            usuario=self.user.usuario
        )
        
        file_path = apunte.archivo.path
        self.assertTrue(os.path.exists(file_path))
        
        apunte.delete()
        
        self.assertFalse(os.path.exists(file_path))


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
        
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200) # Redirect followed
        self.assertTrue(Apunte.objects.filter(titulo='Nuevo Apunte').exists())
        
        # Verify success message
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), '¡Apunte subido exitosamente!')

    def test_subir_apunte_invalid_data(self):
        self.client.login(username='author', password='password')
        url = reverse('gestion_apuntes:subir_apunte', args=[self.materia.id])
        
        # Intento de subir sin archivo ni título
        data = {
            'titulo': '',
            'descripcion': 'Desc',
             # Sin archivo
        }
        
        response = self.client.post(url, data, follow=True)
        
        # Debería renderizar la misma página (código 200) pero sin redirigir (si no es follow=True, sería 200 directo)
        # Con follow=True, si hay error, se queda en la página (200) y muestra errores
        self.assertEqual(response.status_code, 200)
        
        # Verificar que NO se creó el apunte
        self.assertFalse(Apunte.objects.filter(descripcion='Desc').exists())
        
        # Verificar mensaje de error global
        messages = list(response.context['messages'])
        self.assertTrue(any("Hubo un error" in str(m) for m in messages))
        
        # Verificar errores de campo en el formulario
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('titulo', form.errors)
        self.assertIn('archivo', form.errors)

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
        
        response = self.client.get(url, follow=True) # Eliminacion via GET/redirect
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Apunte.objects.filter(id=self.apunte.id).exists()) # Should still exist
        
        # Verify error message
        messages = list(response.context['messages'])
        self.assertTrue(any("No tenés permisos" in str(m) for m in messages))

        # Author deletes
        self.client.login(username='author', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Apunte.objects.filter(id=self.apunte.id).exists()) # Should be gone