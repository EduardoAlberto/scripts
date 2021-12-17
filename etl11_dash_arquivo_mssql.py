
from dash_html_components.Figure import Figure
from dash_html_components.H1 import H1
import pyodbc 
import dash
import dash_table
import sqlalchemy as mssdb
import pandas as pd
import datetime as dt
import random
import dash_core_components as dcc
import dash_html_components as html


# estilo da tabela
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

cnxn = pyodbc.connect(DRIVER='{ODBC Driver 17 for SQL Server}',SERVER='localhost,1433',DATABASE='TutorialDB',UID='sa',PWD='Numsey@Password!')
cursor = cnxn.cursor()

# insert da tabela
csv = pd.read_csv("/Users/eduardoaandrad/Dropbox/Desenv/Script/csv/kc_house_data.csv")
cursor.fast_executemany = True
cursor.execute('truncate table tmp_bi_vendas')
cursor.executemany("insert into tmp_bi_vendas values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", csv.values.tolist())
cursor.execute('exec sp_carga_vendas')
tabela01 = pd.read_sql('select top 10 * from %s' % 'tb_bi_vendas', cnxn)
tabela02 = pd.read_sql('select * from %s' % 'tb_bi_vendas', cnxn)
cursor.commit()
cursor.close()
cnxn.close()

dados = pd.DataFrame(tabela02)

datadia = dados['dtatualizacao'].max()


total_price = 0
total_price15 = 0
total_living = 0
total_living15 = 0
total_lot = 0
total_lot15 = 0


total_price   = dados['price'].sum() / random.randint(1, 5)
total_living  = dados['sqft_living'].sum() / random.randint(1, 5)
total_lot     = dados['sqft_lot'].sum() / random.randint(1, 5) 


total_price15  = dados['price'].sum() / random.randint(1, 10)
total_living15 = dados['sqft_living15'].sum()  / random.randint(1, 10)
total_lot15    = dados['sqft_lot15'].sum() / random.randint(1, 10) 

# tabela html de exibição 
Tabela = dash_table.DataTable(
    data=tabela01.to_dict('records'),
    columns = [{'id': c, 'name': c} for c in tabela01.columns],
    style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'left'
        } for c in ['id', 'sqft_lot15']
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
    html.H1(children='Dashboard do Arquivo CSV'),
    Tabela,
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                    {'x':['Total Price','Total Living','Total Lot'], 'y':[total_price,total_living,total_lot], 'type': 'bar', 'name': 'Total Valor'},
                    {'x':['Total Price','Total Living','Total Lot'], 'y':[total_price15,total_living15,total_lot15], 'type': 'bar', 'name': 'Total Valor'},
                    
            ],
            'layout': {
                'title': 'Cargar CSV'
            }
        }
    )
])


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)

                    