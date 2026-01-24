import os

def format_euro(x):
    try:
        valor = f"€{float(x):,.2f}".replace(".", "X").replace(",", ".").replace("X", ",")
        return valor
    except:
        return x

def format_float(x):
    try:
        valor = str(x).replace(".", "").replace(",", ".").replace("€", "")
        return valor
    except:
        return x

def cent_to_euros(cent):
    try:
        return f"{int(cent)/100:.2f}"
    except Exception as e:
        raise Exception(f"Erro: {e}")

def format_nif(nif):
    try:
        nif_ok = f"{nif[:3]}.{nif[3:6]}.{nif[6:]}"
        return nif_ok
    except:
        return nif

def format_nib(nib):
    try:
        nib_ok = f"{nib[:4]} {nib[4:8]} {nib[8:19]} {nib[19:]}"
        return nib_ok
    except:
        return nib
    
def limpar_terminal():
    os.system("cls" if os.name == "nt" else "clear")