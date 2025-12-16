"""
Modelos de datos para la gestión de apuntes.

Este módulo define los modelos principales para el almacenamiento de apuntes académicos
y sus puntuaciones asociadas.
"""

from django.db import models
from django.db.models import Avg
from gestion_usuarios.models import Usuario
from gestion_materias.models import Materia
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

def validar_tamano_archivo(archivo):
    """
    Valida que el archivo no supere un tamaño máximo predefinido.

    Args:
        archivo (File): El archivo a validar.

    Raises:
        ValidationError: Si el archivo supera el límite (10MB).
    """
    limite_mb = 10
    if archivo.size > limite_mb * 1024 * 1024:
        raise ValidationError(f"El archivo no puede superar {limite_mb}MB")

class Apunte(models.Model):
    """
    Modelo que representa un apunte académico subido por un usuario.

    Contiene información sobre el título, descripción, archivo adjunto,
    materia asociada y usuario que lo subió.
    """
    titulo = models.CharField(max_length=100, null=False, blank=False)
    descripcion = models.TextField()
    archivo = models.FileField(upload_to="apuntes/", validators=[
            FileExtensionValidator(allowed_extensions=[
                "c", "cpp", "css", "doc", "docx", "drawio", "gif", "html", 
                "java", "jpeg", "jpg", "js", "json", "md", "mp3", "pdf", "png", 
                "ppt", "pptx", "psc", "py", "svg", "txt", "webp", "xls", 
                "xlsx", "xml"
            ]),
            validar_tamano_archivo,
        ],
    )
    fecha_publicacion = models.DateField(auto_now_add=True)
    materia = models.ForeignKey(Materia, on_delete=models.SET_NULL, null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['fecha_publicacion', 'titulo']
        indexes = [
            models.Index(fields=["-fecha_publicacion"], name="apunte_fecha_idx"),
            models.Index(fields=["materia", "-fecha_publicacion"], name="apunte_materia_fecha_idx"),
            models.Index(fields=["usuario"], name="apunte_usuario_idx"),
        ]
        verbose_name = "Apunte"
        verbose_name_plural = "Apuntes"
    
    def __str__(self):
        return (f'{self.titulo} - {self.fecha_publicacion} - '
                f'{self.usuario.user.username if self.usuario else "Anónimo"} - {self.fecha_publicacion}')
    
    def promedio_puntuacion(self):
        """
        Calcula el promedio de las puntuaciones recibidas.

        Returns:
            float or None: El promedio redondeado a 1 decimal, o None si no hay puntuaciones.
        """
        promedio = self.puntuaciones.aggregate(Avg('valor'))['valor__avg']
        return round(promedio, 1) if promedio else None
    
    def total_puntuaciones(self):
        """
        Retorna el número total de puntuaciones recibidas.

        Returns:
            int: Cantidad de puntuaciones.
        """
        return self.puntuaciones.count()
    
    def puntuacion_usuario(self, usuario):
        """
        Retorna la puntuación que un usuario específico dio a este apunte.

        Args:
            usuario (Usuario): El usuario a consultar.

        Returns:
            int or None: El valor de la puntuación o None si el usuario no ha puntuado.
        """
        try:
            puntuacion = self.puntuaciones.get(usuario=usuario)
            return puntuacion.valor
        except Puntuacion.DoesNotExist:
            return None

    def get_file_type(self):
        """
        Determina la categoría del archivo basándose en su extensión.

        Returns:
            str: Categoría del archivo ('image', 'pdf', 'word', etc.).
        """
        name = self.archivo.name.lower()
        if name.endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg", ".webp")):
            return "image"
        elif name.endswith(".pdf"):
            return "pdf"
        elif name.endswith((".doc", ".docx")):
            return "word"
        elif name.endswith((".xls", ".xlsx")):
            return "excel"
        elif name.endswith((".ppt", ".pptx")):
            return "powerpoint"
        elif name.endswith((".drawio")):
            return "diagram"
        elif name.endswith(("cpp", ".html", ".java", "psc", ".xml")):
            return "code"
        elif name.endswith((".c", ".css", ".js", ".json", ".txt", ".md", ".py")):
            return "text"
        elif name.endswith((".mp3")):
            return "audio"
        return "other"

    @property
    def extension(self):
        """
        Devuelve la extensión del archivo en mayúsculas sin el punto.

        Returns:
            str: Extensión del archivo (ej: 'PDF').
        """
        name = self.archivo.name
        if "." in name:
            return name.split(".")[-1].upper()
        return ""

class Puntuacion(models.Model):
    """
    Modelo para almacenar las puntuaciones individuales de cada usuario a un apunte.
    
    Permite registrar la valoración (1-5) que un usuario asigna a un apunte específico.
    """
    apunte = models.ForeignKey(Apunte, on_delete=models.CASCADE, related_name='puntuaciones')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    valor = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    fecha = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('apunte', 'usuario')  # Un usuario solo puede puntuar una vez cada apunte
        ordering = ['-fecha']
    
    def __str__(self):
        return f'{self.usuario.user.username} - {self.apunte.titulo} - {self.valor}★'

