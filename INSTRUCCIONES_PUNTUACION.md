# Sistema de Puntuación para Apuntes - Instrucciones

## Cambios Implementados

Se ha implementado un sistema completo de puntuación para los apuntes donde:
- Cada usuario puede dar una calificación de 1 a 5 estrellas a cada apunte
- Se muestra el promedio de todas las puntuaciones en la tarjeta del apunte
- Los usuarios pueden actualizar su puntuación en cualquier momento
- Solo se permite una puntuación por usuario por apunte

## Archivos Modificados

### 1. `gestion_apuntes/models.py`
- Se agregó el modelo `Puntuacion` para almacenar las calificaciones individuales
- Se agregaron métodos al modelo `Apunte`:
  - `promedio_puntuacion()`: Calcula el promedio de puntuaciones
  - `total_puntuaciones()`: Cuenta el total de valoraciones
  - `puntuacion_usuario(usuario)`: Obtiene la puntuación de un usuario específico

### 2. `gestion_apuntes/views.py`
- Se agregó la vista `puntuar_apunte()` que maneja las peticiones AJAX para puntuar

### 3. `gestion_apuntes/urls.py`
- Se agregó la URL `/apuntes/puntuar/<int:apunte_id>/`

### 4. `gestion_materias/views.py`
- Se modificó para pasar el `usuario_actual` al contexto del template

### 5. `templates/gestion_materias/lista_materias.html`
- Se agregó la visualización del promedio de puntuación con estrellas
- Se agregaron estrellas interactivas para que los usuarios puedan puntuar
- Se agregó JavaScript para manejar las interacciones con AJAX
- Se agregó CSS para estilizar las estrellas

## Pasos para Completar la Instalación

### 1. Crear las migraciones de base de datos

Abre una terminal en la carpeta del proyecto y ejecuta:

```bash
cd "c:\Users\Blue\Documents\UTN\semestre2\Programacion II\django_apuntes\apuntes"
python manage.py makemigrations gestion_apuntes
```

### 2. Aplicar las migraciones

```bash
python manage.py migrate
```

### 3. (Opcional) Registrar el modelo en el admin

Si deseas gestionar las puntuaciones desde el panel de administración, agrega esto a `gestion_apuntes/admin.py`:

```python
from .models import Puntuacion

@admin.register(Puntuacion)
class PuntuacionAdmin(admin.ModelAdmin):
    list_display = ['apunte', 'usuario', 'valor', 'fecha']
    list_filter = ['valor', 'fecha']
    search_fields = ['apunte__titulo', 'usuario__user__username']
```

## Cómo Funciona

1. **Visualización del Promedio**: En cada tarjeta de apunte se muestra:
   - Estrellas llenas (★) para la parte entera del promedio
   - Estrellas vacías (☆) para el resto
   - El promedio numérico y el total de valoraciones

2. **Puntuar un Apunte**: 
   - Los usuarios autenticados ven "Tu valoración:" con 5 estrellas
   - Al hacer clic en una estrella, se envía la puntuación al servidor
   - La interfaz se actualiza automáticamente sin recargar la página
   - Las estrellas seleccionadas se muestran en color dorado

3. **Actualizar Puntuación**:
   - Si un usuario ya puntuó, puede cambiar su calificación haciendo clic en otra estrella
   - Solo se permite una puntuación por usuario por apunte

## Características Técnicas

- **AJAX**: Las puntuaciones se envían sin recargar la página
- **Validación**: Solo valores de 1-5 son aceptados
- **Seguridad**: Requiere autenticación y token CSRF
- **Base de datos**: Restricción unique_together para evitar duplicados
- **UI/UX**: Efecto hover para mostrar la selección antes de confirmar

## Pruebas Recomendadas

1. Iniciar sesión con diferentes usuarios
2. Puntuar el mismo apunte con diferentes usuarios
3. Verificar que el promedio se actualiza correctamente
4. Intentar cambiar la puntuación y verificar que se actualiza
5. Verificar que usuarios no autenticados no ven las estrellas interactivas
