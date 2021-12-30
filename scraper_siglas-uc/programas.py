import pandas as pd
from nltk import word_tokenize
from nltk.corpus import stopwords

tilde, sint = 'áéíóúÁÉÍÓÚ','aeiouAEIOU'
trans = str.maketrans(tilde, sint)

spanish_sw = stopwords.words("spanish")

programas = pd.read_csv("scrapercatalogouc/outputs/programas.csv").query("description != 'Programa de curso no disponible'")
programas["description"] = programas["description"].str.replace("En este curso nos comprometemos con la Integridad Académica, reconociéndola como pilar fundamental del proceso formativo de nuestros estudiantes, para colaborar en la construcción de una cultura de respeto e integridad en la UC. Por tanto, las estrategias metodológicas y de evaluación, debiesen favorecer la promoción de los valores de honestidad, confianza, justicia, respeto y responsabilidad, así como el desarrollo de habilidades transversales para el aprendizaje.\nAdemás, para fortalecer esta cultura de respeto e integridad, este curso se adscribe y compromete con el Código de Honor UC:\n\nComo miembro de la comunidad de la Pontificia Universidad Católica de Chile, me comprometo a respetar los principios y normativas que la rigen. Asimismo, me comprometo a actuar con rectitud y honestidad en las relaciones con los demás integrantes de la comunidad y en la realización de todo trabajo, particularmente en aquellas actividades vinculadas a la docencia, al aprendizaje y la creación, difusión y transferencia del conocimiento. Además, me comprometo a velar por la dignidad e integridad de las personas, evitando incurrir en y, rechazando, toda conducta abusiva de carácter físico, verbal, psicológico y de violencia sexual. Del mismo modo, asumo el compromiso de cuidar los bienes de la Universidad", "")

del_tilde   = programas["description"].str.translate(trans)
tokenize    = del_tilde.apply(lambda x: word_tokenize(x))
del_noalpha = tokenize.apply(lambda lista: [palabra.replace("\x92", "").replace("\x93", "").replace("\x94", "") for palabra in lista])
del_upper   = del_noalpha.apply(lambda lista: [palabra for palabra in lista if not palabra.isupper()])
tolower     = del_upper.apply(lambda lista: [palabra.lower() for palabra in lista if palabra.isalpha()])
del_num     = tolower.apply(lambda lista: [palabra.strip("0123456789") for palabra in lista if palabra.isalpha()])
del_http    = del_num.apply(lambda lista: [palabra for palabra in lista if palabra != "http"])
del_sw      = del_http.apply(lambda lista: [palabra for palabra in lista if palabra not in spanish_sw])
join_list   = del_sw.apply(lambda x: " ".join(x) if len(x) > 3 else "")

programas["programa"] = join_list
programas.drop(columns = "description", inplace = True)
programas = programas.query("programa != ''")

programas.to_json("scraper_siglas-uc/outputs/programas_clean.json", orient = "table", index = False)