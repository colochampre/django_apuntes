from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from .models import Apunte
from gestion_materias.models import Materia
from gestion_usuarios.models import Usuario


class ApunteModelTest(TestCase):
    """
    Conjunto de pruebas para el modelo Apunte.
    Verifica la integridad de los datos y las relaciones al crear objetos Apunte.
    """

    def setUp(self):
        """
        Configuración inicial para las pruebas.
        Crea un usuario, un perfil de usuario y una materia base para relacionar con los apuntes.
        """
        self.user = User.objects.create_user(username="testuser", password="password")
        self.usuario = Usuario.objects.create(user=self.user)
        self.materia = Materia.objects.create(nombre="Matemática", anio=2023)

    def test_apunte_creation(self):
        """
        Prueba la creación exitosa de un objeto Apunte.
        Verifica que los campos se guarden correctamente y que las relaciones (usuario, materia)
        se establezcan como se espera.
        """
        file = SimpleUploadedFile("file.txt", b"file_content")
        apunte = Apunte.objects.create(
            titulo="Apunte 1",
            descripcion="Desc",
            archivo=file,
            materia=self.materia,
            usuario=self.usuario,
        )
        self.assertEqual(apunte.titulo, "Apunte 1")
        self.assertEqual(apunte.materia, self.materia)
        self.assertEqual(apunte.usuario, self.usuario)
        
        # Verifica que la representación en cadena (__str__) contenga el título y el usuario
        self.assertIn("Apunte 1", str(apunte))
        self.assertIn("testuser", str(apunte))


class ApunteViewTest(TestCase):
    """
    Conjunto de pruebas para las vistas de la aplicación gestion_apuntes.
    Simula peticiones HTTP para verificar el comportamiento de las rutas, plantillas y lógica de negocio.
    """

    def setUp(self):
        """
        Configuración inicial del entorno de pruebas.
        Inicializa el cliente HTTP, crea usuarios y datos de prueba necesarios (Materia, Apunte).
        """
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.usuario = Usuario.objects.create(user=self.user)
        self.materia = Materia.objects.create(nombre="Matemática", anio=2023)
        self.file = SimpleUploadedFile("file.txt", b"file_content")
        self.apunte = Apunte.objects.create(
            titulo="Apunte 1",
            descripcion="Desc",
            archivo=self.file,
            materia=self.materia,
            usuario=self.usuario,
        )

    def test_apuntes_view(self):
        """
        Verifica que la vista principal de apuntes sea accesible.
        Debe devolver un código de estado 200 y usar la plantilla correcta.
        """
        response = self.client.get(reverse("gestion_apuntes:apuntes"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "gestion_apuntes/apuntes.html")

    def test_subir_apunte_view_login_required(self):
        """
        Verifica la seguridad de la vista de subir apuntes.
        Un usuario no autenticado no debería poder acceder y debería ser redirigido.
        """
        self.client.logout()
        response = self.client.get(reverse("gestion_apuntes:subir_apunte"))
        self.assertNotEqual(response.status_code, 200)

    def test_subir_apunte_view_get_authenticated(self):
        """
        Verifica que un usuario autenticado pueda acceder al formulario de subida de apuntes.
        """
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("gestion_apuntes:subir_apunte"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "gestion_apuntes/subir_apunte.html")

    def test_subir_apunte_view_post_valid(self):
        """
        Prueba el flujo completo de subida de un archivo válido mediante POST.
        Verifica que:
        1. Se redirija al usuario tras una subida exitosa (código 301/302).
        2. El objeto Apunte se cree en la base de datos.
        3. El apunte esté correctamente asociado al usuario que lo subió.
        """
        self.client.login(username="testuser", password="password")

        file_content = b"Contenido de prueba del apunte."
        uploaded_file = SimpleUploadedFile(
            "nuevo_apunte.pdf", file_content, content_type="application/pdf"
        )

        data = {
            "titulo": "Nuevo Apunte de Prueba",
            "descripcion": "Una descripcion valida",
            "materia": self.materia.id,
            "archivo": uploaded_file,
        }

        response = self.client.post(reverse("gestion_apuntes:subir_apunte"), data)

        # Espera una redirección tras el éxito
        self.assertIn(response.status_code, [301, 302])

        # Verifica que el objeto existe en la BD
        self.assertTrue(Apunte.objects.filter(titulo="Nuevo Apunte de Prueba").exists())
        apunte = Apunte.objects.get(titulo="Nuevo Apunte de Prueba")
        self.assertEqual(apunte.usuario, self.usuario)

    def test_buscar_apunte(self):
        """
        Prueba la funcionalidad de búsqueda.
        Verifica que al buscar por un término específico, solo se devuelvan los apuntes coincidentes.
        """
        # Crea un segundo apunte para verificar que el filtrado funciona correctamente
        materia2 = Materia.objects.create(nombre="Fisica", anio=2023)
        Apunte.objects.create(
            titulo="Guia de Ejercicios Fisica",
            descripcion="Ejercicios",
            archivo=SimpleUploadedFile("fisica.pdf", b"fisica"),
            materia=materia2,
            usuario=self.usuario,
        )

        response = self.client.get(
            reverse("gestion_apuntes:buscar_apunte"), {"q": "Fisica"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Guia de Ejercicios Fisica")
        self.assertNotContains(response, "Apunte 1")  # El apunte creado en setUp no debería aparecer

    def test_descargar_apunte_view(self):
        """
        Verifica que la vista de descarga sirva el archivo correctamente.
        Comprueba que la respuesta tenga el encabezado 'Content-Disposition' para forzar la descarga.
        """
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse(
                "gestion_apuntes:descargar_apunte", kwargs={"apunte_id": self.apunte.id}
            )
        )
        self.assertEqual(response.status_code, 200)
        # Verifica que sea una respuesta de archivo adjunto
        self.assertTrue(response.has_header("Content-Disposition"))