"""
Configuración de URLs para la aplicación gestion_usuarios.

Define las rutas para registro, inicio de sesión, cierre de sesión y gestión de perfiles.
"""

from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

app_name = 'gestion_usuarios'

urlpatterns = [
    path("register/", views.registro, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="gestion_usuarios/login.html"),
        name="login",
    ),
    path("logout/", views.custom_logout, name="logout"),
    path("perfil/", views.perfil, name="perfil"),
    path("perfil/editar/", views.editar_perfil, name="editar_perfil"),
    path(
        "perfil/cambiar-password/",
        auth_views.PasswordChangeView.as_view(
            template_name="gestion_usuarios/change_password.html",
            success_url=reverse_lazy("gestion_usuarios:perfil")
        ),
        name="cambiar_password",
    ),
    path("usuario/<str:username>/", views.ver_perfil_usuario, name="ver_perfil"),
]