#######################################################
# Assunto: Extração dos dados do DEEZER SERVICO MUSICA
# Autor  : Eduardo Alberto
# Data   : 11/04/2021
#######################################################
import json, requests
import pandas as pd
from cassandra.cluster import Cluster
from tqdm import tqdm
# conexao cassandra
cluster = Cluster(['127.0.0.1'])
session = cluster.connect()

# ##########################  
#  API JSON DEEZER ALBUM  
# #########################
album = []
for a in tqdm(range(500)):
    id = a
    aut = {"x-rapidapi-key": "e0c50cc3cfmshf390077920d36b3p17667fjsn687dd8e32cb3"}
    response = requests.get("https://deezerdevs-deezer.p.rapidapi.com/album/{}".format(id),headers=aut)
    arq = response.json()
    album.append(arq)
    df = pd.json_normalize(album)

print(df)