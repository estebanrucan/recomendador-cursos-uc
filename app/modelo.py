import numpy as np
import gensim
import nltk
import os

class Modelo:
    
    def __init__(self):
        self.ruta_modelo  = os.path.join("modelo", "outputs", "model.model")
        self.ruta_index   = os.path.join("modelo", "outputs", "index.index")
        self.ruta_diccio  = os.path.join("modelo", "outputs", "diccionario.dict")
        self.trans        = str.maketrans('áéíóúÁÉÍÓÚ','aeiouAEIOU')

    def cargar(self):
        # Load the model
        self.modelo      = gensim.models.LsiModel.load(self.ruta_modelo)
        self.index       = gensim.similarities.MatrixSimilarity.load(self.ruta_index)
        self.diccionario = gensim.corpora.Dictionary.load(self.ruta_diccio)

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
        return consulta

    def get_score(self, consulta, datos):
        consulta                 = self.__limpiar_consulta(consulta)
        consulta_bow             = self.diccionario.doc2bow(consulta)
        datos.programas["score"] = self.index[self.modelo[consulta_bow]]

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