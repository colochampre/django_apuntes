from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from .models import Carrera


class CarreraModelTest(TestCase):
    """
    Pruebas para el modelo Carrera.
    Verifica la creación y validación de datos de Carreras.
    """
    def test_carrera_creation(self):
        """
        Verifica que se pueda crear una carrera y que su método __str__ sea correcto.
        """
        carrera = Carrera.objects.create(nombre="Ingeniería", universidad="UTN")
        self.assertEqual(carrera.nombre, "Ingeniería")
        self.assertEqual(carrera.universidad, "UTN")
        self.assertEqual(str(carrera), "Ingeniería - UTN")

    def test_carrera_validation_invalid_nombre(self):
        """
        Prueba de validación: El nombre no debe contener caracteres especiales no permitidos.
        """
        carrera = Carrera(nombre="Inv@lid", universidad="UTN")
        with self.assertRaises(ValidationError):
            carrera.clean()

    def test_carrera_validation_invalid_universidad(self):
        """
        Prueba de validación: La universidad no debe contener caracteres especiales no permitidos.
        """
        carrera = Carrera(nombre="Ingeniería", universidad="Inv@lid")
        with self.assertRaises(ValidationError):
            carrera.clean()


class CarreraViewTest(TestCase):
    """
    Pruebas para las vistas de la aplicación gestion_carreras.
    """
    def setUp(self):
        """Configuración inicial con datos de prueba."""
        self.client = Client()
        self.carrera1 = Carrera.objects.create(nombre="A Carrera", universidad="UTN")
        self.carrera2 = Carrera.objects.create(nombre="B Carrera", universidad="UBA")

    def test_lista_carreras_view(self):
        """
        Verifica que la vista de lista de carreras devuelva 200 y muestre las carreras creadas.
        """
        response = self.client.get(reverse("gestion_carreras:lista_carreras"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "gestion_carreras/lista_carreras.html")
        self.assertContains(response, "A Carrera")
        self.assertContains(response, "B Carrera")