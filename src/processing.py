import pandas as pd
from parser import ler_ps2
from utils import format_euro

def mostrar_df(df):
    print("="*120)
    print(f"{'RESUMO FICHEIRO':^120}\n")
    df["cabecalho"]["Valor"] = df["cabecalho"]["Valor"].apply(format_euro)
    df["movimentos"]["Valor"] = df["movimentos"]["Valor"].apply(format_euro)
    df["fecho"]["Valor_Total"] = df["fecho"]["Valor_Total"].apply(format_euro)
    texto_cab = df["cabecalho"].to_string(index=False)
    for linha in texto_cab.splitlines():
        print(linha.center(120))
    print("="*120)
    print("RESUMO FINAL\n".center(120))
    texto_mov = df["fecho"].to_string(index=False)
    for linha in texto_mov.splitlines():
        print(linha.center(120))
    print("="*120)
    print("MOVIMENTOS\n".center(120))
    texto_fec = df["movimentos"].to_string(index=False)
    for linha in texto_fec.splitlines():
        print(linha.center(120))

def resumo_varios_ficheiros(estrutura_dados):
    try:
        df_cab = pd.DataFrame(estrutura_dados["cabecalho"])
        df_mov = pd.DataFrame(estrutura_dados["movimentos"])
        df_fec = pd.DataFrame(estrutura_dados["fecho"])
        df_mov.drop(columns=["Ordem"], inplace=True, errors="ignore")
        valor_total = df_fec["Valor_Total"].sum()
        registro_total = int(df_fec["Total_Registros"].sum())
        erros = "; ".join(str(e).strip() for e in df_fec["Erros"] if e)
        quantidade_créditos = sum(df_mov["Tipo"] == "Crédito")
        quantidade_débitos = sum(df_mov["Tipo"] == "Débito")
        df_fec = pd.DataFrame([{"Valor_Total": float(valor_total),
                  "Total_Registros": int(registro_total),
                  "Quantidade_Créditos": quantidade_créditos,
                  "Quantidade_Débitos": quantidade_débitos,
                  "Erros": erros,}])
        return True, {
            "cabecalho": df_cab, 
            "movimentos": df_mov, 
            "fecho": df_fec
            }
    except Exception as e:
        return False, f"IMPOSSÍVEL CRIAR RESUMO. ERRO: {e}"

def transformar_para_df(estrutura_dados):
    try:
        df_cab = pd.DataFrame([estrutura_dados["cabecalho"]])
        df_mov = pd.DataFrame(estrutura_dados["movimentos"])
        df_fec = pd.DataFrame([estrutura_dados["fecho"]])
        return True, {
            "cabecalho": df_cab, 
            "movimentos": df_mov, 
            "fecho": df_fec
            }
    except Exception as e:
        return False, f"IMPOSSÍVEL TRANSFORMAR PARA DATAFRAME. ERRO: {e}"

def processar_ficheiros(paths):
    if not isinstance(paths, list):
        return False, f"Não contém ficheiros para analisar."
    todos_ficheiros = {}
    erros = []
    if len(paths) > 1:
        ficheiros_agrupados = {"cabecalho": [], "movimentos": [], "fecho": []}
        for path in paths:
            ok, info = ler_ps2(path)
            if ok:
                todos_ficheiros[info["cabecalho"]["Ficheiro"]] = info.copy()
                ficheiros_agrupados["cabecalho"].append(info["cabecalho"].copy())
                ficheiros_agrupados["movimentos"].extend(info["movimentos"].copy())
                ficheiros_agrupados["fecho"].append(info["fecho"].copy())
            else:
                erros.append(info)
        for key, values in todos_ficheiros.items():
            ok, maybe_df = transformar_para_df(values)
            if not ok:
                erros.append(maybe_df)
            else:
                todos_ficheiros[key] = maybe_df
        ok, maybe_resumo = resumo_varios_ficheiros(ficheiros_agrupados)
        if not ok:
            erros.append(maybe_resumo)
            return False, erros
        else:
            todos_ficheiros["resumo"] = maybe_resumo
            return True, todos_ficheiros
    else:
       ok, info = ler_ps2(paths[0]) 
       if ok:
            ok, maybe_df = transformar_para_df(info)
            if not ok:
                erros.append(maybe_df)
                return False, erros
            else:
                todos_ficheiros[info["cabecalho"]["Ficheiro"]] = maybe_df
            return True, todos_ficheiros
       else:
           erros.append(info)
           return False, erros
