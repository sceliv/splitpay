def round_currency(value, decimals=2):
    return round(value, decimals)


def safe_div(a, b):
    """
    Divide evitando errores por división entre 0.
    """
    if b == 0:
        return 0
    return a / b
