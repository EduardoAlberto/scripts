# criação de web scriping 
import pandas as pd
import requests
import dash
import dash_table
import sqlalchemy as mysdb
import sqlalchemy as mssdb
from bs4 import BeautifulSoup


# conexao com banco
# MSSQL
engineMssdb = mssdb.create_engine("mssql+pyodbc://sa:Numsey@Password!@localhost,1401/DBDESENV?driver=ODBC+DRIVER+17+for+SQL+Server")
# MYSQL
engineMysdb = mysdb.create_engine('mysql+mysqlconnector://root:mysql@localhost:3306/mydesenv')

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
for clube, pontos,jogos,vitorias,empates,derrotas,derrotas,golsContras,saldoGols in zip(clube, pontos,jogos,vitorias,empates,derrotas,derrotas,golsContras,saldoGols):
    tbl = [   
             clube
            ,pontos
            ,jogos
            ,vitorias
            ,empates
            ,derrotas
            ,derrotas
            ,golsContras
            ,saldoGols
    ]
    tabela.append(tbl)
txt = pd.DataFrame(tabela, columns=['TIME','P','J','V','E','D','G','GC','SG']) 

# cria as tabelas no banco
txt.to_sql('tb_campeonadobrasil_{}'.format(ano), con=engineMssdb, if_exists='replace', schema='dbo', index=False, chunksize = None)
txt.to_sql('tb_campeonadobrasil_{}'.format(ano), con=engineMysdb, if_exists='replace',  index=False)

# criado dashboard


