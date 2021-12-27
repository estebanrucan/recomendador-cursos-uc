import pandas as pd
from nltk import word_tokenize
from nltk.corpus import stopwords

tilde, sint = 'áéíóúÁÉÍÓÚ','aeiouAEIOU'
trans = str.maketrans(tilde, sint)

spanish_sw = stopwords.words("spanish")

programas = pd.read_csv("../scrapercatalogouc/outputs/programas.csv").query("description != 'Programa de curso no disponible'")

del_tilde  = programas["description"].str.translate(trans)
tokenize   = del_tilde.apply(lambda x: word_tokenize(x))
del_upper  = tokenize.apply(lambda lista: [palabra for palabra in lista if not palabra.isupper()])
tolower    = del_upper.apply(lambda lista: [palabra.lower() for palabra in lista if palabra.isalpha()])
del_sw     = tolower.apply(lambda lista: [palabra for palabra in lista if palabra not in spanish_sw + ["c"]])
join_list  = del_sw.apply(lambda x: " ".join(x) if len(x) > 3 else "") 

programas["programa"] = join_list
programas.drop(columns = "description", inplace = True)
programas = programas.query("programa != ''")

programas.to_json("outputs/programas_clean.json", orient = "table", index = False)