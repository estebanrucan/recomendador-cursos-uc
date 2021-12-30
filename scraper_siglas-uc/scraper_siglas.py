# Libraries

from selenium import webdriver
import json
import codecs
from time import sleep

# Import keys

with codecs.open("scraper_siglas-uc/files/docs.json", "rU", "utf-8") as js:
    data = json.load(js)[0]

# Url generator

base_url = lambda ID: f"https://buscacursos.uc.cl/?cxml_semestre=2022-1&cxml_sigla=&cxml_nrc=&cxml_nombre=&cxml_categoria=TODOS&cxml_area_fg=TODOS&cxml_formato_cur=TODOS&cxml_profesor=&cxml_campus=TODOS&cxml_unidad_academica={ID}&cxml_horario_tipo_busqueda=si_tenga&cxml_horario_tipo_busqueda_actividad=TODOS#resultados"


# Init webdriver

options = webdriver.ChromeOptions()
options.add_argument("--incognito")
driver = webdriver.Chrome(executable_path="scraper_siglas-uc/webdriver/chromedriver.exe", options=options)

# Scrape siglas

lista_siglas = dict()

for esc, num in data.items():

    driver.get(base_url(num))
    sleep(5)

    siglas = driver.find_elements_by_xpath("//*[@id='wrapper']/div/div/div[3]/table/tbody/tr/td[2]/div")
    lista_siglas[esc] = [sigla.text for sigla in siglas]

    print(esc, ":", [sigla.text for sigla in siglas])

# Close driver

driver.close()

# Save resuls

with codecs.open("scraper_siglas-uc/outputs/siglas.json", "w", "utf-8") as js:
    json.dump(lista_siglas, js)