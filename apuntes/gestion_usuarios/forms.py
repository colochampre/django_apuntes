from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, UserChangeForm as BaseUserChangeForm
from django.contrib.auth.models import User
from .models import Usuario

class UsuarioCreationForm(BaseUserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class UsuarioProfileForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['carrera']
        widgets = {
            'carrera': forms.CheckboxSelectMultiple,
        }