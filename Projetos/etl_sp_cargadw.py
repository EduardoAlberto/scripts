#######################################################
# Assunto: Extração de dados no SQL_SERVER
# Autor  : Eduardo Alberto
# Data   : 16/04/2021
#######################################################
import pyodbc 
import pandas as pd
import sqlalchemy as mssdb

# arquivo
df = pd.read_csv("/Users/eduardoaandrad/RepFile/archive/olist_order_reviews_dataset.csv")

# conexao com o banco
cnxn = pyodbc.connect(DRIVER='{ODBC Driver 17 for SQL Server}',SERVER='localhost,1433',DATABASE='olist',UID='sa',PWD='Numsey@Password!',UseFMTONLY='Yes')
cursor = cnxn.cursor()

# cria Dataframe
arq = pd.DataFrame(df, columns=['review_id','order_id','review_score','review_comment_title','review_comment_message','review_creation_date','review_answer_timestamp'])

# carga stg
cursor.fast_executemany = True
cursor.execute('truncate table olist.dbo.tmp_order_reviews')
cursor.executemany("insert into olist.dbo.tmp_order_reviews values (?,?,?,?,?,?,?)", arq.values.tolist())
cursor.commit()
cursor.close()
cnxn.close()



