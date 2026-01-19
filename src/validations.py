from pathlib import Path
import pandas as pd

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

def validar_ps2(ficheiro):
    if not ficheiro:
        raise ValueError("Nenhum ficheiro especificado.")
    p = Path(ficheiro)
    if not p.exists():
        raise FileNotFoundError("O ficheiro não existe.")
    if not p.is_file():
        raise ValueError("Não é um ficheiro.")
    if p.suffix.lower() != ".ps2":
        raise ValueError("Não é um ficheiro do tipo .ps2")
    if p.stat().st_size < 1:
        raise ValueError("Ficheiro vazio")
    
    return p

def validar_existencia_dados(estrutura_dados):
    if isinstance(estrutura_dados, dict):
        valor = obter_valor_seguro_dict(estrutura_dados, "movimentos", [])
        return valor

def obter_valor_seguro_df(df, coluna, linha=0, valor_padrao="—"):
    try:
        return df.at[linha, coluna]
    except (KeyError, IndexError):
        return valor_padrao

def obter_valor_seguro_dict(estrutura_dados, chave_desejada, valor_padrao="—"):
    if isinstance(estrutura_dados, dict):
        valor = estrutura_dados.get(chave_desejada, valor_padrao)
        return valor if valor not in (None, "") else valor_padrao
    
    return valor_padrao