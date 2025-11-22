# Documentación de Tests - Gestión Apuntes

Este documento describe los casos de prueba implementados en el archivo `tests.py` para la aplicación **gestion_apuntes**.

## Modelos (`ApunteModelTest`)

Verifican la integridad de los datos a nivel de base de datos.

*   **`test_apunte_creation`**: Comprueba que se puede crear un objeto `Apunte` correctamente relacionándolo con un `Usuario` y una `Materia`. Valida también la representación en cadena (`__str__`) del modelo.

## Vistas (`ApunteViewTest`)

Simulan peticiones HTTP para verificar el comportamiento de las rutas y controladores.

*   **`test_apuntes_view`**: Verifica que la página principal de apuntes carga correctamente (código 200) y usa la plantilla adecuada.
*   **`test_subir_apunte_view_login_required`**: Asegura que un usuario anónimo no pueda acceder a la vista de subir apuntes y sea redirigido al login.
*   **`test_subir_apunte_view_get_authenticated`**: Verifica que un usuario autenticado pueda acceder al formulario de subida.
*   **`test_subir_apunte_view_post_valid`**: Simula la subida exitosa de un archivo. Verifica:
    *   Redirección tras el éxito (código 302).
    *   Creación del objeto en la base de datos.
    *   Asociación correcta del apunte al usuario logueado.
*   **`test_buscar_apunte`**: Prueba la funcionalidad de búsqueda. Crea apuntes con diferentes títulos y verifica que al enviar una query ("q"), la respuesta contenga solo los resultados relevantes y excluya los irrelevantes.
*   **`test_descargar_apunte_view`**: Comprueba que la ruta de descarga sirve el archivo correctamente, validando el header `Content-Disposition` (fuerza la descarga).
