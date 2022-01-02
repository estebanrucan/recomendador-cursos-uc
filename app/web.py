import json
import codecs
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import os

class Web:

    def __init__(self):
        self.ruta_menus = os.path.join("scraper_siglas-uc", "outputs", "menus.json")
        self.min_rec    = 4
        self.max_rec    = 30
        self.step_rec   = 2

        # Valores por defecto

        self.sel_escuelas = list()
        self.sel_campus   = list()
        self.sel_formatos = list()
        self.sel_recomend = 10

    def cargar(self):
        with codecs.open(self.ruta_menus, "rU", encoding = "utf-8") as archivo:
            menus = json.load(archivo) 
            self.escuelas = menus["escuelas"]
            self.campus   = menus["campus"]
            self.formatos = menus["formato"]
            del menus       

    def base_url(self, sigla):
        return f"https://catalogo.uc.cl/index.php?tmpl=component&option=com_catalogo&view=programa&sigla={sigla}"

    def __datos_a_html(self, datos):
        datos["url"]    = datos["Sigla"].apply(lambda x: f"<a href={self.base_url(x)} target=\"_blank\">")
        datos["Nombre"] = datos["url"] + datos["Nombre"].apply(lambda x: f"{x}</a>")
        datos.drop(columns = "url", inplace = True)
        fig = go.Figure(
            data = [go.Table(
                header = dict(values = list(datos.columns)),
                cells = dict(
                    values = [datos["Similitud"], datos["Sigla"], datos["Nombre"], datos["Escuela"], datos["Campus"], datos["Formato"], datos["Créditos"]]
                )
            )]
        )
        return fig

    def __crear_grafico(self, datos):
        data_media = datos.\
            groupby(["Escuela"]).\
            agg({"Similitud": "mean"}).\
            sort_values("Similitud", ascending = False)
        fig = px.bar(
            data_media,
            labels = {"value": "Porcentaje (%)"},
            title  = "Media de Similitud por Escuela"
        )
        fig.update_layout(showlegend = False)
        return fig

    def mostrar_objeto(self, modelo, tipo = "datos"):
        data_show = modelo.datos_modelo.copy()

        if len(self.consulta) == 0:
            st.markdown(f"""
            Acá aparecerán {"recomendaciones" if tipo == "datos" else "visualizaciones"} cuando ingreses una consulta ¡Anímate!
            """)
        elif modelo.datos_modelo["Similitud"].unique().shape[0] == 1:
            st.markdown(f"""
            No hay {"recomendaciones" if tipo == "datos" else "visualizaciones"} para mostrar. Intenta con una nueva consulta o utiliza sinónimos.
            """)
        else:
            if tipo == "datos":
                if len(self.sel_escuelas) != 0:
                    data_show = data_show.query("Escuela in @self.sel_escuelas")
                if len(self.sel_campus) != 0:
                    data_show = data_show.query("Campus in @self.sel_campus")
                if len(self.sel_formatos) != 0:
                    data_show = data_show.query("Formato in @self.sel_formatos")
                data_show["Similitud"] = np.round(data_show["Similitud"], 1).astype(str) + "%"
                data_show = self.__datos_a_html(data_show)
                return st.plotly_chart(data_show.iloc[:self.sel_recomend, :])
            else:
                fig = self.__crear_grafico(data_show)
                return st.plotly_chart(fig)