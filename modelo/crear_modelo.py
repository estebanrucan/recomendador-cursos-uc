import numpy as np
import pandas as pd
from nltk import word_tokenize
import nltk
import gensim
import pickle

sw = nltk.corpus.stopwords.words("spanish")
with open("files/stopwords.pkl", "wb") as file:
    pickle.dump(sw, file)

detalles = pd.read_json("../scraper_siglas-uc/outputs/detalles.json")
det = detalles.drop(columns = "docente").drop_duplicates() 

det.to_json("../scraper_siglas-uc/outputs/detalles_sp.json", orient = "table", index = False)

data = pd.read_json("../scraper_siglas-uc/outputs/programas_clean.json", orient="table")

programas   = data["programa"].apply(lambda x: word_tokenize(x)).to_list()
diccionario = gensim.corpora.Dictionary(programas)
corpus      = [diccionario.doc2bow(programa) for programa in programas]
model       = gensim.models.LsiModel(corpus, 180, diccionario)
index       = gensim.similarities.MatrixSimilarity(model[corpus])
data.drop(columns = "programa", inplace = True)
index.save('files/index.index')
diccionario.save("files/diccionario.dict")

model.save("files/model.model")
gensim.corpora.MmCorpus.serialize("files/bow_corpus.mm", corpus)