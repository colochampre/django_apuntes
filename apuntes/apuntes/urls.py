"""
Configuración de URLs para el proyecto apuntes.

El parámetro `urlpatterns` define las rutas URL hacia las vistas. Para más información, consulte:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/

Ejemplos:
    Vistas basadas en funciones:
    1. Agregue una importación:  from my_app import views
    2. Agregue una URL a urlpatterns:  path('', views.home, name='home')

    Vistas basadas en clases:
    1. Agregue una importación:  from other_app.views import Home
    2. Agregue una URL a urlpatterns:  path('', Home.as_view(), name='home')

    Inclusión de otra configuración de URL (URLconf):
    1. Importe la función include(): from django.urls import include, path
    2. Agregue una URL a urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from .views import home
from django.conf import settings
from django.conf.urls.static import static

# Definición de las rutas URL principales del proyecto
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("usuarios/", include(("gestion_usuarios.urls", "gestion_usuarios"), namespace="gestion_usuarios")),
    path("carreras/", include(("gestion_carreras.urls", "gestion_carreras"), namespace="gestion_carreras")),
    path("materias/", include(("gestion_materias.urls", "gestion_materias"), namespace="gestion_materias")),
    path("apuntes/", include(("gestion_apuntes.urls", "gestion_apuntes"), namespace="gestion_apuntes")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
