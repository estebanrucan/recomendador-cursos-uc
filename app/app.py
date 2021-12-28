# DEPENDENCIES

import streamlit as st

import numpy as np
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util
import json
import codecs
import plotly.express as px

import nltk
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Utils

tilde, sint = 'áéíóúÁÉÍÓÚ','aeiouAEIOU'
trans       = str.maketrans(tilde, sint)

# LOADS

base_url = lambda ID: f"https://catalogo.uc.cl/index.php?tmpl=component&option=com_catalogo&view=programa&sigla={ID}"


@st.cache(allow_output_mutation=True)
def data():
    with codecs.open("scraper_siglas-uc/outputs/menus.json", "rU", encoding = "utf-8") as archivo:
        menus = json.load(archivo)

    model    = SentenceTransformer("bert-base-nli-mean-tokens")
    embds    = torch.load("modelo/files/bert_de.tensor")
    data     = pd.read_json("scraper_siglas-uc/outputs/programas_clean.json", orient = "table")
    detalles = pd.read_json("scraper_siglas-uc/outputs/detalles_sp.json", orient = "table")
    return model, embds, data, detalles, menus

bert_model, documment_embs, data, detalles, menus = data()

# MAIN TITLE

st.title("Recomendador de Cursos UC")

st.markdown("""
*Hecho por Esteban Rucán*.

Esta aplicación entrega recomendaciones en base a la similitud de la consulta ingresada y los programas disponibles en el [Catálogo UC](https://catalogo.uc.cl/). 

**Actualizado al Primer Semestre de 2022**.
""")

# SIDERBAR

st.sidebar.title("Opciones")

## Consulta

st.sidebar.markdown("## Consulta")

consulta = st.sidebar.text_area(label = "", placeholder = "Por ejemplo: Portafolios de inversión")
consulta = consulta.translate(trans)
consulta = nltk.word_tokenize(consulta)
consulta = " ".join([palabra.lower() for palabra in consulta if palabra.isalpha()])

consulta_embs = bert_model.encode(consulta)
data["score"] = util.cos_sim(consulta_embs, documment_embs)[0]
datos_consulta = detalles.\
    merge(data, how = "right", on = ["escuela", "sigla"]).\
    sort_values("score", ascending = False).\
    iloc[:, [-1] + [0, 1, 2, 3, 4, 5]].\
    assign(score = lambda x: 100 * x.score).\
    rename({
        "score"   : "Similitud",
        "escuela" : "Escuela",
        "campus"  : "Campus",
        "formato" : "Formato",
        "sigla"   : "Sigla",
        "nombre"  : "Nombre",
        "creditos": "Créditos"
    }, axis = 1).\
    iloc[:, [0, 4, 5, 1, 2, 3, 6]].\
    assign(pos = np.arange(1, 3229)).\
    set_index("pos")

## Filtros

st.sidebar.markdown("""## Filtros""")

escuelas = st.sidebar.multiselect("Escuela", menus["escuelas"], )
campus   = st.sidebar.multiselect("Campus", menus["campus"])
formatos = st.sidebar.multiselect("Formato", menus["formato"])
top_n    = st.sidebar.slider("Top Recomendaciones", 4, 30, 10, 2)

# APP BODY

st.header("Recomendaciones")

data_show = datos_consulta.iloc[:top_n, :]
data_show["Similitud"] = np.round(data_show["Similitud"], 1).astype(str) + "%"

## Recomendaciones

if len(consulta) == 0:
    st.markdown("""
    Acá aparecerán recomendaciones cuando ingreses una consulta ¡Anímate!
    """)
elif data_show["Similitud"].unique().shape[0] == 1:
    st.markdown("""
    No hay recomendaciones para mostrar. Intenta con una nueva consulta o utiliza sinónimos.
    """)
else:
    if len(escuelas) == 0:
        pass
    else:
        data_show = data_show.query("Escuela in @escuelas")

    if len(campus) == 0:
        pass
    else:
        data_show = data_show.query("Campus in @campus")

    if len(formatos) == 0:
        pass
    else:
        data_show = data_show.query("Formato in @formatos")

    data_show["url"] = data_show["Sigla"].apply(lambda x: f"<a href={base_url(x)} target=\"_blank\">")
    data_show["Nombre"] = data_show["url"] + data_show["Nombre"].apply(lambda x: f"{x}</a>")
    data_show.drop(columns = "url", inplace = True)
    st.write(data_show.to_html(escape=False, index=False), unsafe_allow_html=True)

## Visualizaciones

st.header("Visualizaciones")

if len(consulta) == 0:
    st.markdown("""
    Acá aparecerán visualizaciones cuando ingreses una consulta ¡Anímate!
    """)
elif data_show["Similitud"].unique().shape[0] == 1:
    st.markdown("""
    No hay visualizaciones para mostrar. Intenta con una nueva consulta o utiliza sinónimos.
    """)
else:
    data_media = datos_consulta.iloc[:top_n, :].\
        groupby(["Escuela"]).\
        agg({"Similitud": "mean"}).\
        sort_values("Similitud", ascending=False)
    fig = px.bar(
        data_media,
        labels = {"value": "Porcentaje (%)"},
        title  = "Media de Similitud por Escuela"
    )
    fig.update_layout(showlegend = False)
    st.plotly_chart(fig)