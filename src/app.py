from shiny import App, render, ui, reactive
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.sidebar(
            ui.h1("Filtros"),
            ui.input_file("input_ficheiros", "Carregar Ficheiros (.ps2)", multiple=True, accept=".ps2"),
            ui.input_date_range("seletor_periodo", "Período (Data)",min="2025-12-01", max="2025-12-31"),
            ui.input_selectize("seletor_ficheiro", "Ficheiro (.ps2)", multiple=True, choices=["1.ps1", "2.ps2", "3.ps2"]),
            ui.input_select("seletor_cliente", "Cliente (NIF)", multiple=True, choices=["311", "919", "524"]),
            ui.input_radio_buttons("teste", "Testando", choices=["Todos", "1", "Misss"])
        )
    )
)

def server(input, output, session):
    pass

app = App(app_ui, server)
