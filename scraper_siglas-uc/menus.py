import json
import codecs
import pandas as pd

prog = pd.read_json("scraper_siglas-uc/outputs/detalles.json")

escuelas = [e for e in prog.escuela.unique()]
campus   = [e for e in prog.campus.unique()]
formato  = [e for e in prog.formato.unique()]

diccionario = {
    "escuelas": escuelas,
    "campus"  : campus,
    "formato" : formato
}

with codecs.open("scraper_siglas-uc/outputs/menus.json", "w", "utf-8") as file:
    json.dump(diccionario, file)