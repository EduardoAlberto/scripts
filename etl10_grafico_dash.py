# primeiro grafico usando o Dash
from dash_html_components.Figure import Figure
import dash
import pandas as pd
import tweepy 
import dash_table
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

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
                     
                     tweet.user.friends_count,
                     tweet.user.followers_count,
                     tweet.user.listed_count,
                     tweet.user.favourites_count,
                     tweet.user.statuses_count,
                     tweet.retweet_count                     
              ]
              table.append(tbl)
       return table
# pesquisa palavra no twitter
pesquisa = input('Digite uma palavra: ')
palavra = arq(pesquisa)
txt = pd.DataFrame(palavra, columns=['total_amigos','total_seguidores','total_listas','total_likes','total_status','total_retweet'])

# valor maximo
max_1 = txt['total_amigos'].max()
max_2 = txt['total_seguidores'].max()
max_3 = txt['total_listas'].max()
max_4 = txt['total_likes'].max()
max_5 = txt['total_status'].max()
max_6 = txt['total_retweet'].max()

# valor minimo
min_1 = txt['total_amigos'].sum()
min_2 = txt['total_seguidores'].sum()
min_3 = txt['total_listas'].sum()
min_4 = txt['total_likes'].sum() 
min_5 = txt['total_status'].sum()
min_6 = txt['total_retweet'].sum()

# Gera tabela
tabela = dash_table.DataTable(
    data=txt.to_dict('records'),
    columns =[{'id': c, 'name': c} for c in txt.columns],

    style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'left'
        } for c in ['total_amigos', 'total_seguidores']
    ],
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        }
    ],
    style_header={
        'backgroundColor': 'rgb(230, 230, 230)',
        'fontWeight': 'bold'
    }
    
)

# cria tabela com dados da api 
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Center(children=[
    html.H1(children='Dashboard com Dados do Twitter'),
    tabela,
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                    {'x': ['Total Amigo','Total Seguidores','Total Lista'], 'y': [max_1, max_2, max_4], 'type': 'bar', 'name': 'Maximos de Amigos'},
                    {'x': ['Total Amigo','Total Seguidores','Total Lista'], 'y': [min_1, min_2, min_4], 'type': 'bar', 'name': 'Soma de Amigos'},
                    
            ],
            'layout': {
                'title': 'Dash dos Dados Twitter'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)

