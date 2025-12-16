"""
Validadores personalizados para el proyecto.

Este módulo define funciones de validación específicas para campos de modelos y formularios,
asegurando que los datos cumplan con los requisitos de negocio.
"""

from .helpers import limpiar_texto, colapsar_espacios, solo_digitos

def es_nombre_valido(valor=None) -> bool:
    """
    Verifica si un nombre es válido permitiendo solo ciertos caracteres y una longitud específica.
    
    Permite letras (incluyendo acentos y caracteres especiales comunes en nombres), espacios, guiones y puntos.
    La longitud debe estar entre 2 y 100 caracteres después de limpiar y normalizar el texto.

    Args:
        valor (str, opcional): El nombre a validar.

    Returns:
        bool: True si el nombre es válido, False en caso contrario.
    """
    permitidos = set(
       "abcdefghijklmnopqrstuvwxyz"
       "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
       "áéíóúüñÁÉÍÓÚÜÑ"
       "àèìòùÀÈÌÒÙ"
       "âêîôûÂÊÎÔÛ"
       "äëïöüÿÄËÏÖÜŸ"
       "ãõÃÕ"
       "çÇ"
       " -'."
    )
    if valor is None:
        return False
    v = colapsar_espacios(limpiar_texto(valor))
    return 2 <= len(v) <= 100 and all(ch in permitidos for ch in v)


def es_anio_valido(valor=None) -> bool:
    """
    Valida si un valor representa un año válido de 4 dígitos.

    Args:
        valor (Any, opcional): El valor a validar.

    Returns:
        bool: True si el valor contiene exactamente 4 dígitos, False en caso contrario.
    """
    if valor is None:
        return False
    v = solo_digitos(limpiar_texto(valor))
    return len(v) in (4,)