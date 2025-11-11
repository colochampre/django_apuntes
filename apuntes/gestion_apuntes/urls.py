from django.urls import path
from .views import apuntes

urlpatterns = [
    path('', apuntes, name='apuntes'),
]
