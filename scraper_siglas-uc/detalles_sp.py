import pandas as pd
import os

detalles    = pd.read_json(os.path.join("scraper_siglas-uc", "outputs", "detalles.json"))
detalles_sp = detalles.drop(columns = "docente").drop_duplicates()

detalles_sp.to_json(os.path.join("scraper_siglas-uc", "outputs", "detalles_sp.json"), orient = "table", index = False)