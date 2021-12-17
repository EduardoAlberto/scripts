# lib

# import dash
import pandas as pd
# from pandas.core.frame import DataFrame
import dash
import dash_table
# import dash_core_components as dcc
# import dash_html_components as html
import sqlalchemy as mssdb



# estilo da tabela
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# conexao com o banco e origem do arquivo .csv
# engine = mssdb.create_engine('mssql+pymssql://sa:Numsey@Password!@localhost:1401/DBDESENV')
# engine = mssdb.create_engine("mssql+pyodbc://sa:Numsey@Password!@localhost,1401/DBDESENV?driver=ODBC+DRIVER+17+for+SQL+Server")
engine = mssdb.create_engine("mssql+pyodbc://sa:Numsey@Password!@localhost,1433/TutorialDB?driver=ODBC+DRIVER+17+for+SQL+Server")
# engine = mssdb.create_engine('mssql+pyodbc://sa:Numsey@Password!@localhost,1401')

# cria dataframe com o arquivo .csv
df = pd.read_csv("/Users/eduardoaandrad/Dropbox/Desenv/Script/csv/kc_house_data.csv", sep=',', header=0, encoding='utf8', index_col=False)
# formata as colunas
df['dt_date']=df['dt_date'].apply(pd.to_datetime) 
df['lat']=df['lat'].apply(pd.to_numeric).map('{:,.3f}'.format)
df['long']=df['long'].apply(pd.to_numeric).map('{:,.3f}'.format) 


arquivo = pd.DataFrame(df)
arquivo.to_sql('vendas', con=engine, if_exists='replace', schema='dbo', index=False, chunksize = None, dtype={'dt_date':mssdb.types.Date})

# consultando a tabela no mssql
select = pd.read_sql('select top 10 * from %s' % 'vendas', engine)

# cria tabela com dados da api 
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# tabela html de exibição 
app.layout = dash_table.DataTable(
    data=select.to_dict('records'),
    columns = [{'id': c, 'name': c} for c in select.columns],
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

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)



