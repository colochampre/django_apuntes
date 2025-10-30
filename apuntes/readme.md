# Proyecto Django "apuntes"

Este repositorio contiene una pequeña aplicación Django de ejemplo llamada "apuntes".
En este README encontrarás instrucciones para instalar el proyecto, inicializarlo desde cero
y ejecutar el servidor de desarrollo en Windows (PowerShell).

## Requisitos

- Python 3.11+ (o 3.8+ si correspondiera)
- Git (opcional, para clonar el repositorio)
- Virtualenv (opcional, se usa el módulo builtin `venv`)

> Nota: El proyecto usa por defecto SQLite, por lo que no necesitas configurar una base de datos externa
si solo quieres ejecutar localmente.

## Pasos para instalar (rápido)

1. Clonar el repositorio (si no lo tienes local):

```powershell
git clone https://github.com/colochampre/django_apuntes.git
cd django_apuntes
```

2. Crear y activar un entorno virtual (PowerShell):

```powershell
python -m venv .venv
# Activar en PowerShell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la ejecución del script, puedes permitirlo solo para la sesión actual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

3. Instalar dependencias:

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

4. Aplicar migraciones y crear usuario administrador: // es para base de datos

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

5. Ejecutar el servidor de desarrollo:

```powershell
python manage.py runserver
# Visita http://127.0.0.1:8000/
```


## Comandos útiles

- Crear una nueva app dentro del proyecto:

```powershell
python manage.py startapp nombre_app
```

- Hacer nuevas migraciones después de cambiar modelos:

```powershell
python manage.py makemigrations
python manage.py migrate
```

- Ejecutar tests:

```powershell
python manage.py test
```

- Limpiar y volver a empezar con la base de datos SQLite (local):

```powershell
# Detener servidor si está corriendo
Remove-Item db.sqlite3 -ErrorAction SilentlyContinue
python manage.py migrate
python manage.py createsuperuser
```


## Estructura relevante del proyecto

- `manage.py` — script de administración de Django
- `apuntes/` — paquete principal del proyecto (settings, urls, wsgi, asgi)
- `gestion_*` — aplicaciones Django incluidas (usuarios, materias, carreras, apuntes)
- `templates/` — plantillas HTML


