import pandas as pd
from processing import processar_ficheiros

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.colheader_justify', 'center')
ficheiros = ["../data/1.ps2", "../data/2.ps2", "../data/3.ps2", "../data/4.ps2", "../data/5.ps2"]

DFs = processar_ficheiros(ficheiros)
print("="*120)
print(f"{'RESUMO FICHEIROS':^120}")
print("="*120)
texto_cab = DFs["resumo"]["cabecalho"].to_string(index=False)
for linha in texto_cab.splitlines():
    print(linha.center(120))
print("="*120)
print("RESUMO MOVIMENTOS".center(120))
print("="*120)
texto_mov = DFs["resumo"]["movimentos"].to_string(index=False)
for linha in texto_mov.splitlines():
    print(linha.center(120))
print("="*120)
print("RESUMO FECHO".center(120))
print("="*120)
texto_fec = DFs["resumo"]["fecho"].to_string(index=False)
for linha in texto_fec.splitlines():
    print(linha.center(120))

