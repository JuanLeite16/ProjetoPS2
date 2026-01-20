def format_euro(valor):
    return f"€{float(valor):,.2f}".replace(".", "X").replace(",", ".").replace("X", ",")

def format_float(valor):
    return str(valor).replace(".", "").replace(",", ".").replace("€", "")

def cent_to_euros(cent):
    try:
        return f"{float(cent)/100:.2f}"
    except Exception as e:
        raise Exception(f"Erro: {e}")

def format_nif(nif):
    return f"{nif[:3]}.{nif[3:6]}.{nif[6:]}"

def format_nib(nib):
    return f"{nib[:4]} {nib[4:8]} {nib[8:19]} {nib[19:]}"