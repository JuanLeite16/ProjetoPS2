import pandas as pd
from pathlib import Path
from parser import ler_ps2

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.colheader_justify', 'center')

def resumo_varios_ficheiros(estrutura_dados):
    try:
        df_cab = pd.DataFrame(estrutura_dados["cabecalho"])
        df_mov = pd.DataFrame(estrutura_dados["movimentos"])
        df_fec = pd.DataFrame(estrutura_dados["fecho"])
        df_mov.drop(columns=["Ordem"], inplace=True)
        valor_total = df_fec["Valor_Total"].sum()
        registro_total = int(df_fec["Total_Registros"].sum())
        df_fec.drop(df_fec.index, inplace=True)
        df_fec.loc[0, "Valor_Total"] = valor_total
        df_fec.loc[0, "Total_Registros"] = registro_total
        print(registro_total)
        df_fec.loc[0, "Erros"] = ""
        return {
            "cabecalho": df_cab, 
            "movimentos": df_mov, 
            "fecho": df_fec
            }
    except Exception as e:
        print(e)
        return estrutura_dados

def transformar_para_df(estrutura_dados):
    try:
        df_cab = pd.DataFrame([estrutura_dados["cabecalho"]])
        df_mov = pd.DataFrame(estrutura_dados["movimentos"])
        df_fec = pd.DataFrame([estrutura_dados["fecho"]])
        return {
            "cabecalho": df_cab, 
            "movimentos": df_mov, 
            "fecho": df_fec
            }
    except Exception as e:
        print(e)
        return estrutura_dados

def processar_ficheiros(paths):
    if not isinstance(paths, list):
        return None
    todos_ficheiros = {}
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
                print(info)
        for key, values in todos_ficheiros.items():
            todos_ficheiros[key] = transformar_para_df(values)
        todos_ficheiros["resumo"] = resumo_varios_ficheiros(ficheiros_agrupados)
        return todos_ficheiros
    else:
       ok, info = ler_ps2(paths[0]) 
       if ok:
            todos_ficheiros[info["cabecalho"]["Ficheiro"]] = transformar_para_df(info)
            return todos_ficheiros
