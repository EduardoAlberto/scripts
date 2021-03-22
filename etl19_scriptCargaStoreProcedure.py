########################################################
# Assunto: criação de procedure e execucao
# data:21/03/2021
# Criado: Eduardo Alberto Andrade
########################################################
import pyodbc 
import pandas as pd
import datetime as dt

cnxn = pyodbc.connect(DRIVER='{ODBC Driver 17 for SQL Server}',SERVER='localhost,1433',DATABASE='dbproducao',UID='sa',PWD='Numsey@Password!')
cursor = cnxn.cursor()

# executando a procedure
StartProductID = 807
CheckDate = pd.to_datetime('2010-03-04')
proc = pd.read_sql_query("exec dbo.uspGetBillOfMaterials {},'{}'".format(StartProductID,CheckDate),cnxn)
print(CheckDate)





