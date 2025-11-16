## Sistema de Autenticación: Login

Este documento explica la implementación del sistema de inicio de sesión en el proyecto, el porqué de su diseño y cómo funciona el flujo de autenticación de un usuario.

### 1. ¿Por Qué se Refactorizó el Login?

Anteriormente, el formulario de login se encontraba en un menú desplegable dentro de la barra de navegación principal (`base.html`).

Aunque funcional, esta aproximación presentaba un problema de diseño: mezclaba la lógica de autenticación con la plantilla de la estructura base del sitio. La práctica profesional recomendada es la **Separación de Responsabilidades**, donde cada componente del sistema tiene una única y clara función.

**Solución:**
Se movió el sistema de login a una **página dedicada**, siguiendo las convenciones estándar de desarrollo web.

**Beneficios:**
*   **Código Limpio:** `base.html` ahora solo se ocupa de la maquetación, mientras que la nueva página de login se ocupa exclusivamente de la autenticación.
*   **Mantenibilidad:** Es mucho más fácil de gestionar, depurar y asegurar.
*   **Escalabilidad:** Sienta las bases para futuras funcionalidades como el registro de nuevos usuarios o la recuperación de contraseñas.

### 2. El Camino del Login: ¿Cómo Funciona?

Este es el flujo que sigue un usuario para iniciar sesión, explicado de manera sencilla:

**Paso 1: El Usuario hace clic en "Login"**
*   Desde cualquier lugar del sitio, el usuario pulsa el botón "Login" en la barra de navegación que se encuentra en `base.html`.
*   Ese botón es un enlace que lo dirige a la URL `/usuarios/login/`.

**Paso 2: La URL Llama a la Vista Correcta**
*   El sistema de URLs de Django, configurado en `apuntes/urls.py` y `gestion_usuarios/urls.py`, asocia la ruta `/usuarios/login/` con una función específica.
*   La función que se ejecuta es `login_view`, ubicada en el archivo `gestion_usuarios/views.py`.

**Paso 3: La Vista Prepara el Formulario**
*   La función `login_view` crea un formulario de autenticación (`AuthenticationForm`) que Django provee por seguridad.
*   Luego, renderiza (dibuja) la plantilla `gestion_usuarios/templates/gestion_usuarios/login.html`, mostrándole al usuario la página para ingresar sus credenciales.

**Paso 4: El Usuario Envía sus Datos**
*   El usuario rellena el formulario y hace clic en "Iniciar Sesión".
*   Los datos se envían de vuelta a la misma vista (`login_view`), pero esta vez como una petición `POST`.

**Paso 5: La Vista Valida y Autentica**
*   Al recibir los datos, `login_view` los valida.
*   Si el usuario y la contraseña son correctos, la vista utiliza la función `login()` de Django para crear la sesión del usuario.
*   Finalmente, redirige al usuario a la página de inicio o a la página que intentaba acceder.

### 3. Protección de Páginas

Algunas secciones del sitio, como la de "Apuntes", solo deben ser accesibles para usuarios autenticados.

*   Esto se logra añadiendo el decorador `@login_required` a las vistas que queremos proteger, como en `gestion_apuntes/views.py`.
*   Si un usuario no autenticado intenta acceder, Django lo redirige automáticamente a la página de login. Esto es posible gracias a la configuración `LOGIN_URL = 'gestion_usuarios:login'` en el archivo `settings.py`.
