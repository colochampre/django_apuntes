from django.urls import path
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
]