
from django import forms
from .models import Apunte

EXTENSIONES_PERMITIDAS = [
    "c", "cpp", "css", "doc", "docx", "drawio", "gif", "html", 
    "java", "jpeg", "jpg", "js", "json", "md", "mp3", "pdf", "png", 
    "ppt", "pptx", "psc", "py", "svg", "txt", "webp", "xls", "xlsx", "xml"
]

class ApunteForm(forms.ModelForm):
    """
    Formulario para la creación y edición de apuntes.
    Permite subir archivos y definir título y descripción.
    Incluye validaciones de tamaño y tipo de archivo.
    """
    def __init__(self, *args, **kwargs):
        # Extraer la materia del kwargs si está presente
        self.materia = kwargs.pop('materia', None)
        super().__init__(*args, **kwargs)
    
    class Meta:
        """Metadatos del formulario ApunteForm."""
        model = Apunte
        fields = ['titulo', 'descripcion', 'archivo', 'materia']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título del apunte'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe brevemente el contenido del apunte',
                'rows': 4
            }),
            'archivo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': ',' .join(f'.{ext}' for ext in EXTENSIONES_PERMITIDAS)
            })
        }
    
    def clean_archivo(self):
        """
        Validación adicional del archivo subido.
        Verifica tamaño y tipo MIME si está disponible.
        """
        archivo = self.cleaned_data.get('archivo')
        
        if archivo:
            # Validar tamaño (10MB máximo)
            limite_mb = 10
            if archivo.size > limite_mb * 1024 * 1024:
                raise forms.ValidationError(
                    f'El archivo es muy grande. Tamaño máximo: {limite_mb}MB. '
                    f'Tu archivo: {archivo.size / (1024 * 1024):.2f}MB'
                )
            
            # Validar que el archivo tenga extensión
            nombre = archivo.name.lower()
            extensiones_validas = [f".{ext}" for ext in EXTENSIONES_PERMITIDAS]
            
            if not any(nombre.endswith(ext) for ext in extensiones_validas):
                raise forms.ValidationError(
                    f'Tipo de archivo no permitido. Extensiones válidas: '
                    f'{", ".join(extensiones_validas)}'
                )
        
        return archivo
    
    def clean_titulo(self):
        """
        Validación del título: no puede estar vacío ni ser solo espacios.
        Además, verifica que no exista otro apunte con el mismo título en la misma materia.
        """
        titulo = self.cleaned_data.get('titulo')
        
        if titulo and not titulo.strip():
            raise forms.ValidationError('El título no puede estar vacío')
        
        titulo = titulo.strip() if titulo else titulo
        
        # Verificar si ya existe un apunte con el mismo título en la misma materia
        if titulo and self.materia:
            # Excluir el apunte actual si estamos editando (self.instance.pk existe)
            apuntes_existentes = Apunte.objects.filter(
                titulo__iexact=titulo,  # iexact = case-insensitive
                materia=self.materia
            )
            
            # Si estamos editando, excluir el apunte actual
            if self.instance and self.instance.pk:
                apuntes_existentes = apuntes_existentes.exclude(pk=self.instance.pk)
            
            if apuntes_existentes.exists():
                raise forms.ValidationError(
                    f'Ya existe un apunte "{titulo}" en esta materia. '
                    'Por favor, elige un título diferente.'
                )
        
        return titulo
