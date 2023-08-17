# DEPENDENCIES

import streamlit as st
from datos import Datos
from modelo import Modelo
from web import Web

# LOADS

@st.cache(allow_output_mutation=True)
def loads():
    objetos = (Datos(), Modelo(), Web())
    for objeto in objetos:
        objeto.cargar()
    return objetos
datos, modelo, web = loads()

# SIDERBAR

st.sidebar.title("Opciones")

## Consulta

st.sidebar.markdown("## Consulta")

web.consulta = st.sidebar.text_area(label = "", placeholder = "Por ejemplo: Portafolios de inversión")

modelo.get_score(web.consulta, datos)

## Filtros

st.sidebar.markdown("""## Filtros""")

web.sel_escuelas = st.sidebar.multiselect("Escuela", web.escuelas, web.sel_escuelas)
web.sel_campus   = st.sidebar.multiselect("Campus", web.campus, web.sel_campus)
web.sel_formatos = st.sidebar.multiselect("Formato", web.formatos, web.sel_formatos)
web.sel_recomend = st.sidebar.slider("Top Recomendaciones", web.min_rec, web.max_rec, web.sel_recomend, web.step_rec)

# APP BODY

## Tíyulo
st.title("Recomendador de Cursos UC")

st.markdown("""
*Actualizado al Primer Semestre de 2023. Hecho por Esteban Rucán.*

Esta aplicación entrega recomendaciones en base a la similitud de la consulta ingresada y los programas disponibles en el [Catálogo UC](https://catalogo.uc.cl/).
""")

## Recomendaciones

st.header("Recomendaciones")

web.mostrar_objeto(modelo)

## Visualizaciones

st.header("Visualizaciones")

web.mostrar_objeto(modelo, tipo = "grafico")