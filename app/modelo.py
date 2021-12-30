import numpy as np
from sentence_transformers import SentenceTransformer, util
import torch
import nltk

class Modelo:
    
    def __init__(self):
        self.ruta_modelo  = "bert-base-nli-mean-tokens"
        self.ruta_embs    = "modelo/files/bert_de.tensor"
        self.trans        = str.maketrans('áéíóúÁÉÍÓÚ','aeiouAEIOU')

    def cargar(self):
        # Load the model
        self.modelo = SentenceTransformer(self.ruta_modelo)
        self.embds  = torch.load(self.ruta_embs)

        # Load stopwords
        try:
            nltk.data.find("tokenizers/punkt")
            nltk.data.find("corpora/stopwords")
        except LookupError:
            nltk.download("punkt")
            nltk.download('stopwords')
        finally:
            self.stop_words = nltk.corpus.stopwords.words("spanish")


    def __limpiar_consulta(self, consulta):
        consulta = consulta.translate(self.trans)
        consulta = nltk.word_tokenize(consulta)
        consulta = [palabra.lower() for palabra in consulta if palabra.isalpha()]
        consulta = [palabra for palabra in consulta if palabra not in self.stop_words]
        return " ".join(consulta)

    def get_score(self, consulta, datos):
        consulta                 = self.__limpiar_consulta(consulta)
        consulta_embs            = self.modelo.encode(consulta)
        datos.programas["score"] = util.cos_sim(consulta_embs, self.embds)[0]

        self.datos_modelo = datos.detalles.\
            merge(datos.programas, how = "right", on = ["escuela", "sigla"]).\
            sort_values("score", ascending = False).\
            iloc[:, [-1, 0, 1, 2, 3, 4, 5]].\
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
            assign(pos = np.arange(1, 3229)).\
            set_index("pos")