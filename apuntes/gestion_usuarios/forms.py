from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, UserChangeForm as BaseUserChangeForm
from django.contrib.auth.models import User
from .models import Usuario

class UsuarioCreationForm(BaseUserCreationForm):
    email = forms.EmailField(
        max_length=254,
        label='Correo electrónico',
        help_text='Requerido. Ingresá una dirección de correo válida.',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'tu@email.com'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label='Nombre',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu nombre'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label='Apellido',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu apellido'
        })
    )

    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)
        labels = {
            'username': 'Usuario',
        }
        help_texts = {
            'username': 'Máximo 150 caracteres con letras, dígitos o [@ . + - _]',
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Elegí un nombre de usuario'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar los campos de contraseña
        self.fields['password1'].label = 'Contraseña'
        self.fields['password1'].help_text = '''
            <ul>
                <li>Debe contener al menos 8 caracteres.</li>
                <li>No puede ser completamente numérica.</li>
            </ul>
        '''
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ingresá tu contraseña'
        })
        
        self.fields['password2'].label = 'Confirmar contraseña'
        self.fields['password2'].help_text = 'Ingresá la misma contraseña para verificación.'
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmá tu contraseña'
        })


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