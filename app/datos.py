import pandas as pd
import os

class Datos:
    def __init__(self):
        self.ruta_programas = os.path.join("scraper_siglas-uc", "outputs", "programas_clean.json")
        self.ruta_detalles  = os.path.join("scraper_siglas-uc", "outputs", "detalles_sp.json")

    def cargar(self):
        self.programas = pd.read_json(self.ruta_programas, orient = "table")
        self.detalles  = pd.read_json(self.ruta_detalles, orient = "table")