def limpiar_texto(valor=None) -> str:
    """
    Limpia un texto eliminando los espacios en blanco al principio y al final.
    Si el valor es None, devuelve una cadena vacía.
    """
    return "" if valor is None else str(valor).strip()


def colapsar_espacios(valor: str) -> str:
    """
    Colapsa los espacios en blanco de un texto, reemplazando
    múltiples espacios por uno solo.
    """
    return " ".join(str(valor).split())


def solo_digitos(valor) -> str:
    """
    Elimina todos los caracteres que no son dígitos de un texto.
    """
    return "".join(ch for ch in str(valor) if ch.isdigit())
