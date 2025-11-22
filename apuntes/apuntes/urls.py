from django.contrib import admin
from django.urls import path, include
from .views import home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path(
        "usuarios/",
        include(
            ("gestion_usuarios.urls", "gestion_usuarios"), namespace="gestion_usuarios"
        ),
    ),
    path(
        "carreras/",
        include(
            ("gestion_carreras.urls", "gestion_carreras"), namespace="gestion_carreras"
        ),
    ),
    path(
        "materias/",
        include(
            ("gestion_materias.urls", "gestion_materias"), namespace="gestion_materias"
        ),
    ),
    path(
        "apuntes/",
        include(
            ("gestion_apuntes.urls", "gestion_apuntes"), namespace="gestion_apuntes"
        ),
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
