# acessar https://apps.twitter.com para criar uma nova aplicação
# cada aplicação tem suas próprias chaves
import tweepy 
import datetime as dt
import pandas as pd
import random as rd
import os 
from cassandra.cluster import Cluster
import zipfile as zp



# diretorio saida
data_carga = str(dt.date.today()).replace('-','')

# chaves de conexão com twitter 
tolken = open('cript.txt', 'r')

consumer_key = []
consumer_secret = []
access_token = []
access_token_secret = []

# chaves de conexão com twitter 
for linha, tolken in enumerate(tolken):
    if linha == 0:
        consumer_key = tolken.replace("'",'').strip()
    if linha == 1:
        consumer_secret = tolken.replace("'",'').strip()
    if linha == 2:
        access_token = tolken.replace("'",'').strip()
    if linha == 3:
        access_token_secret = tolken.replace("'",'').strip()

aut = tweepy.OAuthHandler(consumer_key, consumer_secret)
aut.set_access_token(access_token, access_token_secret )

twitter = tweepy.API(aut)


def arq(pesquisa):
       # palavra que iremos procurar
       resultado = twitter.search(pesquisa)
       table = []
       for tweet in resultado:
              
              tbl = [
                     tweet.user.screen_name,
                     tweet.user.location,
                     tweet.user.friends_count,
                     tweet.user.followers_count,
                     tweet.user.listed_count,
                     tweet.user.favourites_count,
                     tweet.user.verified,
                     tweet.user.statuses_count,
                     tweet.retweet_count,
                     tweet.text
              ]
              table.append(tbl)
       return table

# pesquisa palavra no twitter
# palavra = arq(input())
pesquisa = input('Digite uma palavra: ')
palavra = arq(pesquisa)
txt = pd.DataFrame(palavra, columns=['usuario','localizacao','total_amigos','total_seguidores','total_listas','total_likes','status_verificado','total_status','total_retweet','tweet'])
txt['localizacao'].replace({'\u0000', 'sem_localizacao'},inplace =True)

# conexao com o banco
cluster = Cluster(['127.0.0.1'])
session = cluster.connect()

def acessa_banco(palavra):
       session.execute("""CREATE KEYSPACE IF NOT EXISTS %s WITH replication = {'class': 'SimpleStrategy', 'replication_factor' :'1' }"""% palavra)
       session.set_keyspace(palavra)
       session.execute("""
              create table if not exists tmp_{}(
                      user_id           uuid  
                     ,usuario           text
                     ,localizacao       text
                     ,total_amigos      int 
                     ,total_seguidores  int 
                     ,total_listas      int         
                     ,total_likes       int          
                     ,status_verificado boolean
                     ,total_status      int  
                     ,total_retweet     int  
                     ,tweet             text
                     ,dt_load           TIMESTAMP  
                     ,PRIMARY KEY(user_id, usuario)       
              ) WITH comment='Informacao dos twitter mais pesquisados';
       """.format(palavra) 
       )

       # insert da tabela 
       query = "insert into tmp_{} (user_id, usuario, localizacao, total_amigos, total_seguidores, total_listas, total_likes, status_verificado, total_status, total_retweet, tweet,dt_load ) \
       values (now(), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,dateOf(now()))".format(palavra)
               
       prepared = session.prepare(query)
       for index, row in txt.iterrows():
              session.execute(prepared
                             ,(row['usuario']
                             , row['localizacao']
                             , row['total_amigos']
                             , row['total_seguidores']
                             , row['total_listas']
                             , row['total_likes']
                             , row['status_verificado']
                             , row['total_status']
                             , row['total_retweet']
                             , row['tweet'])
                             )
       row = session.execute('select * from tmp_{}'.format(palavra))  
       gera_csv = pd.DataFrame(row)
       gera_csv.to_csv(file_input, sep=';')

# gera arquivo .csv
file_input = 'twitter_'+str(pesquisa)+'_'+str(data_carga)+'.csv'
try:
       with zp.ZipFile('arq_'+str(data_carga)+'.zip', 'w') as file:
              file.write(file_input) 
              os.remove(file_input)                       
except IOError:
    print('Arquivo não encontrado')
# temove arquivo
os.remove(file_input)
acessa_banco(pesquisa)




