from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from gestion_carreras.models import Carrera
from gestion_materias.models import Materia
from gestion_apuntes.models import Apunte
from django.core.files.uploadedfile import SimpleUploadedFile

class BusquedaMateriasTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        
        # Estructura básica
        self.carrera = Carrera.objects.create(nombre="Tecnicatura en Programación")
        self.materia = Materia.objects.create(nombre="Programación 2", anio=1)
        self.materia.carreras.add(self.carrera)
        
        # Archivo dummy
        file = SimpleUploadedFile("test.txt", b"content", content_type="text/plain")
        
        # Crear 2 apuntes con títulos diferentes
        self.apunte1 = Apunte.objects.create(
            titulo="Resumen de Python",
            descripcion="Todo sobre listas y diccionarios",
            archivo=file,
            materia=self.materia,
            usuario=self.user.usuario
        )
        
        self.apunte2 = Apunte.objects.create(
            titulo="Guía de Java",
            descripcion="Introducción a clases y objetos",
            archivo=file,
            materia=self.materia,
            usuario=self.user.usuario
        )

    def test_busqueda_encuentra_resultados(self):
        """Prueba que el buscador encuentre apuntes por título."""
        url = reverse('gestion_materias:materias_por_carrera', args=[self.carrera.id])
        
        # Simulamos búsqueda de "Python"
        response = self.client.get(url, {'materia_id': self.materia.id, 'q': 'Python'})
        
        self.assertEqual(response.status_code, 200)
        apuntes_en_contexto = response.context['apuntes']
        
        # Debe encontrar el apunte 1
        self.assertIn(self.apunte1, apuntes_en_contexto)
        # NO debe encontrar el apunte 2
        self.assertNotIn(self.apunte2, apuntes_en_contexto)

    def test_busqueda_sin_resultados(self):
        """Prueba que el buscador no devuelva nada si no hay coincidencia."""
        url = reverse('gestion_materias:materias_por_carrera', args=[self.carrera.id])
        
        # Buscamos algo que no existe
        response = self.client.get(url, {'materia_id': self.materia.id, 'q': 'Cobol'})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['apuntes']), 0)