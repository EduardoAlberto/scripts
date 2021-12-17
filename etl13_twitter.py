import tweepy 
import pandas as pd
import sqlalchemy as mssdb


# chaves de conexão com twitter 
tolken = open('cript.txt', 'r')

consumer_key = []
consumer_secret = []
access_token = []
access_token_secret = []

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

# engine = mssdb.create_engine('mssql+pymssql://sa:Numsey@Password!@localhost:1401/DBDESENV')
engine = mssdb.create_engine("mssql+pyodbc://sa:Numsey@Password!@0.0.0.0,1433/DBPRD?driver=ODBC+DRIVER+17+for+SQL+Server")

def arq(pesquisa):
       # palavra que iremos procurar
       resultado = twitter.search(pesquisa)
       table = []
       for tweet in resultado:
              
              tbl = [
                     tweet.user.name,
                     tweet.user.screen_name,
                     tweet.user.location,
                     tweet.user.description,
                     tweet.user.protected,
                     tweet.user.verified,
                     tweet.user.followers_count, 
                     tweet.user.friends_count,
                     tweet.user.listed_count,
                     tweet.user.favourites_count,
                     tweet.user.statuses_count,
                     tweet.user.created_at,
                     tweet.lang,
                     tweet.text,
                     tweet.source,
                     tweet.retweet_count,
                     tweet.author.following,
                     tweet.author.follow_request_sent,
                     tweet.retweeted                     
              ]
              table.append(tbl)
       return table

pesquisa = input('Digite uma palavra: ')
resultado = arq(pesquisa)
table = pd.DataFrame(resultado, columns=['name','screen_name','location','description','protected','verified','followers_count','friends_count',
                                        'listed_count','favourites_count','statuses_count','created_at','lang','twitter','source','retweet_count',
                                        'following','follow_request_sent','retweeted'])


table.to_sql('twitter', con=engine, if_exists='append', schema='dbo', index=False, chunksize = None)