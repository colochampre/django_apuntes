# Documentación de Tests - Gestión Materias

Este documento describe los casos de prueba implementados en el archivo `tests.py` para la aplicación **gestion_materias**.

## Modelos (`MateriaModelTest`)

Incluye validaciones personalizadas de lógica de negocio.

*   **`test_materia_creation`**: Crea una materia básica y verifica sus atributos.
*   **`test_materia_validation_invalid_nombre`**: Verifica que el validador `es_nombre_valido` rechace nombres con caracteres especiales no permitidos (lanza `ValidationError`).
*   **`test_materia_validation_invalid_anio`**: Verifica que el validador `es_anio_valido` rechace años que no tengan 4 dígitos.

## Vistas (`MateriaViewTest`)

*   **`test_listar_materias_por_carrera_view`**: Verifica que se listen las materias correspondientes a una carrera específica.
*   **`test_listar_materias_por_carrera_with_materia_selected`**: Prueba la funcionalidad de "selección activa" (cuando se pasa un `materia_id` en la URL), asegurando que el contexto de la plantilla reciba el objeto seleccionado.
*   **`test_listar_materias_invalid_carrera_404`**: **Manejo de Errores**. Verifica que al intentar acceder a las materias de una carrera con un ID inexistente (ej. 99999), el servidor responda correctamente con un error 404 (Not Found) en lugar de un error 500.
