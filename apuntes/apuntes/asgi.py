"""
Configuración ASGI para el proyecto apuntes.

Expone el invocable ASGI como una variable de nivel de módulo llamada ``application``.

Para más información sobre este archivo, consulte:
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apuntes.settings')

application = get_asgi_application()
