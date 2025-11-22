# Documentación de Tests - Gestión Carreras

Este documento describe los casos de prueba implementados en el archivo `tests.py` para la aplicación **gestion_carreras**.

## Modelos (`CarreraModelTest`)

Validaciones de integridad de datos.

*   **`test_carrera_creation`**: Verifica la instanciación correcta de una Carrera.
*   **`test_carrera_validation_invalid_nombre`**: Comprueba que no se puedan crear carreras con caracteres inválidos en el nombre.
*   **`test_carrera_validation_invalid_universidad`**: Comprueba que no se puedan crear carreras con caracteres inválidos en el campo universidad.

## Vistas (`CarreraViewTest`)

*   **`test_lista_carreras_view`**: Verifica que la vista de listado:
    *   Devuelva un código 200 (OK).
    *   Use la plantilla correcta.
    *   Muestre en el HTML los nombres de las carreras creadas en la base de datos de prueba.
