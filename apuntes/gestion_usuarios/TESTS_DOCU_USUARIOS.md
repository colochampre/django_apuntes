# Documentación de Tests - Gestión Usuarios

Este documento describe los casos de prueba implementados en el archivo `tests.py` para la aplicación **gestion_usuarios**.

## Modelos (`UsuarioModelTest`)

*   **`test_usuario_creation`**: Verifica la creación del perfil extendido `Usuario` vinculado al modelo estándar `User` de Django y su relación ManyToMany con `Carrera`.

## Vistas (`UsuarioViewTest`)

Pruebas de flujo de autenticación y registro.

*   **`test_registro_view_get`**: Verifica que la página de registro carga correctamente.
*   **`test_registro_view_post_valid`**: Simula un registro exitoso con todos los datos válidos. Verifica que el usuario se crea en la base de datos y se redirige.
*   **`test_registro_view_post_password_mismatch`**: **Caso de Validación**. Envía un formulario donde las contraseñas no coinciden y verifica que:
    *   No se crea el usuario.
    *   Se devuelve la misma página (código 200).
    *   El formulario contiene errores específicos en el campo de contraseña.
*   **`test_registro_view_post_duplicate_user`**: **Caso de Validación**. Intenta registrar un nombre de usuario que ya existe y verifica que el sistema devuelve un error de formulario apropiado.
*   **`test_perfil_view_login_required`**: Protege la vista de perfil contra accesos anónimos.
*   **`test_perfil_view_get_authenticated`**: Permite el acceso al perfil a usuarios logueados.
*   **`test_custom_logout`**: Verifica que la vista de cierre de sesión redirige al usuario a la home (código 302).
