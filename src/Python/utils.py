## @file utils.py
#  @package utils
#  @brief Módulo de utilitários genéricos.
#  @details Contém funções auxiliares para formatação de moeda, manipulação segura
#  dos dicionários e conversão das strings numéricas.

import os

## @brief Formata um valor numérico para o formato monetário em euros.
# @details Converte o valor para float e formata com duas casas decimais,
# usando vírgula como separador decimal e ponto para milhares.
# @param x Valor a formatar.
# @return String formatada em euros ou o valor original em caso de erro.
def format_euro(x):
    try:
        valor = f"€{float(x):,.2f}".replace(".", "X").replace(",", ".").replace("X", ",")
        return valor
    except:
        return x

## @brief Normaliza um valor numérico em formato string.
# @details Converte o valor removendo símbolos monetários e ajustando
# separadores decimais para o formato padrão (ponto).
# @param x Valor a normalizar.
# @return String com o valor normalizado ou o valor original em caso de erro.
def format_float(x):
    try:
        valor = str(x).replace(".", "").replace(",", ".").replace("€", "")
        return valor
    except:
        return x

## @brief Converte um valor em cêntimos para euros.
# @details Divide o valor em cêntimos por 100 e formata com duas casas decimais.
# @param cent Valor em cêntimos.
# @return String com o valor convertido para euros.
# @raises Exception Se ocorrer erro na conversão.
def cent_to_euros(cent):
    try:
        return f"{int(cent)/100:.2f}"
    except Exception as e:
        raise Exception(f"Erro: {e}")

## @brief Formata um NIF no formato legível.
# @details Aplica a formatação XXX.XXX.XXX ao NIF fornecido.
# @param nif String com o NIF a formatar.
# @return String com o NIF formatado ou o valor original em caso de erro.
def format_nif(nif):
    try:
        nif_ok = f"{nif[:3]}.{nif[3:6]}.{nif[6:]}"
        return nif_ok
    except:
        return nif

## @brief Formata um NIB no formato legível.
# @details Aplica espaçamento ao NIB para facilitar a leitura.
# @param nib String com o NIB a formatar.
# @return String com o NIB formatado ou o valor original em caso de erro.
def format_nib(nib):
    try:
        nib_ok = f"{nib[:4]} {nib[4:8]} {nib[8:19]} {nib[19:]}"
        return nib_ok
    except:
        return nib
    
## @brief Limpa o terminal/console.
# @details Executa o comando adequado ao sistema operativo para limpar
# o ecrã do terminal (Windows ou sistemas Unix-like).
def limpar_terminal():
    os.system("cls" if os.name == "nt" else "clear")