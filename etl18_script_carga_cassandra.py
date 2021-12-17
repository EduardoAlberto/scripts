###########################################################################
# Assunto: script de carga do banco Apache Cassandra
# data: 10/03/2021
# 
###########################################################################

from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
import pyodbc 
import pandas as pd

# conexao  mssql
cnxn = pyodbc.connect(DRIVER='{ODBC Driver 17 for SQL Server}',SERVER='localhost,1433',DATABASE='TutorialDB',UID='sa',PWD='Numsey@Password!')
cursor = cnxn.cursor()

# conexao cassandra
cluster = Cluster(['127.0.0.1'])
session = cluster.connect()

# arquivo .csv
csv = pd.read_csv("/Users/eduardoaandrad/Dropbox/Desenv/Script/csv/kc_house_data.csv", 
                  sep=',', header=0, encoding='utf8', index_col=False)

# formatando o campo data e os campos decimais
csv['dt_date']=pd.to_datetime(csv['dt_date'].astype(str))
csv['lat']=csv['lat'].apply(pd.to_numeric).map('{:,.3f}'.format)
csv['long']=csv['long'].apply(pd.to_numeric).map('{:,.3f}'.format) 

# print(csv)

# mssql
mssql = pd.read_sql_query('select * from rental_data',cnxn)


# verifica se tabela já existe
session.execute ("""
                CREATE TABLE if not exists dbcassandra.tb_bi_vendas(
                 id_num         uuid
                ,id	            bigint
                ,dt_date        date
                ,price	        float
                ,bedrooms	    float
                ,bathrooms	    float
                ,sqft_living    int
                ,sqft_lot	    int
                ,floors	        float
                ,waterfront	    int
                ,views	        int
                ,condition	    int
                ,grade	        int
                ,sqft_above	    int
                ,sqft_basement	int
                ,yr_built	    int
                ,yr_renovated	int
                ,zipcode	    int
                ,lat	        DECIMAL
                ,long	        DECIMAL
                ,sqft_living15	int
                ,sqft_lot15	    int
                ,dtatualizacao  TIMESTAMP
                ,PRIMARY KEY(id)
                )WITH comment = 'Tabela de teste de carga'; 
""")

query01="insert into dbcassandra.tb_bi_vendas(id_num,id,dt_date,price,bedrooms,bathrooms,sqft_living,\
         sqft_lot,floors,waterfront,views,condition,grade,sqft_above,sqft_basement,\
         yr_built,yr_renovated,zipcode,lat,long,sqft_living15,sqft_lot15,dtatualizacao)\
         values (now(), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, dateOf(now()))"
         
# executa a carga
prepared = session.prepare(query01)
for index,carga in csv.iterrows():
    session.execute(prepared
                    ,(carga['id']
                    , carga['dt_date']
                    , carga['price']
                    , carga['bedrooms']
                    , carga['bathrooms']
                    , carga['sqft_living']
                    , carga['sqft_lot']
                    , carga['floors']
                    , carga['waterfront']
                    , carga['view']
                    , carga['condition']
                    , carga['grade']
                    , carga['sqft_above']
                    , carga['sqft_basement']
                    , carga['yr_built']
                    , carga['yr_renovated']
                    , carga['zipcode']
                    , carga['lat']
                    , carga['long']
                    , carga['sqft_living15']
                    , carga['sqft_lot15'])
                    )

# cria tabela rental_data
session.execute("""
                CREATE TABLE if not exists dbcassandra.rental_data(
                Year	          int
                ,Month  	      int
                ,Day	          int
                ,RentalCount	  int
                ,WeekDay	      int
                ,Holiday	      int
                ,Snow	          int
                ,FHoliday	      text
                ,FSnow	          text
                ,FWeekDay	      text
                ,PRIMARY KEY(Year, Month, Day)
                )WITH comment = 'Tabela de teste de carga'; 
""")

# cria insert
query02 = "insert into dbcassandra.rental_data(Year,Month,Day,RentalCount,WeekDay,Holiday,Snow,FHoliday,FSnow,FWeekDay)\
         values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

prepared = SimpleStatement(query02)
for index,carga in mssql.iterrows():
    session.execute(prepared
                    ,(carga['Year']
                    , carga['Month']
                    , carga['Day']
                    , carga['RentalCount']
                    , carga['WeekDay']
                    , carga['Holiday']
                    , carga['Snow']
                    , carga['FHoliday']
                    , carga['FSnow']
                    , carga['FWeekDay'])
                    )


