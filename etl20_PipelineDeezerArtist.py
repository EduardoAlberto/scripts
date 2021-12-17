#######################################################
# Assunto: Extração dos dados do DEEZER SERVICO MUSICA
# Autor  : Eduardo Alberto
# Data   : 10/04/2021
#######################################################
import json, requests
import datetime
import pandas as pd
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from tqdm import tqdm
import smtplib

# conexao cassandra
cluster = Cluster(['127.0.0.1'])
session = cluster.connect()

# ##########################  
#  API JSON DEEZER ARTISTA  
# ##########################
artist = []
for a in tqdm(range(500)):
    id = a
    aut = {"x-rapidapi-key": "e0c50cc3cfmshf390077920d36b3p17667fjsn687dd8e32cb3"}
    response = requests.get("https://deezerdevs-deezer.p.rapidapi.com/artist/{}".format(id),headers=aut)
    arq = response.json()
    artist.append(arq)
    df = pd.json_normalize(artist)
    df = pd.DataFrame(df, columns=['id', 'name', 'link', 'share', 'picture', 'picture_small', 'picture_medium', 'picture_big', 'picture_xl', 'nb_album', 'nb_fan', 'radio', 'tracklist', 'type'])
    df = df.dropna(subset=['id'])
    df['id'] = pd.to_numeric(df['id'])
    df['nb_album'] = pd.to_numeric(df['nb_album'])
    df['nb_fan'] = pd.to_numeric(df['nb_fan'])
    df['id'] = df['id'].astype(int)
    df['nb_album'] = df['nb_album'].astype(int)
    df['nb_fan'] = df['nb_fan'].astype(int)
    df['name'] = df['name'].astype(str)
    df['link'] = df['link'].astype(str)
    df['share'] = df['share'].astype(str)
    df['picture'] = df['picture'].astype(str)
    df['picture_small'] = df['picture_small'].astype(str)
    df['picture_medium'] = df['picture_medium'].astype(str)
    df['picture_big'] = df['picture_big'].astype(str)
    df['picture_xl'] = df['picture_xl'].astype(str)
    df['radio'] = df['radio'].astype(str)
    df['tracklist'] = df['tracklist'].astype(str)
    df['type'] = df['type'].astype(str)


session.execute("""
        create table if not exists dbcassandra.deezer_artist(
             id                 int
            ,name               text
            ,link               text
            ,share              text
            ,picture            text
            ,picture_small      text
            ,picture_medium     text
            ,picture_big        text
            ,picture_xl         text
            ,nb_album           int
            ,nb_fan             int
            ,radio              text
            ,tracklist          text
            ,type               text
            ,primary key(id, name)
            )with comment = 'tabelas com artistas'
""")
queryArtist = "insert into dbcassandra.deezer_artist(id, name, link, share, picture, picture_small, picture_medium, picture_big, picture_xl, nb_album, nb_fan, radio, tracklist, type) \
               values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
 

prepared = session.prepare(queryArtist)
for index, carga in df.iterrows():
    session.execute(prepared
                    ,( carga['id']
                      ,carga['name']
                      ,carga['link']
                      ,carga['share']
                      ,carga['picture']
                      ,carga['picture_small']
                      ,carga['picture_medium']
                      ,carga['picture_big']
                      ,carga['picture_xl']
                      ,carga['nb_album']
                      ,carga['nb_fan']
                      ,carga['radio']
                      ,carga['tracklist']
                      ,carga['type'])
                    )

# varias consultas 
consulta = session.execute("select id, name, nb_fan, radio, tracklist,type from dbcassandra.deezer_artist where nb_fan >=6080077 ALLOW FILTERING;")
query = []
for row in consulta:
  row[0:]
  query.append(row)
df = pd.DataFrame(query) 
print(df)



 