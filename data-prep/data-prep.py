
import pandas as pd

# Requisitos
requisitos = pd.read_json("scrapercatalogouc/outputs/requisitos.json")
requisitos = requisitos.rename({
    "Prerrequisitos": "prerrequisitos",
    "Relación entre prerrequisitos y restricciones": "relacion_prerreq_rest",
    "Restricciones": "restricciones",
    "Equivalencias": "equivalencias"
}, axis = 1)
requisitos.to_csv("data-prep/outputs/requisitos.csv")

# Normalizar docentes
detalles = pd.read_json("scraper_siglas-uc/outputs/detalles.json")
detalles["docente"] = detalles["docente"].str.split(",\n")
largo = detalles["docente"].apply(lambda x: len(x))
faltante = largo.apply(lambda x: 25 - x)
espacios = [['' for _ in range(num)] for num in faltante]
lista_doc = (detalles["docente"] + pd.Series(espacios)).to_list()
data_concat = pd.concat([detalles.drop(columns="docente"), pd.DataFrame(lista_doc)], axis = 1)
data_concat = data_concat.melt(value_vars = [i for i in range(25)], value_name = "docente", id_vars=data_concat.columns[:7])
detalles = data_concat.query("docente != ''").sort_values(["escuela", "sigla", "seccion"])
detalles = detalles.reset_index().drop(columns = ["index", "variable"])

# Escuelas
escuelas = detalles.drop_duplicates("escuela")[["escuela"]].assign(id = range(1, 46)).iloc[:, [1, 0]].rename({"escuela": "nombre"}, axis = 1)
escuelas.to_csv("data-prep/outputs/escuelas.csv", index=False)

detalles = detalles.merge(escuelas, how = "left", left_on= "escuela", right_on="nombre").drop(columns = ["escuela", "nombre_y"]).rename(columns = {"id": "escuela_id"})

# Formatos
formatos = detalles.drop_duplicates("formato")[["formato"]].assign(id = range(1, 5)).iloc[:, [1, 0]].rename({"formato": "tipo"}, axis = 1)
formatos.to_csv("data-prep/outputs/formatos.csv", index=False)
detalles = detalles.merge(formatos, how="left", left_on="formato", right_on="tipo").drop(columns = ["tipo", "formato"]).rename({"id": "formato_id"}, axis = 1)

# Campus
campus = detalles.drop_duplicates("campus")[["campus"]].assign(id = range(1, 7)).iloc[:, [1, 0]].rename({"campus": "nombre"}, axis = 1)
campus.to_csv("data-prep/outputs/campus.csv", index=False)
detalles = detalles.merge(campus, how="left", left_on="campus", right_on="nombre").drop(columns = ["campus", "nombre"]).rename({"id": "campus_id", "sigla": "curso_id"}, axis = 1)

# Docentes
docentes = detalles.drop_duplicates("docente")[["docente"]].assign(id = range(1, 2969)).iloc[:, [1, 0]].rename({"docente": "nombre"}, axis = 1)
docentes.to_csv("data-prep/outputs/docentes.csv", index=False)

detalles = detalles.merge(docentes, how="left", left_on="docente", right_on="nombre").drop(columns = ["docente", "nombre"]).rename({"id": "docente_id", "sigla": "curso_id"}, axis = 1)

detalles = detalles.rename({"nombre_x": "nombre"}, axis = 1)
detalles.to_csv("data-prep/outputs/detalles.csv", index = False)

# Programas, módulos, carácter, curso 
cursos = detalles[["curso_id", "nombre", "creditos", "seccion"]]
secciones = cursos.drop_duplicates(["curso_id", "seccion"]).groupby(["curso_id"]).agg({"curso_id": "count"}).rename({"curso_id": "nro_secciones"}, axis = 1).reset_index()
cursos = cursos.drop(columns="seccion").drop_duplicates(["curso_id", "nombre", "creditos"]).merge(secciones, on = "curso_id")
programas = pd.read_json("scrapercatalogouc/outputs/programas.json").query("description != 'Programa de curso no disponible'")
programas.columns = ["curso_id", "programa"]
programas["módulos"] = programas["programa"].str.extract("MÓDULOS:\s{0,50}(.+)\n")[0]
programas["carácter"] = programas["programa"].str.extract("CARÁCTER:\s{0,50}(.+)\n")[0].str.title()
cursos = cursos.merge(programas, on="curso_id", how="right").rename({"curso_id": "id", "creditos": "créditos"}, axis = 1)
cursos.to_csv("data-prep/outputs/cursos.csv", index = False)


