# Libraries

from selenium import webdriver
import json
import codecs
from time import sleep

# Import keys

with codecs.open("files/docs.json", "rU", "utf-8") as js:
    data = json.load(js)[0]

# Url generator

base_url = lambda ID: f"https://buscacursos.uc.cl/?cxml_semestre=2022-1&cxml_sigla=&cxml_nrc=&cxml_nombre=&cxml_categoria=TODOS&cxml_area_fg=TODOS&cxml_formato_cur=TODOS&cxml_profesor=&cxml_campus=TODOS&cxml_unidad_academica={ID}&cxml_horario_tipo_busqueda=si_tenga&cxml_horario_tipo_busqueda_actividad=TODOS#resultados"


# Init webdriver

options = webdriver.ChromeOptions()
options.add_argument("--incognito")
driver = webdriver.Chrome(executable_path="webdriver/chromedriver.exe", options=options)

# Scrape siglas

lista_detalles = list()

for esc, num in data.items():

    driver.get(base_url(num))
    sleep(5)

    siglas = driver.find_elements_by_xpath("//*[@id='wrapper']/div/div/div[3]/table/tbody/tr/td[2]/div")

    if len(siglas) > 0:

        formatos   = driver.find_elements_by_xpath("//*[@id='wrapper']/div/div/div[3]/table/tbody/tr/td[8]")[1:]
        nombres    = driver.find_elements_by_xpath("//*[@id='wrapper']/div/div/div[3]/table/tbody/tr/td[10]")[1:]
        profesores = driver.find_elements_by_xpath("//*[@id='wrapper']/div/div/div[3]/table/tbody/tr/td[11]/a[1]")
        campus     = driver.find_elements_by_xpath("//*[@id='wrapper']/div/div/div[3]/table/tbody/tr/td[12]")[1:]
        creditos   = driver.find_elements_by_xpath("//*[@id='wrapper']/div/div/div[3]/table/tbody/tr/td[13]")[1:]

        siglas     = [sigla.text for sigla in siglas]
        formatos   = [formato.text for formato in formatos]
        nombres    = [nombre.text for nombre in nombres]
        profesores = [profesor.text for profesor in profesores]
        campus     = [c.text for c in campus]
        escuelas   = [esc for i in range(len(siglas))]
        creditos   = [int(cred.text) for cred in creditos]
        
        lista_detalles += [{"escuela": escu, "campus": camp, "formato": formato, "sigla": sigla, "nombre": nombre, "creditos": cred, "docente": prof} for escu, camp, formato, sigla, nombre, cred, prof in zip(escuelas, campus, formatos, siglas, nombres, creditos, profesores)]

        print(lista_detalles[-len(siglas):])

# Close driver

driver.close()

# Save results

with codecs.open("outputs/detalles.json", "w", "utf-8") as js:
    json.dump(lista_detalles, js)