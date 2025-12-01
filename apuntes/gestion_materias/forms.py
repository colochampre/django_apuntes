from django import forms
from gestion_carreras.models import Carrera

class CarreraFilterForm(forms.Form):
    carrera = forms.ModelChoiceField(
        queryset=Carrera.objects.all(),
        label="Carrera",
        required=False,
        widget=forms.Select(attrs={"class": "form-control"})
    )