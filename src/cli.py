import sys
from parser import ler_ps2
import pandas as pd

ficheiros = sys.argv[1:]

for ficheiro in ficheiros:
    dicionario = ler_ps2(ficheiro)

print("ok")
