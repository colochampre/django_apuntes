## Sistema de Autenticación: Registro de Usuarios

Este documento explica cómo funciona el flujo de registro de nuevos usuarios en la plataforma.

### 1. ¿Por Qué Usar `UserCreationForm` de Django?

Para el registro de usuarios, en lugar de crear un formulario desde cero, utilizamos `UserCreationForm`, una herramienta que Django provee.

**Motivo (Práctica Profesional):**
La seguridad es crítica en el registro. `UserCreationForm` se encarga automáticamente de las tareas más importantes y complejas:
*   **Validación de Contraseñas:** Comprueba que las contraseñas ingresadas por el usuario coincidan.
*   **Seguridad de Contraseñas:** Se asegura de que la contraseña no sea demasiado simple.
*   **Encriptación:** **Nunca** guarda la contraseña como texto plano. La encripta (usando un "hash") antes de guardarla en la base de datos, haciendo que sea ilegible.
*   **Nombres de Usuario Únicos:** Verifica que el nombre de usuario elegido no esté ya en uso.

Usar esta herramienta nos garantiza un proceso de registro robusto y seguro sin tener que reinventar la rueda.

### 2. El Camino del Registro: ¿Cómo Funciona?

Este es el flujo que sigue un estudiante para crear una nueva cuenta:

**Paso 1: El Usuario va a la Página de Registro**
*   Desde la página de "Login", el usuario hace clic en el enlace "¿No tenés cuenta? **Registrate**".
*   Este enlace lo dirige a la URL `/usuarios/registro/`.

**Paso 2: La URL Llama a la Vista Correcta**
*   El sistema de URLs de Django (en `gestion_usuarios/urls.py`) asocia la ruta `/usuarios/registro/` con la función `register_view`.
*   Esta función se encuentra en el archivo `gestion_usuarios/views.py`.

**Paso 3: La Vista Prepara el Formulario de Registro**
*   La función `register_view` crea una instancia del formulario `UserCreationForm`.
*   Luego, renderiza la plantilla `gestion_usuarios/templates/gestion_usuarios/register.html`, mostrándole al usuario los campos necesarios para crear su cuenta (usuario, contraseña y confirmación de contraseña).

**Paso 4: El Usuario Envía sus Datos**
*   El usuario completa el formulario y hace clic en "Registrarse".
*   Los datos se envían de vuelta a la misma vista (`register_view`) mediante una petición `POST`.

**Paso 5: La Vista Valida, Guarda y Autentica al Nuevo Usuario**
*   Al recibir los datos, `register_view` usa `UserCreationForm` para validarlos.
*   Si los datos son correctos (el usuario no existe, las contraseñas coinciden, etc.), el formulario **crea el nuevo usuario** en la base de datos con la contraseña ya encriptada.
*   Inmediatamente después, la vista utiliza la función `login()` de Django para **iniciar la sesión del nuevo usuario automáticamente**.
*   Finalmente, redirige al usuario a la página de inicio (`home`) con un mensaje de bienvenida.
