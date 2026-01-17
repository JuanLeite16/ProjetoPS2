def validar_nif(nif):
    if not nif.isdigit() or len(nif) != 9:
        return False
    else:
        try:
            soma = sum([int(nif[i])*(9-i) for i in range(8)])
            resto = soma%11
            return True if (0 if resto <= 1 else 11 - resto) == int(nif[-1]) else False
        except Exception as e:
            print(f"Motivo de erro: {e}")
            return False

def validar_nib(nib):
    if not nib.isdigit() or len(nib) != 21:
        return False

    iban = nib + "252950"
    return int(iban) % 97 == 1
