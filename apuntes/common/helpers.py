"""
Módulo de utilidades y funciones auxiliares.

Este módulo contiene funciones de ayuda generales para el procesamiento de texto
y otras tareas comunes utilizadas en todo el proyecto.
"""

def limpiar_texto(valor=None) -> str:
    """
    Convierte el valor dado a una cadena y elimina los espacios en blanco al inicio y al final.

    Args:
        valor (Any, opcional): El valor a limpiar. Puede ser None.

    Returns:
        str: La cadena limpia o una cadena vacía si el valor es None.
    """
    return "" if valor is None else str(valor).strip()


def colapsar_espacios(valor: str) -> str:
    """
    Reduce múltiples espacios consecutivos en una cadena a un solo espacio.

    Args:
        valor (str): La cadena a procesar.

    Returns:
        str: La cadena con los espacios colapsados.
    """
    return " ".join(str(valor).split())


def solo_digitos(valor) -> str:
    """
    Extrae únicamente los caracteres numéricos de un valor dado.

    Args:
        valor (Any): El valor del cual extraer los dígitos.

    Returns:
        str: Una cadena que contiene solo los dígitos del valor original.
    """
    return "".join(ch for ch in str(valor) if ch.isdigit())