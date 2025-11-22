from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from .models import Materia
from gestion_carreras.models import Carrera


class MateriaModelTest(TestCase):
    """
    Pruebas para el modelo Materia.
    Incluye verificaciones de creación y validaciones personalizadas.
    """
    def test_materia_creation(self):
        """
        Verifica la creación correcta de una materia y su representación en cadena.
        """
        materia = Materia.objects.create(nombre="Matemática", anio=2023)
        self.assertEqual(materia.nombre, "Matemática")
        self.assertEqual(materia.anio, 2023)
        self.assertEqual(str(materia), "Matemática - 2023")

    def test_materia_validation_invalid_nombre(self):
        """
        Prueba de validación: Verifica que se rechacen nombres con caracteres no permitidos.
        """
        materia = Materia(nombre="Inv@lid", anio=2023)
        with self.assertRaises(ValidationError):
            materia.clean()

    def test_materia_validation_invalid_anio(self):
        """
        Prueba de validación: Verifica que se rechacen años con formato incorrecto.
        """
        materia = Materia(nombre="Matemática", anio=123)  # Longitud inválida
        with self.assertRaises(ValidationError):
            materia.clean()


class MateriaViewTest(TestCase):
    """
    Pruebas para las vistas de la aplicación gestion_materias.
    """
    def setUp(self):
        """Configuración inicial para las pruebas de vistas."""
        self.client = Client()
        self.carrera = Carrera.objects.create(nombre="Ingeniería", universidad="UTN")
        self.materia = Materia.objects.create(nombre="Matemática", anio=2023)
        self.carrera.materias.add(self.materia)

    def test_listar_materias_por_carrera_view(self):
        """
        Verifica que se listen correctamente las materias de una carrera específica.
        """
        url = reverse(
            "gestion_materias:materias_por_carrera",
            kwargs={"carrera_id": self.carrera.id},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "gestion_materias/lista_materias.html")
        self.assertContains(response, "Matemática")

    def test_listar_materias_por_carrera_with_materia_selected(self):
        """
        Verifica que al seleccionar una materia, esta se pase correctamente en el contexto.
        """
        url = reverse(
            "gestion_materias:materias_por_carrera",
            kwargs={"carrera_id": self.carrera.id},
        )
        response = self.client.get(f"{url}?materia_id={self.materia.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["materia_seleccionada"], self.materia)

    def test_listar_materias_invalid_carrera_404(self):
        """
        Prueba de manejo de errores: Verifica que acceder a una carrera inexistente devuelva 404.
        """
        url = reverse(
            "gestion_materias:materias_por_carrera",
            kwargs={"carrera_id": 99999},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)