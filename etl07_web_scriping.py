# criação de web scriping 
import pandas as pd
import requests
import mysql.connector
from bs4 import BeautifulSoup


# url
ano = input('digite o ano: ')
url = "https://esportes.estadao.com.br/classificacao/futebol/campeonato-brasileiro-serie-a/"+str(ano)+""
response = requests.get(url)
if response.status_code == 200:
    print('Requisição bem sucedida!')
    html = response.content

# Parser
soup = BeautifulSoup(html, 'lxml')

# procura por tabela
tbl = soup.find_all('table')
times = pd.read_html(str(tbl))[0]
pontuacao = pd.read_html(str(tbl))[1]



#times
clube = times['Unnamed: 3']
# pontos
pontos         = pontuacao['p']
jogos          = pontuacao['j']
vitorias       = pontuacao['v']
empates        = pontuacao['e']
derrotas       = pontuacao['d']
gols           = pontuacao['g']
golsContras    = pontuacao['gc']
saldoGols      = pontuacao['sg']

# unificando tudo em uma unica tabela

tabela=[]
for a, b,c,d,e,f,g,h,i in zip(clube, pontos,jogos,vitorias,empates,derrotas,gols,golsContras,saldoGols):
    tbl = [   
             a
            ,b
            ,c
            ,d
            ,e
            ,f
            ,g
            ,h
            ,i
    ]
    tabela.append(tbl)
txt = pd.DataFrame(tabela) 

print(txt)

# txt = pd.DataFrame(tbl1, columns=[ 'TIME','P','J','V','E','D','G','GC','SG'])

# print(txt)
  

