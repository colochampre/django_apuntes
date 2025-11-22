from .helpers import limpiar_texto, colapsar_espacios, solo_digitos

def es_nombre_valido(valor=None) -> bool:
    """
    Valida si un valor es un nombre válido.
    Un nombre válido debe tener entre 2 y 100 caracteres y solo puede contener
    letras, espacios, guiones, apóstrofes y puntos.
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
    Valida si un valor es un año válido.
    Un año válido debe tener 4 dígitos.
    """
    if valor is None:
        return False
    v = solo_digitos(limpiar_texto(valor))
    return len(v) in (4,)
