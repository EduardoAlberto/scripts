#######################################################
# Assunto: Extração dos dados do DEEZER SERVICO MUSICA
# Autor  : Eduardo Alberto
# Data   : 24/03/2021
#######################################################
import json, requests,http.client
from cassandra.query import SimpleStatement
import pandas as pd
import numpy as np
from cassandra.cluster import Cluster

# conexao cassandra
cluster = Cluster(['127.0.0.1'])
session = cluster.connect()

# variavel range
rg = 300 
# ##########################  
# API JSON DEEZER Radio  
# #########################
carga = []
for a in range(rg):
    id = a
    aut = {"x-rapidapi-key": "e0c50cc3cfmshf390077920d36b3p17667fjsn687dd8e32cb3"}
    response = requests.get("https://deezerdevs-deezer.p.rapidapi.com/radio/{}".format(id),headers=aut)
    arq = response.json()
    carga.append(arq)
    df = pd.json_normalize(carga)
    df = pd.DataFrame(df, columns=['id', 'title', 'description', 'share', 'picture', 'picture_small', 'picture_medium', 'picture_big', 'picture_xl', 'tracklist', 'md5_image', 'type'])
    
    # remove os NAN e formata o campo
    df['id'] = pd.to_numeric(df['id'], errors='coerce')
    df = df.dropna(subset=['id'])
    df['id'] = df['id'].astype(int)



# cria tabela no apache cassandra
session.execute("""
    create table if not exists dbcassandra.deezer_radio(
                 id                  int
                ,title              text
                ,description        text
                ,share              text
                ,picture            text
                ,picture_small      text
                ,picture_medium     text
                ,picture_big        text
                ,picture_xl         text
                ,tracklist          text
                ,md5_image          text
                ,type               text
                ,primary key(id)
                )with comment = 'tabelas com radios da Deezer';
""")


# cria insert
queryRadio = "insert into dbcassandra.deezer_radio( id, title, description, share, picture, picture_small, picture_medium, picture_big, picture_xl, tracklist, md5_image, type) \
              values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

# excuta a carga
prepared = session.prepare(queryRadio)
for index, carga in df.iterrows():
    session.execute(prepared
                   ,(carga['id']
                   , carga['title']
                   , carga['description']
                   , carga['share']
                   , carga['picture']
                   , carga['picture_small']
                   , carga['picture_medium']
                   , carga['picture_big']
                   , carga['picture_xl']
                   , carga['tracklist']
                   , carga['md5_image']
                   , carga['type'])
                   )

print(df)


