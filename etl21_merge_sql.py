#######################################################
# Assunto: Extração de dados no SQL_SERVER
# Autor  : Eduardo Alberto
# Data   : 12/04/2021
#######################################################
# import pyodbc 
import sqlalchemy as mssdb
import pandas as pd

# arquivo
arquivo = pd.read_csv('/Users/eduardoaandrad/RepFile/emails.csv')

# conexão
# cnxn = pyodbc.connect(DRIVER='{ODBC Driver 17 for SQL Server}',SERVER='localhost,1433',DATABASE='dwproducao',UID='sa',PWD='Numsey@Password!')
# cursor = cnxn.cursor()

engine = mssdb.create_engine("mssql+pyodbc://sa:Numsey@Password!@localhost,1433/TutorialDB?driver=ODBC+DRIVER+17+for+SQL+Server")

#Verificando versão do sql server
row = engine.execute("SELECT @@version;").fetchall()
for a in row:
    print(a[0])

#criando tabela no sql
arquivo = pd.DataFrame(arquivo, columns=['Email No.', 'the', 'to', 'ect', 'and', 'for', 'of', 'a', 'you', 'hou',
                                         'connevey', 'jay', 'valued', 'lay', 'infrastructure', 'military',
                                         'allowing', 'ff', 'dry', 'Prediction'])

arquivo.to_sql('email_spam', con=engine, if_exists='replace', schema='dbo', index=False)


