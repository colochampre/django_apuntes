"""
Configuración de Django para el proyecto apuntes.

Generado por 'django-admin startproject' usando Django 5.2.7.

Para más información sobre este archivo, consulte:
https://docs.djangoproject.com/en/5.2/topics/settings/

Para la lista completa de configuraciones y sus valores, consulte:
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

import os
from pathlib import Path

# Construye las rutas dentro del proyecto como: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Configuraciones de desarrollo de inicio rápido - no aptas para producción
# Consulte https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# ADVERTENCIA DE SEGURIDAD: ¡Mantenga secreta la clave utilizada en producción!
# En producción, establezca la variable de entorno DJANGO_SECRET_KEY
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-emks*vu&0n73h89i8-s4olpc5k78*yenehaw2%@drd^&*#84h(')

# ADVERTENCIA DE SEGURIDAD: ¡No ejecute con debug activado en producción!
# En producción, establezca DJANGO_DEBUG=False
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

# En producción, defina los hosts permitidos separados por comas en DJANGO_ALLOWED_HOSTS
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',') if os.environ.get('DJANGO_ALLOWED_HOSTS') else []


# Definición de aplicaciones instaladas

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'common.apps.CommonConfig',
    'gestion_apuntes',
    'gestion_carreras',
    'gestion_materias',
    'gestion_usuarios',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'apuntes.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'apuntes.wsgi.application'


# Configuración de la base de datos
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Validación de contraseñas
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internacionalización
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'es-AR'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_TZ = True


# Archivos estáticos (CSS, JavaScript, Imágenes)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [BASE_DIR / 'static']

STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configuración de X-Frame-Options para permitir iframes
# SAMEORIGIN permite que los archivos se muestren en iframes del mismo dominio
X_FRAME_OPTIONS = 'SAMEORIGIN'

# Tipo de campo de clave primaria por defecto
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'home'  # Redirección por defecto si no hay 'next'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'gestion_usuarios:login'
