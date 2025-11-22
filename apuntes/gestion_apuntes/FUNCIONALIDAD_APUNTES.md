# Implementación de Apuntes por Materia y Funcionalidad de Subida

Este documento detalla el proceso técnico para implementar dos funcionalidades clave en el proyecto: la capacidad de ver los apuntes asociados a una materia específica y el mecanismo para que los usuarios puedan subir nuevos apuntes.

---

## Parte 1: Visualización de Apuntes por Materia

El objetivo era que, al hacer clic en una materia dentro de la página de una carrera, el usuario sea redirigido a una nueva página que liste todos los apuntes de esa materia.

### Paso 1: Creación de la Ruta (URL)

Para que cada página de apuntes de una materia tenga una dirección única, se definió un nuevo patrón de URL.

**Archivo:** `apuntes/gestion_materias/urls.py`

```python
path('<int:materia_id>/apuntes/', views.apuntes_por_materia, name='apuntes_por_materia'),
```

**Explicación:**
-   `'<int:materia_id>/apuntes/'`: Este patrón define la estructura de la URL. Django captura la parte numérica de la URL y la pasa a la vista como una variable llamada `materia_id`.
-   `views.apuntes_por_materia`: Especifica que esta URL será manejada por la función `apuntes_por_materia` en el archivo `views.py`.
-   `name='apuntes_por_materia'`: Es un nombre único para esta ruta, que nos permite referenciarla fácilmente desde las plantillas sin tener que escribir la URL completa.

### Paso 2: Creación de la Vista (View)

La vista contiene la lógica para obtener los datos correctos de la base de datos y enviarlos a la plantilla.

**Archivo:** `apuntes/gestion_materias/views.py`

```python
def apuntes_por_materia(request, materia_id):
    materia = get_object_or_404(Materia, id=materia_id)
    apuntes = Apunte.objects.filter(materia=materia).order_by("-fecha_publicacion")
    context = {"materia": materia, "apuntes": apuntes}
    return render(request, "gestion_materias/apuntes_por_materia.html", context)
```

**Explicación:**
1.  La función recibe el `request` y el `materia_id` capturado de la URL.
2.  `materia = get_object_or_404(Materia, id=materia_id)`: Busca en la base de datos un objeto `Materia` cuyo `id` coincida con el de la URL. Si no lo encuentra, muestra una página de error 404 (Not Found).
3.  `apuntes = Apunte.objects.filter(materia=materia)`: Realiza una consulta a la base de datos para obtener todos los objetos `Apunte` que estén relacionados (a través de su `ForeignKey`) con la `materia` encontrada en el paso anterior. Se ordenan por fecha de publicación descendente.
4.  `render(...)`: Carga la plantilla `apuntes_por_materia.html`, le pasa los objetos `materia` y `apuntes` dentro de un diccionario de contexto, y la devuelve al navegador del usuario.

### Paso 3: Conexión desde la Lista de Materias

Finalmente, se modificó la plantilla que lista las materias de una carrera para que cada una enlace a su nueva página de apuntes.

**Archivo:** `apuntes/templates/gestion_materias/lista_materias.html`

```html
<a href="{% url 'gestion_materias:apuntes_por_materia' materia.id %}">
    {{ materia.nombre }}
</a>
```

**Explicación:**
-   `{% url 'gestion_materias:apuntes_por_materia' materia.id %}`: Esta es una etiqueta de plantilla de Django que genera una URL dinámicamente.
    -   `'gestion_materias:apuntes_por_materia'`: Le dice a Django que use la ruta con el nombre `apuntes_por_materia` que definimos en el `urls.py` de la app `gestion_materias`.
    -   `materia.id`: Le pasa el ID de la materia actual (en el bucle `for`) para construir la URL final (ej: `/materias/5/apuntes/`).

---

## Parte 2: Funcionalidad "Subir Apunte"

Se implementó un flujo completo para permitir a los usuarios subir nuevos apuntes, incluyendo un formulario, la lógica de procesamiento y la plantilla correspondiente.

### Paso 1: Creación del Formulario (Form)

Para simplificar la creación y validación de formularios, se utilizó la clase `ModelForm` de Django.

**Archivo:** `apuntes/gestion_apuntes/forms.py`

```python
from django import forms
from .models import Apunte

class ApunteForm(forms.ModelForm):
    class Meta:
        model = Apunte
        fields = ['titulo', 'descripcion', 'archivo', 'materia']
```

**Explicación:**
-   `ModelForm` crea un formulario automáticamente a partir de un modelo de Django.
-   `class Meta`: Es una clase interna que configura el formulario.
    -   `model = Apunte`: Lo vincula con el modelo `Apunte`.
    -   `fields = [...]`: Especifica qué campos del modelo se mostrarán en el formulario. `usuario` y `fecha_publicacion` se omiten porque se gestionan automáticamente en la vista.

### Paso 2: Implementación de la Lógica (URL y Vista)

Se creó una nueva URL (`/apuntes/subir/`) y una vista para manejar la subida de archivos.

**Archivo:** `apuntes/gestion_apuntes/views.py`

```python
def subir_apunte(request):
    if request.method == 'POST':
        form = ApunteForm(request.POST, request.FILES)
        if form.is_valid():
            apunte = form.save(commit=False)
            apunte.usuario = Usuario.objects.get(user=request.user)
            apunte.save()
            return redirect('gestion_materias:apuntes_por_materia', materia_id=apunte.materia.id)
    else:
        form = ApunteForm()
    
    context = {'form': form}
    return render(request, 'gestion_apuntes/subir_apunte.html', context)
```

**Explicación:**
-   La vista diferencia dos casos:
    1.  **Método GET (primer acceso a la página):** Se crea un formulario vacío (`form = ApunteForm()`) y se muestra la plantilla.
    2.  **Método POST (envío del formulario):**
        -   `form = ApunteForm(request.POST, request.FILES)`: Se crea el formulario con los datos enviados por el usuario. `request.FILES` es crucial para manejar los archivos subidos.
        -   `form.is_valid()`: Django ejecuta todas las validaciones definidas en el modelo y el formulario.
        -   `form.save(commit=False)`: Crea una instancia del objeto `Apunte` pero no la guarda aún en la base de datos, permitiéndonos añadir datos adicionales.
        -   `apunte.usuario = ...`: Se asigna el usuario actualmente autenticado (`request.user`) al apunte.
        -   `apunte.save()`: Ahora sí, se guarda el objeto completo en la base de datos.
        -   `redirect(...)`: Se redirige al usuario a la página de apuntes de la materia recién actualizada.

### Paso 3: Integración del Botón

Finalmente, se añadió el botón "Subir Contenido" en la plantilla de apuntes por materia para dar acceso a la nueva funcionalidad.

**Archivo:** `apuntes/templates/gestion_materias/apuntes_por_materia.html`

```html
<a href="{% url 'gestion_apuntes:subir_apunte' %}" class="btn btn-primary">
    Subir Contenido
</a>
```
**Explicación:**
-   Este enlace utiliza la etiqueta `{% url %}` para apuntar a la nueva vista `subir_apunte`, iniciando así el flujo de subida de un nuevo apunte.
-   El estilo del botón se gestionó con clases de Bootstrap para una correcta visualización junto al título de la página.
