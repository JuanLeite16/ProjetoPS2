import sys
from parser import ler_ps2
import pandas as pd

ficheiros = sys.argv[1:]
lista = []

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.colheader_justify', 'center')

for ficheiro in ficheiros:
    dados = {}
    ok, info = ler_ps2(ficheiro)
    if ok:
        dados["cabecalho"] = pd.DataFrame([info["cabecalho"]])
        dados["movimentos"] = pd.DataFrame(info["movimentos"])
        dados["fecho"] = pd.DataFrame([info["fecho"]])
        lista.append(dados)
    else:
        print(info)

for df in lista:
    print(df["cabecalho"].to_string(index=False))
    print(df["movimentos"].to_string(index=False))
    print(df["fecho"].to_string(index=False), "\n")