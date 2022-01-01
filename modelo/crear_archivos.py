import os
import pandas as pd
from nltk import word_tokenize
import gensim

data = pd.read_json(os.path.join("scraper_siglas-uc", "outputs", "programas_clean.json"), orient="table")

programas   = data["programa"].apply(lambda x: word_tokenize(x)).to_list()
diccionario = gensim.corpora.Dictionary(programas)
corpus      = [diccionario.doc2bow(programa) for programa in programas]
model       = gensim.models.LsiModel(corpus, 203, diccionario)
index       = gensim.similarities.MatrixSimilarity(model[corpus])

index.save(os.path.join("modelo", "outputs", "index.index"))
diccionario.save(os.path.join("modelo", "outputs", "diccionario.dict"))
model.save(os.path.join("modelo", "outputs", "model.model"))