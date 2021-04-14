#######################################################
# Assunto: Extração dos dados do DEEZER SERVICO MUSICA
# Autor  : Eduardo Alberto
# Data   : 29/03/2021
#######################################################
import json, requests
import pandas as pd
from cassandra.cluster import Cluster
from tqdm import tqdm
# conexao cassandra
cluster = Cluster(['127.0.0.1'])
session = cluster.connect()


# ##########################  
#  API JSON DEEZER Playlist  
# #########################
track = []
for a in tqdm(range(300)):
    id = a
    aut = {"x-rapidapi-key": "e0c50cc3cfmshf390077920d36b3p17667fjsn687dd8e32cb3"}
    response = requests.get("https://deezerdevs-deezer.p.rapidapi.com/playlist/{}".format(id),headers=aut)
    arq = response.json()
    track.append(arq)
    df = pd.json_normalize(track)
    df = pd.DataFrame(df, columns=['id','title','description','duration','public','is_loved_track','collaborative','nb_tracks','fans','link','share','picture','picture_small','picture_medium','picture_big','picture_xl','checksum','tracklist','creation_date','md5_image','picture_type','creator.id','creator.name','creator.tracklist','creator.type','type','tracks.data','tracks.checksum'])
    df['id'] = pd.to_numeric(df['id'], errors='coerce')
    df = df.dropna(subset=['id'])
    df['id'] = df['id'].astype(int)
    df['duration'] = df['duration'].astype(int)
    df['nb_tracks'] = df['nb_tracks'].astype(int)
    df['fans'] = df['fans'].astype(int)
    df['creator.id'] = df['creator.id'].astype(int)
    df['creation_date'] = pd.to_datetime(df['creation_date'].astype(str))

    
    

session.execute("""
    create table if not exists dbcassandra.deezer_playlist(
                 id                 int
                ,title              text
                ,description        text
                ,duration           int
                ,public             boolean
                ,is_loved_track     boolean
                ,collaborative      boolean
                ,nb_tracks          int
                ,fans               int
                ,link               text    
                ,share              text
                ,picture            text
                ,picture_small      text
                ,picture_medium     text
                ,picture_big        text
                ,picture_xl         text
                ,checksum           text
                ,tracklist          text
                ,creation_date      timestamp
                ,md5_image          text
                ,picture_type       text
                ,creator_id         int
                ,creator_name       text
                ,creator_tracklist  text
                ,creator_type       text
                ,type               text
                ,tracks_checksum    text
                ,primary key(id)
                )with comment = 'tabelas com playlist da Deezer';
""")


queryPlaylist = " insert into dbcassandra.deezer_playlist(id,title,description,duration,public,is_loved_track,collaborative,nb_tracks,fans,link,share,picture,picture_small,picture_medium,picture_big,picture_xl,checksum,tracklist,creation_date,md5_image,picture_type,creator_id,creator_name,creator_tracklist,creator_type,type,tracks_checksum) \
                  values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

prepared = session.prepare(queryPlaylist)
for index, carga in df.iterrows():
    session.execute(prepared
                   ,( carga['id']
                     ,carga['title']
                     ,carga['description']
                     ,carga['duration']
                     ,carga['public']
                     ,carga['is_loved_track']
                     ,carga['collaborative']
                     ,carga['nb_tracks']
                     ,carga['fans']
                     ,carga['link']
                     ,carga['share']
                     ,carga['picture']
                     ,carga['picture_small']
                     ,carga['picture_medium']
                     ,carga['picture_big']
                     ,carga['picture_xl']
                     ,carga['checksum']
                     ,carga['tracklist']
                     ,carga['creation_date']
                     ,carga['md5_image']
                     ,carga['picture_type']
                     ,carga['creator.id']
                     ,carga['creator.name']
                     ,carga['creator.tracklist']
                     ,carga['creator.type']
                     ,carga['type']
                     ,carga['tracks.checksum'])
                     )

print(df[['creation_date','tracks.data']])




