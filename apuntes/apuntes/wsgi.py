"""
Configuración WSGI para el proyecto apuntes.

Expone el invocable WSGI como una variable de nivel de módulo llamada ``application``.

Para más información sobre este archivo, consulte:
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apuntes.settings')

application = get_wsgi_application()
