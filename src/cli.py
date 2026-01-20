import sys
import pandas as pd
from pathlib import Path
import questionary
from processing import mostrar_df, processar_ficheiros
from validations import validar_ps2
from utils import limpar_terminal

ficheiros = sys.argv[1:]

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.colheader_justify', 'center')

if not ficheiros:
    raise ValueError("\033[1;31mPROGRAMA MAL EXECUTADO. ACESSE O README PARA MAIS INFORMAÇÕES.\033[m")

ficheiros = sorted(set(str(f) for f in ficheiros))
ok, DFs = processar_ficheiros(ficheiros)
if ok:
    while True:
        opcao = questionary.select(
            "Escolha uma opção:",
            choices=[
                "1) Mostrar resumo de todos os ficheiros.",
                "2) Mostrar ficheiro específico.",
                "3) Acrescentar ficheiro.",
                "4) Remover ficheiro.",
                "5) Sair."
            ],
        ).ask()

        match opcao:
            case "1) Mostrar resumo de todos os ficheiros.":
                limpar_terminal()
                if ficheiros == []:
                    print("\033[1;33mNão há ficheiros. Use a opção 3 para acrescentar.\033[m")
                else:
                    ok, DFs = processar_ficheiros(ficheiros)
                    if ok:
                        mostrar_df(DFs["resumo"])
                    else:
                        for i, erro in enumerate(DFs):
                            print(f"\033[1;31m{i}° => {e}\033[m")
            case "2) Mostrar ficheiro específico.":
                limpar_terminal()
                if ficheiros == []:
                    print("\033[1;33mNão há ficheiros. Use a opção 3 para acrescentar.\033[m")
                else:
                    keys = questionary.checkbox(
                        "Escolha um ou mais ficheiros. (ESPAÇO marca / ENTER confirma):",
                        choices=[
                            str(ficheiro) for ficheiro in ficheiros
                        ],
                    ).ask()
                    if len(keys) > 1:
                        ok, DFs_especifico = processar_ficheiros(keys)
                        if ok:
                            mostrar_df(DFs_especifico["resumo"])
                        else:  
                            for i, erro in enumerate(DFs_especifico):
                                print(f"\033[1;31m{i}° => {erro}\033[m")
                    elif len(keys) == 1:
                        mostrar_df(DFs[Path(keys[0]).name])
            case "3) Acrescentar ficheiro.":
                limpar_terminal()
                while True:
                    resp = str(input("\033[1;33mInforme o caminho do ficheiro. (0 para sair): \033[m"))
                    if resp == "0":
                        break
                    try:
                        file = validar_ps2(resp)
                        ficheiros.append(file)
                    except Exception as e:
                        print(f"\033[1;31mERRO: {e}\033[m")
                if not ficheiros == []:
                    ficheiros = sorted(set(str(f) for f in ficheiros))
                    ok, DFs = processar_ficheiros(ficheiros)
                    if ok:
                        continue
                    else:
                        for i, erro in enumerate(DFs):
                            print(f"\033[1;31m{i}° => {erro}\033[m")
                        break
            case "4) Remover ficheiro.":
                limpar_terminal()
                if ficheiros == []:
                    print("\033[1;33mNão há ficheiros. Use a opção 3 para acrescentar.\033[m")
                else:
                    resp = questionary.checkbox(
                        "Escolha um ou mais ficheiros. (ESPAÇO marca / ENTER confirma):",
                        choices=[
                            str(f) for f in ficheiros
                        ]
                    ).ask()
                    for x in resp:
                        try:
                            ficheiros.remove(x)
                        except Exception as e:
                            print(f"\033[1;31mERRO: {e}\033[m")
                    ficheiros = sorted(set(str(f) for f in ficheiros))
            case "5) Sair.":
                limpar_terminal()
                print("\033[1;32mSaindo...\033[m")
                break
else:
    for i, erro in enumerate(DFs):
        print(f"\033[1;31m{i}° => {erro}\033[m")