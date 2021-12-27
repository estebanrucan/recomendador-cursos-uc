# DEPENDENCIES


import streamlit as st
import numpy as np
import pandas as pd
import gensim
import json
import codecs
import plotly.express as px

import nltk
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# LOADS

## Menus

with codecs.open("scraper_siglas-uc/outputs/menus.json", "rU", encoding = "utf-8") as archivo:
    menus = json.load(archivo)

## Data

data     = pd.read_json("scraper_siglas-uc/outputs/programas_clean.json", orient = "table")
detalles = pd.read_json("scraper_siglas-uc/outputs/detalles_sp.json", orient = "table")

## Model

model       = gensim.models.LsiModel.load("modelo/files/model.model")
index       = gensim.similarities.MatrixSimilarity.load("modelo/files/index.index")
diccionario = gensim.corpora.Dictionary.load("modelo/files/diccionario.dict")
stopwords   = pd.read_pickle("modelo/files/stopwords.pkl")
tilde, sint = 'áéíóúÁÉÍÓÚ','aeiouAEIOU'
trans       = str.maketrans(tilde, sint)

# MAIN TITLE

st.title("Recomendador de Cursos UC")

st.markdown("""
*Hecho por Esteban Rucán*.

Esta aplicación entrega recomendaciones en base a la similitud de la consulta ingresada y los programas disponibles en el [Catálogo UC](https://catalogo.uc.cl/). Actualizado al Primer Semestre de 2022.
""")

# SIDERBAR

st.sidebar.title("Opciones")

## Consulta

st.sidebar.markdown("## Consulta")

consulta = st.sidebar.text_area(label = "", placeholder = "Por ejemplo: Portafolios de inversión")
consulta = consulta.translate(trans)
consulta = nltk.word_tokenize(consulta)
consulta = [palabra.lower() for palabra in consulta if palabra.isalpha()]
consulta = [palabra for palabra in consulta if palabra not in stopwords]

consulta_bow   = diccionario.doc2bow(consulta)
data["score"]  = index[model[consulta_bow]]
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
    assign(pos = np.arange(1, 1080, 1)).\
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
    No hay recomendaciones para mostrar.
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

    st.dataframe(data_show)

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