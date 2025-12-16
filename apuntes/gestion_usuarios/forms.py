"""
Formularios para la gestión de usuarios.

Este módulo contiene los formularios para el registro, edición y gestión del perfil de los usuarios,
incluyendo validaciones personalizadas para correos electrónicos y contraseñas.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, UserChangeForm as BaseUserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from .models import Usuario
import dns.resolver
import socket

class UsuarioCreationForm(BaseUserCreationForm):
    """
    Formulario personalizado para la creación de nuevos usuarios.
    
    Añade campos para el nombre, apellido y correo electrónico, e incluye validaciones
    avanzadas para el correo (formato, existencia, dominios desechables y registros MX).
    """
    email = forms.EmailField(
        max_length=254,
        required=True,
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

    def clean_email(self):
        """
        Valida que el email tenga un formato válido, que no esté ya registrado,
        y que el dominio tenga registros MX válidos (servidor de correo).
        
        Returns:
            str: El email validado.
        
        Raises:
            ValidationError: Si el email no es válido, ya existe o el dominio es sospechoso.
        """
        email = self.cleaned_data.get('email')
        
        if not email:
            raise ValidationError('El correo electrónico es obligatorio.')
        
        # Validar formato de email
        validator = EmailValidator(message='Ingresá una dirección de correo electrónico válida.')
        try:
            validator(email)
        except ValidationError:
            raise ValidationError('El formato del correo electrónico no es válido.')
        
        # Validar que el email no esté ya registrado
        if User.objects.filter(email=email).exists():
            raise ValidationError('Este correo electrónico ya está registrado.')
        
        # Validar que el dominio exista y tenga registros MX
        if '@' in email:
            domain = email.split('@')[1]
            
            # Lista de dominios temporales/desechables comunes que querés bloquear
            blocked_domains = ['tempmail.com', 'throwaway.email', 'guerrillamail.com', '10minutemail.com']
            if domain.lower() in blocked_domains:
                raise ValidationError('No se permiten correos electrónicos temporales o desechables.')
            
            # Verificar que el dominio tenga registros MX (servidores de correo)
            try:
                mx_records = dns.resolver.resolve(domain, 'MX')
                if not mx_records:
                    raise ValidationError('El dominio del correo electrónico no tiene servidores de correo configurados.')
            except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
                raise ValidationError('El dominio del correo electrónico no existe o no está configurado correctamente.')
            except dns.exception.Timeout:
                # Si hay timeout, permitir el registro (para no bloquear por problemas de red)
                pass
            except Exception:
                # Para otros errores de DNS, permitir el registro
                pass
        
        return email

class UserEditForm(forms.ModelForm):
    """
    Formulario para editar la información básica del usuario (User).
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class UsuarioProfileForm(forms.ModelForm):
    """
    Formulario para editar la información del perfil extendido del usuario.
    
    Permite seleccionar las carreras que el usuario está cursando.
    """
    class Meta:
        model = Usuario
        fields = ['carrera']
        widgets = {
            'carrera': forms.CheckboxSelectMultiple,
        }