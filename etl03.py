# carga verifica verifica tabela 
import mysql.connector
import datetime as dt
import csv

mydb = mysql.connector.connect(user='root',password='mysql',host='0.0.0.0',database='mydesenv')
cur = mydb.cursor()
# verifica se arquivo existe
# caso não exista retorna erro
try:
    # trunca ta tabela
    cur.execute('truncate table mydesenv.t_stg_valores')
    with open('/Users/eduardoaandrad/Dropbox/Desenv/python/3_analise/infopreco.csv', encoding = "ISO-8859-1") as arq:
        csv_data = csv.reader(arq, delimiter=';')
        next(csv_data)
        csv_data
        for row in csv_data:
            cur.execute('insert into mydesenv.t_stg_valores(CNPJ, NOME, ENDERECO, COMPLEMENTO, BAIRRO, MUNICIPIO, UF, PRODUTO, VALOR_VENDA, DATA_CADASTRO) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',row[:55])
            mydb.commit()
except IOError:
    print('Arquivo não encontrado')

