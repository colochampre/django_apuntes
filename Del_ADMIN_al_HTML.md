# De Django Admin a una Lista Interactiva: Mostrando Carreras y Materias

Este documento explica el proceso completo para gestionar datos en el panel de administrador de Django y mostrarlos de forma interactiva en el sitio web.

## El Objetivo

Queremos que un **Administrador** pueda crear "Carreras" y "Materias" fácilmente desde un panel de control, y que un **Usuario** normal pueda ver esas carreras en la web y, al hacer clic en una, ver las materias que le corresponden.

---

### Paso 1: El Panel de Administración (Nuestro "Backend")

**¿Por qué usamos el Admin?**
Para contenido que solo el administrador va a modificar (como crear una nueva carrera), es ineficiente construir formularios y vistas desde cero. Django nos regala una interfaz de administración completa y segura.

**¿Cómo se activa?**
Simplemente "registramos" nuestro modelo en el fichero `admin.py` de la aplicación.

```python
# gestion_carreras/admin.py
from django.contrib import admin
from .models import Carrera

@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):
    # Aquí personalizamos cómo se ve el modelo en el admin
    list_display = ("nombre", "universidad")
    filter_horizontal = ("materias",) # Una mejor UI para relaciones ManyToMany
```

Con esto, el administrador ya puede ir a `/admin` y empezar a cargar datos.

---

### Paso 2: Mostrar la Lista de Carreras (El Flujo de Django)

Para mostrar algo en una página, Django sigue un patrón claro: **URL -> Vista -> Template**.

**1. La URL (`urls.py`): La dirección de la página.**
Es la que conecta una dirección del navegador con una función específica (una vista).

```python
# apuntes/urls.py (el principal)
urlpatterns = [
    # ...
    path('carreras/', include('gestion_carreras.urls')),
]

# gestion_carreras/urls.py (el de la app)
urlpatterns = [
    path('', views.lista_carreras, name='lista_carreras'),
]
```

Cuando un usuario va a `/carreras/`, Django sabe que debe ejecutar la vista `lista_carreras`.

**2. La Vista (`views.py`): El cerebro de la operación.**
Su trabajo es: a) pedir los datos a la base de datos y b) enviar esos datos a un template para que los dibuje.

```python
# gestion_carreras/views.py
def lista_carreras(request):
    # a) Pide todas las carreras a la base de datos
    carreras = Carrera.objects.all()

    # b) Dibuja el template y le pasa la lista de carreras en el "contexto"
    return render(request, "gestion_carreras/lista_carreras.html", {"carreras": carreras})
```

**3. El Template (`lista_carreras.html`): El esqueleto HTML.**
Es un fichero HTML que recibe los datos que le envió la vista.

```html
<!-- gestion_carreras/lista_carreras.html -->
{% for carrera in carreras %}
<div class="carrera-item">
    <p>{{ carrera.nombre }}</p>
    <!-- Muestra el nombre de cada carrera -->
</div>
{% endfor %}
```

Usa un bucle `for` para recorrer la lista `carreras` y mostrar el nombre de cada una.

---

### Paso 3: Hacer la Lista Interactiva (Clic para ver Materias)

Ahora conectamos las carreras con sus materias.

**1. El Enlace Dinámico (Template)**
Modificamos el template para que cada carrera sea un enlace (`<a>`). La URL de destino se construye de forma segura con la etiqueta `{% url %}`.

```html
<!-- gestion_carreras/lista_carreras.html -->
<a href="{% url 'gestion_materias:materias_por_carrera' carrera.id %}"> {{ carrera.nombre }} </a>
```

-   **`gestion_materias:materias_por_carrera`**: Es el nombre único de la URL que queremos construir.
-   **`carrera.id`**: Le pasamos el ID de la carrera actual para que la URL sepa de qué carrera queremos ver las materias (ej: `/materias/por_carrera/5/`).

**2. La Nueva URL para Materias (URL)**
En la app `gestion_materias`, creamos una URL que espera recibir un número (el ID).

```python
# gestion_materias/urls.py
urlpatterns = [
    path('por_carrera/<int:carrera_id>/', views.listar_materias_por_carrera, name='materias_por_carrera'),
]
```

-   **`<int:carrera_id>`**: Captura el número de la URL y lo pasa a la vista como un parámetro llamado `carrera_id`.

**3. La Nueva Vista para Materias (Vista)**
Esta vista recibe el `carrera_id`, busca la carrera y luego sus materias relacionadas.

```python
# gestion_materias/views.py
def listar_materias_por_carrera(request, carrera_id):
    # Busca la carrera específica o devuelve un error 404
    carrera = get_object_or_404(Carrera, id=carrera_id)

    # La magia de Django: gracias a la relación ManyToMany,
    # podemos obtener solo las materias de ESA carrera.
    materias = carrera.materias.all()

    # Envía la carrera y su lista de materias al nuevo template
    context = {'carrera': carrera, 'materias': materias}
    return render(request, 'gestion_materias/listar_materias.html', context)
```

**4. El Template Final (`listar_materias.html`)**
Este template recibe la carrera y la lista de materias ya filtrada.

```html
<!-- gestion_materias/listar_materias.html -->
<h2>Materias de la carrera: {{ carrera.nombre }}</h2>

<ul>
    {% for materia in materias %}
    <li>{{ materia.nombre }}</li>
    {% endfor %}
</ul>
```

---

## Conclusión

El flujo de Django separa las responsabilidades de forma muy clara:

-   **Admin**: Gestiona los datos puros.
-   **URL**: Actúa como un mapa de carreteras.
-   **Vista**: Es el intermediario que busca los datos y decide qué mostrar.
-   **Template**: Es el encargado de dibujar el HTML y presentar los datos al usuario.

Siguiendo este patrón, puedes construir lógicas complejas de forma ordenada y mantenible.
