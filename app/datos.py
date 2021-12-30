import pandas as pd

class Datos:
    def __init__(self):
        self.ruta_programas = "scraper_siglas-uc/outputs/programas_clean.json"
        self.ruta_detalles = "scraper_siglas-uc/outputs/detalles_sp.json"

    def cargar(self):
        self.programas = pd.read_json(self.ruta_programas, orient = "table")
        self.detalles  = pd.read_json(self.ruta_detalles, orient = "table")