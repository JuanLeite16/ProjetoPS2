import pandas as pd
from processing import processar_ficheiros, mostrar_df

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.colheader_justify', 'center')
ficheiros = ["../data/1.ps2", "../data/2.ps2", "../data/3.ps2", "../data/4.ps2", "../data/5.ps2"]

ok, DFs = processar_ficheiros(ficheiros)
if ok:
    mostrar_df(DFs["1.ps2"])
if not ok:
    for pos, erro in enumerate(DFs, start=1):
        print(f"{pos}° => {erro}")
