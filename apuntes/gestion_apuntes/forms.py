from django import forms
from .models import Apunte

class ApunteForm(forms.ModelForm):
    class Meta:
        model = Apunte
        fields = ['titulo', 'descripcion', 'archivo', 'materia']