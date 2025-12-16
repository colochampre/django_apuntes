"""
Formularios para la gestión de materias.

Este módulo contiene formularios para filtrar materias por carrera.
"""

from django import forms
from gestion_carreras.models import Carrera

class CarreraFilterForm(forms.Form):
    """
    Formulario para filtrar materias según la carrera seleccionada.
    
    Utiliza un campo de selección (dropdown) poblado con las carreras disponibles.
    """
    carrera = forms.ModelChoiceField(
        queryset=Carrera.objects.all(),
        label="Carrera",
        required=False,
        widget=forms.Select(attrs={"class": "form-control"})
    )