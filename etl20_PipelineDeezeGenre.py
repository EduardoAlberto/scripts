#######################################################
# Assunto: Extração dos dados do DEEZER SERVICO MUSICA
# Autor  : Eduardo Alberto
# Data   : 05/04/2021
#######################################################
import json, requests
import pandas as pd
from cassandra.cluster import Cluster
from tqdm import tqdm

# imports for sending email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

# conexao cassandra
cluster = Cluster(['127.0.0.1'])
session = cluster.connect()

# ##########################  
#  API JSON DEEZER GENRE  
# #########################
genre = []
for a in tqdm(range(300)):
    id = a
    aut = {"x-rapidapi-key": "e0c50cc3cfmshf390077920d36b3p17667fjsn687dd8e32cb3"}
    response = requests.get("https://deezerdevs-deezer.p.rapidapi.com/genre/{}".format(id),headers=aut)
    arq = response.json()
    genre.append(arq)
    df = pd.json_normalize(genre)
    df = pd.DataFrame(df, columns=['id', 'name', 'picture', 'picture_small', 'picture_medium', 'picture_big', 'picture_xl', 'type'])
    df['id'] = pd.to_numeric(df['id'], errors='coerce')
    df = df.dropna(subset=['id'])
    df['id'] = df['id'].astype(int)
    df['name'] = df['name'].astype(str)
    df['picture'] = df['picture'].astype(str)
    df['picture_small'] = df['picture_small'].astype(str)
    df['picture_medium'] = df['picture_medium'].astype(str)
    df['picture_big'] = df['picture_big'].astype(str)
    df['picture_xl'] = df['picture_xl'].astype(str)
    df['type'] = df['type'].astype(str)
 
  

session.execute("""
    create table if not exists dbcassandra.deezer_genre(
                 id                 int, 
                 name               text,
                 picture            text,
                 picture_small      text,
                 picture_medium     text,
                 picture_big        text,
                 picture_xl         text,
                 type               text,
                 primary key(id,name)
                 )with comment = 'tabelas com generos';
 """)
queryGenre = "insert into dbcassandra.deezer_genre(id, name, picture,  picture_small, picture_medium, picture_big, picture_xl, type) \
              values(?, ?, ?, ?, ?, ?, ?, ?)"

prepared = session.prepare(queryGenre)
for index, carga in df.iterrows():
    session.execute(prepared
                    ,( carga['id']
                      ,carga['name']
                      ,carga['picture']
                      ,carga['picture_small']
                      ,carga['picture_medium']
                      ,carga['picture_big']
                      ,carga['picture_xl']
                      ,carga['type'])
                    )

