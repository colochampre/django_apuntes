# 📚 Plataforma de Gestión de Apuntes Universitarios

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2.7-green.svg)
![Status](https://img.shields.io/badge/Estado-Finalizado-success.svg)

**Materia:** Programación 2 - Tecnicatura Universitaria en Programación (UTN FRLP)  
**Estado:** Proyecto Integrador Final

---

## 📖 Descripción del Proyecto

Esta aplicación web, desarrollada con **Django**, nace con el objetivo de democratizar y facilitar el intercambio de material de estudio entre estudiantes. La plataforma permite a los usuarios compartir, buscar y descargar apuntes de las diferentes materias y carreras de la universidad, fomentando una comunidad colaborativa de aprendizaje.

El sistema resuelve la problemática de la dispersión del material de estudio, centralizando archivos (PDFs, textos) en un entorno organizado por **Carreras** y **Materias**, con un sistema de gestión de usuarios seguro y eficiente.

---

## 🚀 Funcionalidades Principales

El proyecto cumple con todos los requerimientos de la rúbrica de evaluación, destacando:

-   **Gestión de Usuarios:**
    -   Registro e inicio de sesión seguro.
    -   Perfiles de usuario personalizados (Modelo `Usuario` vinculado a `User` OneToOne).
    -   Sistema de reputación basado en la calidad de los aportes.
-   **Organización Académica:**
    -   **Carreras:** Visualización de la oferta académica.
    -   **Materias:** Listado de materias asociadas a cada carrera (Relación _Many-to-Many_).
-   **Gestión de Apuntes:**
    -   **Subida de Archivos:** Los usuarios autenticados pueden publicar apuntes vinculados a una materia específica con validación de extensiones y tamaño.
    -   **Descarga:** Acceso directo a los archivos compartidos.
    -   **Puntuación:** Sistema de votación (1-5 estrellas) para calificar la calidad del material.
    -   **Clasificación:** Organización intuitiva por título, descripción y fecha.

-   **Interfaz Gráfica:**
    -   Diseño limpio y responsive utilizando **Bootstrap 5**.
    -   Uso de **Plantillas Django** (`extends`, `block`, `include`) para una arquitectura frontend modular y mantenible.

---

## 🧠 Aspectos Técnicos Destacados

Para garantizar un rendimiento profesional y un código limpio, se implementaron las siguientes mejoras de ingeniería de software:

*   **Optimización de Consultas (N+1 Problems):** Se implementó `prefetch_related` con objetos `Prefetch` personalizados en las vistas de materias para cargar las puntuaciones de los usuarios en una única consulta, reduciendo drásticamente la carga en la base de datos al listar apuntes.
*   **Señales (Signals):** Automatización de la creación de perfiles de usuario mediante `post_save` signals, asegurando integridad de datos y separando responsabilidades (Principio de Responsabilidad Única).
*   **Testing Automatizado:** Cobertura de tests unitarios y de integración para modelos y vistas críticas, asegurando la robustez de las funcionalidades principales (Subida, Votación, Eliminación).
*   **Validadores Personalizados:** Control estricto de tipos de archivos y tamaños para seguridad del servidor.

---

## 🛠️ Stack Tecnológico

-   **Backend:** Python 3.11+ / Django 5.2.7
-   **Base de Datos:** SQLite (Configuración por defecto para desarrollo)
-   **Frontend:** HTML5, CSS3, Bootstrap 5
-   **Control de Versiones:** Git & GitHub

---

## 💻 Instalación y Ejecución

Sigue estos pasos para levantar el entorno de desarrollo en tu máquina local:

### 1. Clonar el Repositorio

```bash
git clone https://github.com/colochampre/django_apuntes.git
cd django_apuntes
```

### 2. Preparar el Entorno

Es necesario ingresar al directorio del proyecto donde se encuentra el archivo `manage.py`.

```bash
cd apuntes
```

### 3. Crear Entorno Virtual

Es recomendable usar un entorno aislado para las dependencias.

**En Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
```

> _Nota: Si tienes errores de permisos en PowerShell, ejecuta: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`_

### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 5. Configuración de Base de Datos

Aplica las migraciones para generar el esquema de base de datos (SQLite):

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear Superusuario (Opcional)

Para acceder al panel de administración de Django:

```bash
python manage.py createsuperuser
```

### 7. Iniciar el Servidor

```bash
python manage.py runserver
```

Accede a la aplicación en: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🧪 Ejecución de Tests

El proyecto cuenta con una suite de tests automatizados. Para ejecutarlos:

```bash
python manage.py test
```

Esto validará la integridad de los modelos y el correcto funcionamiento de las vistas principales.

---

## 📂 Estructura del Proyecto

El código está organizado siguiendo el patrón de diseño de Django:

-   `apuntes/`: Configuración principal del proyecto (`settings.py`, `urls.py`).
-   `gestion_usuarios/`: Lógica de autenticación, señales, formularios y modelos de perfil.
-   `gestion_carreras/`: Administración de las carreras universitarias.
-   `gestion_materias/`: Administración de las materias y su vinculación con carreras.
-   `gestion_apuntes/`: Núcleo de la aplicación (Modelos de apuntes, subida de archivos, sistema de puntuación).
-   `templates/`: Plantillas HTML globales y estructura base (`base.html`).
-   `static/`: Archivos CSS, imágenes y scripts del frontend.
-   `media/`: Directorio donde se almacenan los archivos subidos por los usuarios (local).

---

## 👥 Equipo de Desarrollo

Este proyecto fue realizado de manera colaborativa.

| Integrante                   | Rol Principal                     |
| :--------------------------- | :-------------------------------- |
| **Reynoso Maite**            | _Base de datos, Estilos_          |
| **Cardenas Lautaro**         | _Base de datos, Estilos_          |
| **Boda Juan Pedro**          | _Backend, Testing_                |
| **Champredonde Juan Martin** | _Frontend, Testing_               |

---

**Programación 2 - 2025**  
_Desarrollado con Django y mucha dedicación._