from sentence_transformers import SentenceTransformer
import pandas as pd
import torch

programas = pd.read_json("scraper_siglas-uc/outputs/programas_clean.json", orient="table")
corpus = programas["programa"].to_list()

bert_model = SentenceTransformer("bert-base-nli-mean-tokens")
documment_embs = bert_model.encode(corpus, show_progress_bar=True, convert_to_tensor=True)

torch.save(documment_embs, "modelo/files/bert_de.tensor")