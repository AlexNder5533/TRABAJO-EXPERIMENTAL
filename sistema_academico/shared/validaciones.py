import re


def es_email_valido(email):
    return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", str(email).strip()))


def es_entero(valor):
    try:
        int(valor)
        return True
    except (TypeError, ValueError):
        return False
