import datetime
from validations import validar_nif, validar_nib

def ler_ps2(path):
    erros_programa = []
    try:
        with open(path, "r", encoding="utf-8") as ficheiro:
            try:
                linhas_lista = [linha.rstrip("\r\n") for linha in ficheiro]
            except :
                erros_programa.append("Impossível ler linhas do ficheiro")
    except FileNotFoundError:
        erros_programa.append("Ficheiro não encontrado.")

    dados_estruturados = {
        "cabecalho": {},
        "movimentos": [],
        "fecho": {},
        "erros": []
    }

    try:
        for pos, linha_atual in enumerate(linhas_lista, start=1):
            erros_dados = []
            tipo_registro = linha_atual[0]

            if tipo_registro == "1":
                data = linha_atual[1:9]
                entidade = linha_atual[9:35]
                nif_entidade = linha_atual[35:44]
                centimos = linha_atual[44:58]
                registros = linha_atual[58:64]

                euros = "—"
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
                    euros = f"{int(centimos)/100:.2f}"
                except:
                    erros_dados.append("EUROS")

                dados_estruturados["cabecalho"] = {
                    "Data": data_formatada,
                    "Entidade": entidade.strip(),
                    "NIF": nif_entidade,
                    "Valor": euros,
                    "Registros": registros.lstrip("0"),
                    "Erros": ", ".join(erros_dados)
                }

            elif tipo_registro == "2":
                tipo_movimento = linha_atual[1:8]
                ordem_movimento = linha_atual[8:11]
                nib_cliente = linha_atual[11:32]
                nif_cliente = linha_atual[32:41]
                valor_pagar = linha_atual[41:55]
                descricao = linha_atual[55:]

                valor = "—"
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
                    valor = f"{int(valor_pagar)/100:.2f}"
                except:
                    erros_dados.append("VALOR")

                movimento_estruturado = {
                    "Tipo": tipo_formatado,
                    "Ordem": ordem_movimento.lstrip("0"),
                    "NIB": nib_cliente,
                    "NIF": nif_cliente,
                    "Valor_Total": valor,
                    "Descrição": descricao,
                    "Erros": ", ".join(erros_dados)
                }
                dados_estruturados["movimentos"].append(movimento_estruturado)

            elif tipo_registro == "9":
                total_cent = linha_atual[1:15]
                total_registros = linha_atual[15:]

                valor_total = "—"
                try:
                    valor_total = f"{int(total_cent)/100:.2f}"
                except:
                    erros_dados.append("VALOR TOTAL")

                dados_estruturados["fecho"] = {
                    "Valor_Total": valor_total,
                    "Total_Registros": total_registros.lstrip("0"),
                    "Erros": ", ".join(erros_dados)
                }

            else:
                erros_programa.append(f"Tipo de registro corrompido na linha {pos}")
    except:
        erros_programa.append("Erro ao tentar ler linhas.")
    
    dados_estruturados["erros"].append(erros_programa)
    
    return dados_estruturados
