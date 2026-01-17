from parser import ler_ps2
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.colheader_justify', 'center')

dados = ler_ps2("../data/_.ps2")

cabecalho_df = pd.DataFrame([dados["cabecalho"]])
movimentos_df = pd.DataFrame(dados["movimentos"])
fecho_df = pd.DataFrame([dados["fecho"]])

print("\n", cabecalho_df.to_string(index=False), "\n")
print(fecho_df.to_string(index=False), "\n")

print(movimentos_df.to_string(index=False))
