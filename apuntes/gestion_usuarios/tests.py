from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Usuario
from gestion_carreras.models import Carrera


class UsuarioModelTest(TestCase):
    """
    Pruebas para el modelo Usuario.
    Verifica la creación del perfil de usuario.
    """

    def setUp(self):
        """Configuración inicial para las pruebas del modelo."""
        self.user = User.objects.create_user(username="testuser", password="password")
        self.carrera = Carrera.objects.create(
            nombre="Ingeniería en Sistemas", universidad="UTN"
        )

    def test_usuario_creation(self):
        """
        Verifica que se cree un objeto Usuario vinculado correctamente a un User de Django
        y que se puedan asignar carreras.
        """
        usuario = Usuario.objects.create(user=self.user)
        usuario.carrera.add(self.carrera)
        self.assertEqual(usuario.user.username, "testuser")
        self.assertIn(self.carrera, usuario.carrera.all())
        self.assertEqual(str(usuario), "testuser")


class UsuarioViewTest(TestCase):
    """
    Pruebas para las vistas de gestión de usuarios (registro, perfil, login/logout).
    """

    def setUp(self):
        """Configuración inicial para las pruebas de vistas."""
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.usuario = Usuario.objects.create(user=self.user)

    def test_registro_view_get(self):
        """
        Verifica que la vista de registro (GET) cargue correctamente.
        """
        response = self.client.get(reverse("gestion_usuarios:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "gestion_usuarios/register.html")

    def test_registro_view_post_valid(self):
        """
        Verifica un proceso de registro exitoso con datos válidos.
        Debe redirigir al home o login tras crear el usuario.
        """
        response = self.client.post(
            reverse("gestion_usuarios:register"),
            {
                "username": "newuser",
                "first_name": "New",
                "last_name": "User",
                "email": "new@example.com",
                "password1": "newpassword123",
                "password2": "newpassword123",
            },
        )
        # Debe redirigir tras el éxito (código 302)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_registro_view_post_password_mismatch(self):
        """
        Prueba de validación: Registro con contraseñas que no coinciden.
        No debe crear el usuario y debe mostrar un error en el formulario.
        """
        response = self.client.post(
            reverse("gestion_usuarios:register"),
            {
                "username": "mismatchuser",
                "first_name": "Bad",
                "last_name": "Pass",
                "email": "bad@example.com",
                "password1": "passwordA",
                "password2": "passwordB",
            },
        )
        self.assertEqual(response.status_code, 200)  # Debe permanecer en la página
        self.assertFalse(User.objects.filter(username="mismatchuser").exists())

        form = response.context["form"]
        self.assertTrue(form.errors)
        self.assertIn("password2", form.errors)
        # Verifica el contenido del error (usando coincidencia parcial para robustez)
        self.assertTrue(any("no coinciden" in e for e in form.errors["password2"]))

    def test_registro_view_post_duplicate_user(self):
        """
        Prueba de validación: Registro con un nombre de usuario existente.
        Debe rechazar el registro y mostrar un error.
        """
        User.objects.create_user(username="duplicate", password="password")
        response = self.client.post(
            reverse("gestion_usuarios:register"),
            {
                "username": "duplicate",
                "first_name": "Dup",
                "last_name": "User",
                "email": "dup@example.com",
                "password1": "password123",
                "password2": "password123",
            },
        )
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertTrue(form.errors)
        self.assertIn("username", form.errors)
        self.assertTrue(
            any(
                "Ya existe" in e or "already exists" in e
                for e in form.errors["username"]
            )
        )

    def test_perfil_view_login_required(self):
        """
        Verifica que la vista de perfil esté protegida y requiera autenticación.
        """
        self.client.logout()
        response = self.client.get(reverse("gestion_usuarios:perfil"))
        self.assertNotEqual(response.status_code, 200)  # Debe redirigir

    def test_perfil_view_get_authenticated(self):
        """
        Verifica que un usuario autenticado pueda ver su perfil.
        """
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("gestion_usuarios:perfil"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "gestion_usuarios/perfil.html")

    def test_custom_logout(self):
        """
        Verifica que la vista de logout cierre la sesión y redirija al inicio.
        """
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("gestion_usuarios:logout"))
        self.assertEqual(response.status_code, 302)  # Redirige al home
