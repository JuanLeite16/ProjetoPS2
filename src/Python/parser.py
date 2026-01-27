import datetime
from validations import validar_nif, validar_nib, validar_ps2, validar_existencia_dados
from utils import cent_to_euros, format_euro

def ler_ps2(path):
    try:
        p = validar_ps2(path)
    except Exception as e:
        return False, [path, f"Arquivo: {path}. Erro: {e}"]
    
    try:
        with open(p, "r", encoding="utf-8") as ficheiro:
            try:
                linhas_lista = [linha.rstrip("\r\n") for linha in ficheiro]
            except Exception as e:
                return False, [path, f"Arquivo: {path}. Erro: {e}"]
    except Exception as e:
        return False, [path, f"Arquivo: {path}. Erro: {e}"]

    dados_estruturados = {
        "cabecalho": {},
        "movimentos": [],
        "fecho": {}
    }
    entidade = data_formatada = "—"

    try:
        for pos, linha_atual in enumerate(linhas_lista, start=1):
            if not linha_atual:
                return False, [path, f"Arquivo: {p.name}. Erro: linha vazia na linha {pos}"]
            erros_dados = []
            tipo_registro = linha_atual[0]

            if tipo_registro == "1":
                if len(linha_atual) != 64:
                    raise ValueError(f"Linha {pos} de tamanho diferente para tipo 1.")
                data = linha_atual[1:9]
                entidade = linha_atual[9:35]
                nif_entidade = linha_atual[35:44]
                centimos = linha_atual[44:58]
                registros = linha_atual[58:64]

                euros = registro_int = None
                try:
                    data_formatada = datetime.datetime.strptime(data, "%Y%m%d").strftime("%d/%m/%Y")
                except:
                    erros_dados.append("DATA")
                    data_formatada = data
                try:
                    if not validar_nif(nif_entidade):
                        erros_dados.append("NIF")
                except:
                    erros_dados.append("NIF")
                try:
                    euros = float(cent_to_euros(centimos))
                except:
                    erros_dados.append("EUROS")
                try:
                    registro_int = int(registros)
                except:
                    erros_dados.append("REGISTROS")

                dados_estruturados["cabecalho"] = {
                    "Ficheiro": p.name,
                    "Data": data_formatada,
                    "Entidade": entidade.strip(),
                    "NIF": nif_entidade,
                    "Valor": euros,
                    "Registros": registro_int,
                    "Erros": ", ".join(erros_dados)
                }

            elif tipo_registro == "2":
                if len(linha_atual) != 82:
                    raise ValueError(f"Linha {pos} de tamanho diferente para tipo 2.")
                tipo_movimento = linha_atual[1:8]
                ordem_movimento = linha_atual[8:11]
                nib_cliente = linha_atual[11:32]
                nif_cliente = linha_atual[32:41]
                valor_pagar = linha_atual[41:55]
                descricao = linha_atual[55:74].strip()

                valor = None
                tipo_formatado = "Desconhecido"
                try:
                    tipo_formatado = tipo_movimento.lstrip("0")
                    tipo_formatado = "Crédito" if tipo_formatado == "1" else "Débito"
                except:
                    erros_dados.append("MOVIMENTO")
                try:
                    if not validar_nif(nif_cliente):
                        erros_dados.append("NIF")
                except:
                    erros_dados.append("NIF")
                try:
                    if not validar_nib(nib_cliente):
                        erros_dados.append("NIB")
                except:
                    erros_dados.append("NIB")
                try:
                    valor = float(cent_to_euros(valor_pagar))
                except:
                    erros_dados.append("VALOR")

                movimento_estruturado = {
                    "Tipo": tipo_formatado,
                    "Ordem": ordem_movimento,
                    "NIB": nib_cliente,
                    "NIF": nif_cliente,
                    "Valor": valor,
                    "Descrição": descricao,
                    "Data": data_formatada,
                    "Erros": ", ".join(erros_dados)
                }
                dados_estruturados["movimentos"].append(movimento_estruturado)

            elif tipo_registro == "9":
                if len(linha_atual) != 21:
                    raise ValueError(f"Linha {pos} de tamanho diferente para tipo 9.")
                total_cent = linha_atual[1:15]
                total_registros = linha_atual[15:]

                valor_total = total_reg_int = None
                try:
                    valor_total = float(cent_to_euros(total_cent))
                except:
                    erros_dados.append("VALOR TOTAL")
                try:
                    total_reg_int = int(total_registros)
                except:
                    erros_dados.append("TOTAL REGISTROS")

                dados_estruturados["fecho"] = {
                    "Valor_Total": valor_total,
                    "Total_Registros": total_reg_int,
                    "Erros": ", ".join(erros_dados)
                }

            else:
                raise ValueError(f"Arquivo corrompido na linha: {pos}")
    except Exception as e:
        return False, [path, f"Arquivo: {path}. Erro: {e}"]

    try:
        if validar_existencia_dados(dados_estruturados) == []:
            raise ValueError(f"Arquivo não tem movimentos.")
    except Exception as e:
        return False, [path, f"Arquivo: {path}. Erro: {e}"]
    
    return True, dados_estruturados
