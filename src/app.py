from shiny import App, render, ui, reactive
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

app_ui = ui.page_fluid(
    ui.h1("PS2 DASHBOARD")
)

def server(input, output, session):
    pass

app = App(app_ui, server)
