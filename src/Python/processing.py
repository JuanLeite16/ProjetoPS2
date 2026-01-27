## @file processing.py
#  @package processing
#  @brief Processamento e agregação de ficheiros PS2.
#  @details Contém funções responsáveis pela leitura, transformação,
#  agregação e resumo de ficheiros PS2, bem como pela execução do
#  processo completo de análise de um ou vários ficheiros.

import pandas as pd
from parser import ler_ps2
from utils import format_euro
import subprocess

## @brief Mostra um resumo formatado dos dados de um DataFrame.
# @details Apresenta no terminal o resumo do ficheiro, incluindo cabeçalho,
# fecho e movimentos, aplicando formatação monetária aos valores.
# @param df Estrutura de dados (DataFrame/dicionário de DataFrames) a apresentar.
def mostrar_df(df):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    pd.set_option('display.colheader_justify', 'center')
    
    df_temp = df.copy()
    print("="*120)
    print(f"{'RESUMO FICHEIRO':^120}\n")
    df_temp["cabecalho"]["Valor"] = df_temp["cabecalho"]["Valor"].apply(format_euro)
    df_temp["movimentos"]["Valor"] = df_temp["movimentos"]["Valor"].apply(format_euro)
    df_temp["fecho"]["Valor_Total"] = df_temp["fecho"]["Valor_Total"].apply(format_euro)
    texto_cab = df_temp["cabecalho"].to_string(index=False)
    for linha in texto_cab.splitlines():
        print(linha.center(120))
    print("="*120)
    print("RESUMO GLOBAL\n".center(120))
    texto_fec = df_temp["fecho"].to_string(index=False)
    for linha in texto_fec.splitlines():
        linha = linha.replace("_", " ")
        print(linha.center(120))
    print("="*120)
    print("MOVIMENTOS\n".center(120))
    texto_mov = df_temp["movimentos"].to_string(index=False)
    for linha in texto_mov.splitlines():
        print(linha.center(120))
    print("\n\n\n")

## @brief Gera um resumo agregado a partir de vários ficheiros.
# @details Constrói DataFrames de cabeçalho, movimentos e fecho, agregando totais,
# número de registos, contagem de créditos/débitos e mensagens de erro.
# @param estrutura_dados Estrutura com as chaves "cabecalho", "movimentos" e "fecho".
# @return (bool, dict|str) Tuplo com sucesso e, em caso positivo, dicionário com
# DataFrames; caso contrário, mensagem de erro.
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

## @brief Converte uma estrutura de dados em DataFrames.
# @details Transforma os dados de cabeçalho, movimentos e fecho em DataFrames
# do pandas, mantendo a estrutura original.
# @param estrutura_dados Estrutura com as chaves "cabecalho", "movimentos" e "fecho".
# @return (bool, dict|str) Tuplo com sucesso e, em caso positivo, dicionário com
# DataFrames; caso contrário, mensagem de erro.
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

## @brief Processa um ou vários ficheiros PS2 e devolve os dados estruturados.
# @details Lê cada ficheiro PS2, converte os resultados para DataFrames e gera um
# resumo (individual ou agregado) conforme a quantidade de ficheiros.
# @param paths Lista de caminhos para ficheiros PS2.
# @return (bool, dict|None, dict) Tuplo com sucesso, dicionário com ficheiros processados
# (inclui a chave "resumo") e dicionário de erros.
def processar_ficheiros(paths):
    if not isinstance(paths, list):
        return False, None, {"erro": f"Não contém ficheiros para analisar."}
    if paths == []:
        return False, None, {"erro": f"Não contém ficheiros para analisar."}
    todos_ficheiros = {}
    erros = {}
    c = 0
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
                erros[info[0]] = info[1]
        for key, values in todos_ficheiros.items():
            ok, maybe_df = transformar_para_df(values)
            if not ok:
                erros[paths[c]] = maybe_df
                c += 1
            else:
                todos_ficheiros[key] = maybe_df
                c += 1
        ok, maybe_resumo = resumo_varios_ficheiros(ficheiros_agrupados)
        if not ok:
            erros["resumo"] = maybe_resumo
            return False, None, erros
        else:
            todos_ficheiros["resumo"] = maybe_resumo
            return True, todos_ficheiros, erros
    else:
       ok, info = ler_ps2(paths[0]) 
       if ok:
            ok, maybe_df = transformar_para_df(info)
            if not ok:
                erros[paths[0]] = maybe_df
                return False, None, erros
            else:
                todos_ficheiros[info["cabecalho"]["Ficheiro"]] = maybe_df
                todos_ficheiros["resumo"] = maybe_df
            return True, todos_ficheiros, erros
       else:
           erros[info[0]] = info[1]
           return False, None, erros

## @brief Executa um executável para gerar um ficheiro PS2.
# @details Executa o programa externo indicado, enviando o ano e o mês via
# entrada padrão (stdin), e devolve o código de retorno e eventuais erros.
# @param caminho_exe Caminho para o executável responsável pela geração do PS2.
# @param ano Ano de referência.
# @param mes Mês de referência.
# @return (int, str) Código de retorno do processo e mensagem de erro (stderr).
def gerar_ficheiro_ps2(caminho_exe: str, ano: int, mes: int):
    entrada = f"{ano}\n{mes}\n"
    try:
        run = subprocess.run(
            [caminho_exe],
            input=entrada,
            text=True,
            capture_output=True)
    except Exception:
        pass
    
    stderr = run.stderr.strip()
    return run.returncode, stderr
