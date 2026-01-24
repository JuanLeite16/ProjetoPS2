from shiny import App, render, ui, reactive
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from styles import CSS
from processing import processar_ficheiros, mostrar_df
from utils import format_euro

# ----------------------------
# Interface do Utilizador (UI)
# ----------------------------
app_ui = ui.page_fluid(
    ui.tags.style(CSS),

    ui.tags.div([
        ui.tags.div([ui.h1("PS2 Dashboard", class_="title")], class_="header")
    ]),

    ui.layout_sidebar(
        ui.sidebar(
            ui.h3("Filtros"),
            ui.input_file("input_ficheiros", "Carregar Ficheiros (.ps2)", multiple=True, accept=[".ps2"]),
            ui.hr(),
            ui.h5("Seleção"),
            ui.input_select("seletor_periodo", "Período (Data)", choices=["Todos"]),
            ui.input_select("seletor_cliente", "Cliente (NIF)", choices=["Todos"]),
            ui.output_ui("status_upload"),
            width=300
        ),
        
        ui.tags.div(
            [
                ui.layout_columns(
                    ui.card(
                        ui.tags.div([ui.h3("Total € (Válidos)"), ui.tags.span("KPI", class_="badge")], class_="card-title"),
                        ui.output_ui("kpi_total_euros"),
                        class_="card"
                    ),
                    ui.card(
                        ui.tags.div([ui.h3("Registros"), ui.tags.span("KPI", class_="badge")], class_="card-title"),
                        ui.output_ui("kpi_num_registos"),
                        class_="card"
                    ),
                    ui.card(
                        ui.tags.div([ui.h3("Créditos"), ui.tags.span("KPI", class_="badge")], class_="card-title"),
                        ui.output_ui("kpi_creditos"),
                        class_="card"
                    ),
                    ui.card(
                        ui.tags.div([ui.h3("Débitos"), ui.tags.span("KPI", class_="badge")], class_="card-title"),
                        ui.output_ui("kpi_debitos"),
                        class_="card"
                    ),
                    col_widths=[3, 3, 3, 3],
                ),

                ui.br(),

                ui.layout_columns(
                    ui.card(
                        ui.tags.div([ui.h3("Info Ficheiro"), ui.tags.span("Resumo", class_="badge")], class_="card-title"),
                        ui.output_ui("cartao_cabecalho"),
                        class_="card"
                    ),
                     ui.card(
                        ui.tags.div([ui.h3("Gastos por Cliente"), ui.tags.span("Gráfico", class_="badge")], class_="card-title"),
                        ui.output_plot("grafico_gastos"),
                        class_="card"
                    ),
                    col_widths=[5, 7],
                ),

                ui.br(),

                ui.card(
                    ui.tags.div([ui.h3("Detalhes e Validação"), ui.tags.span("Tabela", class_="badge")], class_="card-title"),
                    ui.output_ui("contentor_tabela"),
                    class_="card",
                    style="width: 100%;"
                )
            ]
        )
    )
)


def server(input, output, session):
    diretorio_base = Path(__file__).parent.parent.parent
    caminho_default = diretorio_base / "data" / "1.ps2"
    
    try:
        ok, DF_default, erros = processar_ficheiros([caminho_default])
        if erros or not ok:
            DF_default = None
    except Exception:
        DF_default = None
                
    @reactive.Calc
    def obter_dados_atuais():
        lista_uploads = input.input_ficheiros()

        if not lista_uploads:
            if not DF_default:
                return []
            else:
                return [caminho_default]
        else:
            lista_ficheiros = []
            for i, ficheiro in enumerate(lista_uploads):
                caminho_temp = ficheiro.get("datapath") or ficheiro.get("path")
                lista_ficheiros.append(caminho_temp)
            ok, DFs, erros = processar_ficheiros(lista_ficheiros)
            if erros or not ok:
                for key, erro in erros.items():
                    try:
                        lista_ficheiros.remove(key)
                        print(erro)
                    except:
                        return None
                return lista_ficheiros
            else:
                return lista_ficheiros
            
            
    @reactive.Effect
    def atualizar_filtros():
        caminhos = obter_dados_atuais()
        trash1, DFs, trash2 = processar_ficheiros(caminhos)

        lista_periodos = sorted(set(DFs["resumo"]["cabecalho"]["Data"].astype(str)))
        ui.update_select("seletor_periodo", choices=["Todos"] + lista_periodos)

        lista_clientes = sorted(set(DFs["resumo"]["movimentos"]["NIF"].astype(str)))
        ui.update_select("seletor_cliente", choices=["Todos"] + lista_clientes)

    @reactive.Calc
    def df_filtrado():
        lista_paths = obter_dados_atuais()
        if not lista_paths:
            ui.notification_show(f"Todos arquivos corrompidos!")
            return None
        trash1, DFs, trash2 = processar_ficheiros(lista_paths)
        df_mov = DFs["resumo"]["movimentos"]

        if input.seletor_periodo() != "Todos":
            
            DFs["resumo"]["movimentos"] = df_mov[df_mov["Data"] == input.seletor_periodo()]
        
        if input.seletor_cliente() != "Todos":
            DFs["resumo"]["movimentos"] = df_mov[df_mov["NIF"] == str(input.seletor_cliente())]
        
        return DFs["resumo"]
    
    @output
    @render.ui
    def status_upload():
        uploads = input.input_ficheiros()
        if not uploads: return ui.p("Default carregado.", class_="muted")
        return ui.p(f"{len(uploads)} ficheiro(s) carregado(s).", class_="muted")
    
    @output
    @render.ui
    def kpi_total_euros():
        df_mov = df_filtrado()
        df = df_mov["movimentos"]
        linhas = df.to_string(index=False)
        total = 0.0
        if not df.empty:
            total = df.loc[df["Erros"] == "", "Valor"].sum()
            
        return ui.tags.div([
            ui.tags.div("TOTAL (Calculado)", class_="label"),
            ui.tags.div(format_euro(total), class_="value"),
            ui.tags.div("Apenas registos válidos", class_="hint"),
        ],class_="kpi"), 

    @output
    @render.ui
    def kpi_num_registos():
        df_mov = df_filtrado()
        df = df_mov["movimentos"]
        total_regs = len(df)
        qtd_invalidos = len(df[df["Erros"] != ""]) if not df.empty else 0
        
        msg_obs = f"{qtd_invalidos} registos com erro" if qtd_invalidos > 0 else "Todos válidos"
        estilo_cor = "color: red;" if qtd_invalidos > 0 else ""
        
        return ui.tags.div([
            ui.tags.div("REGISTOS", class_="label"),
            ui.tags.div(str(total_regs), class_="value"),
            ui.tags.div(msg_obs, class_="hint", style=estilo_cor),
        ], class_="kpi")

    @output
    @render.ui
    def kpi_creditos():
        df_mov = df_filtrado()
        df = df_mov["movimentos"]
        valor = (df["Tipo"].astype(str).str.lower() == "crédito").sum() if not df.empty else 0
        return ui.tags.div([ui.tags.div("CRÉDITOS", class_="label"), ui.tags.div(str(valor), class_="value")], class_="kpi")

    @output
    @render.ui
    def kpi_debitos():
        df_mov = df_filtrado()
        df = df_mov["movimentos"]
        valor = (df["Tipo"].astype(str).str.lower() == "débito").sum() if not df.empty else 0
        return ui.tags.div([ui.tags.div("DÉBITOS", class_="label"), ui.tags.div(str(valor), class_="value")], class_="kpi")

    @output
    @render.ui
    def cartao_cabecalho():
        df = df_filtrado()
        itens_mostrar = [
            ("Ficheiros", df["cabecalho"]["Ficheiro"].to_string(index=False)),
            ("Data(s)", df["cabecalho"]["Data"].to_string(index=False)),
            ("Entidade", df["cabecalho"]["Entidade"].to_string(index=False)),
            ("NIF Entidade", df["cabecalho"]["NIF"].to_string(index=False)),
        ]
        return ui.tags.div(
            [ui.tags.div([ui.tags.div(k, class_="k"), ui.tags.div(str(v), class_="v")], class_="info-row") for k, v in itens_mostrar],
            class_="info-grid"
        )

    @output
    @render.plot
    def grafico_gastos():
        df = df_filtrado()
        df_mov = df["movimentos"]
        figura, eixo = plt.subplots(figsize=(6, 3.3))
        
        if df_mov.empty:
            eixo.text(0.5, 0.5, "Sem dados", ha="center")
            eixo.axis("off")
            return figura
            
        df_validos = df_mov[df_mov["Erros"] == ""]
        if df_validos.empty:
            eixo.text(0.5, 0.5, "Sem dados válidos", ha="center")
            eixo.axis("off")
            return figura

        dados_agrupados = df_validos.groupby("NIF")["Valor"].sum().sort_values(ascending=False).head(10)
        eixo.bar(dados_agrupados.index, dados_agrupados.values, color="#1677FF")
        eixo.set_title("Top 10 Clientes (Por Gasto)")
        eixo.tick_params(axis='x', rotation=45)
        figura.tight_layout()
        return figura

    @output
    @render.ui
    def contentor_tabela():
        df = df_filtrado()
        df_mov = df["movimentos"]
        if df_mov.empty: return ui.p("Sem linhas.", class_="muted")
        return ui.tags.div(ui.output_table("tabela_principal"), class_="table-wrap")

    @output
    @render.table
    def tabela_principal():
        df = df_filtrado()
        df_mov = df["movimentos"]
        if df_mov.empty: return pd.DataFrame()
        
        colunas_ordem = ["Data", "NIF", "NIB", "Descrição", "Valor", "Tipo", "Erro"]
        colunas_finais = [c for c in colunas_ordem if c in df_mov.columns]
        
        if not colunas_finais: return df_mov.drop(columns=["Valor", "Ficheiro"], errors="ignore")
        return df_mov[colunas_finais]

app = App(app_ui, server)
