def limpiar_texto(valor=None) -> str:
    return "" if valor is None else str(valor).strip()


def colapsar_espacios(valor: str) -> str:
    return " ".join(str(valor).split())


def solo_digitos(valor) -> str:
    return "".join(ch for ch in str(valor) if ch.isdigit())
