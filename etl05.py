# acessar https://apps.twitter.com para criar uma nova aplicação
# cada aplicação tem suas próprias chaves
import tweepy 
import datetime as dt
import pandas as pd



# diretorio saida
data_carga = dt.date.today()
file_input = '/Users/eduardoaandrad/Dropbox/Desenv/script/csv/twitter'+str(data_carga)+'.csv'

# chaves de conexão com twitter 
consumer_key = 'vXXNO13798aXqygq4tt7qkPaH'
consumer_secret = 'W0V2ML4BFqRF0NQZQ4XKVDYAVKb7S0GFboVbCJGy52TO9fEMf2'

access_token = '1141802923921424384-NaInVXbx4fkcwsUtsWRz74ey4FKVBp'
access_token_secret = '3xeTG6z7dt9RfhC4N23lnXSiATBkSZsNlHBla51zJxJSk'

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
palavra = arq(input('Digite uma palavra: '))
txt = pd.DataFrame(palavra, columns=['usuario','localizacao','total_amigos','total_seguidores','total_listas','Total_likes','status_verificado','total_status','total_retweet','tweet'])
txt['localizacao'].replace({'\u0000', 'sem_localizacao'},inplace =True)
# conexao com o banco

print(txt)


