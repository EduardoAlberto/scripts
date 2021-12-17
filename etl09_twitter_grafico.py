import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
import plotly.graph_objects as go
import plotly.express as px
import tweepy 


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


# Teste com grafico de barra
trace1 = go.Bar(x = ['Total Amigo','Total Seguidores', 'Total Likes', 'Total Retweet'],
                y = [txt['total_amigos'], txt['total_seguidores'], txt['total_likes'], txt['total_retweet']])

data = [trace1]
py.iplot(data)


total_1 = txt['total_amigos'].sum()
total_2 = txt['total_seguidores'].sum()
total_3 = txt['total_listas'].sum()
total_4 = txt['total_likes'].sum()
total_5 = txt['total_status'].sum()
total_6 = txt['total_retweet'].sum()



labels = ['Total Amigo','Total Seguidores', 'Total Likes', 'total_likes', 'total_status' ,'Total Retweet']
values = [total_1, total_2, total_3, total_4, total_5, total_6 ]

fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
fig.show()


# print(txt)
# print(txt['total_retweet'].sum())
