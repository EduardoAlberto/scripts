import sqlalchemy as mssdb
import pandas as pd
import tweepy 

# engine = mssdb.create_engine("mssql+pyodbc://sa:Numsey@Password!@0.0.0.0,1433/DBPRD?driver=ODBC+DRIVER+17+for+SQL+Server")

# # consultando a tabela no mssql
# select = pd.read_sql('select top 10 * from %s' % 'twitter', engine)

# chaves de conexão com twitter 
tolken = open('csv/cript.txt', 'r')

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

# print(consumer_key,consumer_secret,access_token, access_token_secret)


twitter.search(input('pesquisa: '))



