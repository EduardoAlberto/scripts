# lib

# import dash
import pandas as pd
# from pandas.core.frame import DataFrame
import dash
import dash_table
# import dash_core_components as dcc
# import dash_html_components as html
import sqlalchemy as mydb



# estilo da tabela
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# conexao com o banco e origem do arquivo .csv
engine = mydb.create_engine('mysql+mysqlconnector://root:mysql@localhost:3306/mydesenv?auth_plugin=mysql_native_password')



csv = "/Users/eduardoaandrad/Dropbox/Desenv/Script/csv/kc_house_data.csv"


# cria dataframe com o arquivo .csv
df = pd.read_csv(csv, sep=',', header=0, encoding='utf8', index_col=False)
# formata as colunas
df['dt_date']=df['dt_date'].apply(pd.to_datetime) 
df['lat']=df['lat'].apply(pd.to_numeric).map('{:,.3f}'.format)
df['long']=df['long'].apply(pd.to_numeric).map('{:,.3f}'.format) 


arquivo = pd.DataFrame(df)
arquivo.to_sql('tmp_vendas', con=engine, if_exists='replace',  index=False, dtype={'dt_date':mydb.types.Date})

# consultando a tabela no mssql
select = pd.read_sql('select * from %s limit 10' % 'tmp_vendas', engine)

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



