## @file validations.py
#  @package validations
#  @brief Funções de validação e formatação de dados.
#  @details Contém funções para validação de NIF, NIB e ficheiros PS2,
#  bem como utilitários de formatação e acesso seguro a dados.

from pathlib import Path

## @brief Valida um NIF (Portugal) pelo algoritmo do dígito de controlo (módulo 11).
# @details Verifica se o NIF tem 9 dígitos numéricos e calcula o dígito de controlo
# para confirmar se o último dígito é válido.
# @param nif String com o NIF a validar.
# @return True se o NIF for válido, False caso contrário.
def validar_nif(nif):
    if not nif.isdigit() or len(nif) != 9:
        return False
    else:
        try:
            soma = sum([int(nif[i])*(9-i) for i in range(8)])
            resto = soma%11
            return True if (0 if resto <= 1 else 11 - resto) == int(nif[-1]) else False
        except Exception as e:
            print(f"Motivo de erro: {e}")
            return False

## @brief Valida um NIB (Portugal) pelo algoritmo módulo 97.
# @details Verifica se o NIB contém 21 dígitos numéricos e valida os dígitos
# de controlo através do cálculo módulo 97.
# @param nib String com o NIB a validar.
# @return True se o NIB for válido, False caso contrário.
def validar_nib(nib):
    if not nib.isdigit() or len(nib) != 21:
        return False

    iban = nib + "252950"
    return int(iban) % 97 == 1

## @brief Valida um ficheiro PS2.
# @details Verifica se o caminho fornecido corresponde a um ficheiro existente,
# regular, com extensão .ps2 e não vazio.
# @param ficheiro Caminho para o ficheiro PS2 a validar.
# @return Objeto Path correspondente ao ficheiro validado.
# @raises ValueError Se o ficheiro não for válido ou estiver vazio.
# @raises FileNotFoundError Se o ficheiro não existir.
def validar_ps2(ficheiro):
    if not ficheiro:
        raise ValueError("Nenhum ficheiro especificado.")
    p = Path(ficheiro)
    if not p.exists():
        raise FileNotFoundError("O ficheiro não existe.")
    if not p.is_file():
        raise ValueError("Não é um ficheiro.")
    if p.suffix.lower() != ".ps2":
        raise ValueError("Não é um ficheiro do tipo .ps2")
    if p.stat().st_size < 1:
        raise ValueError("Ficheiro vazio")
    
    return p

## @brief Verifica a existência de dados numa estrutura do tipo dicionário.
# @details Valida se a estrutura fornecida é um dicionário e tenta obter,
# de forma segura, o conteúdo associado à chave "movimentos".
# @param estrutura_dados Estrutura de dados a validar.
# @return Valor associado à chave "movimentos" ou lista vazia se não existir.
def validar_existencia_dados(estrutura_dados):
    if isinstance(estrutura_dados, dict):
        valor = obter_valor_seguro_dict(estrutura_dados, "movimentos", [])
        return valor

## @brief Obtém um valor de um DataFrame de forma segura.
# @details Tenta aceder ao valor da coluna e linha indicadas num DataFrame.
# Caso a coluna ou a linha não existam, devolve um valor padrão.
# @param df DataFrame de onde o valor será obtido.
# @param coluna Nome da coluna a aceder.
# @param linha Índice da linha (por defeito 0).
# @param valor_padrao Valor devolvido em caso de erro.
# @return Valor encontrado no DataFrame ou o valor padrão.
def obter_valor_seguro_df(df, coluna, linha=0, valor_padrao="—"):
    try:
        return df.at[linha, coluna]
    except (KeyError, IndexError):
        return valor_padrao

## @brief Obtém um valor de um dicionário de forma segura.
# @details Tenta obter o valor associado a uma chave num dicionário,
# devolvendo um valor padrão caso a chave não exista ou o valor seja inválido.
# @param estrutura_dados Dicionário de onde o valor será obtido.
# @param chave_desejada Chave a procurar no dicionário.
# @param valor_padrao Valor devolvido se a chave não existir ou for inválida.
# @return Valor associado à chave ou o valor padrão.
def obter_valor_seguro_dict(estrutura_dados, chave_desejada, valor_padrao="—"):
    if isinstance(estrutura_dados, dict):
        valor = estrutura_dados.get(chave_desejada, valor_padrao)
        return valor if valor not in (None, "") else valor_padrao
    
    return valor_padrao