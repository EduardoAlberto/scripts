# nova script dec carga
import mysql.connector
import datetime as dt
import petl as etl
import os 
import csv

# variavel de data
dt_carga = dt.date.today()

# diretorio
infile = '/Users/eduardoaandrad/Dropbox/Desenv/python/3_analise/infopreco.csv'
outfile = '/Users/eduardoaandrad/Dropbox/Desenv/script/csv/preco_'+str(dt_carga)+'.csv'

#connect ao database 
mydb = mysql.connector.connect(user='root',password='mysql',host='0.0.0.0',database='mydesenv')
cur = mydb.cursor()
try:
    # trunca ta tabela
    cur.execute('truncate table mydesenv.t_tmp_valores')
    # carrega base e executa os tratamentos
    tbl = (etl.fromcsv(infile, encoding = "ISO-8859-1",delimiter=';')
                .convert('CNPJ'         ,  str   )
                .convert('NOME'         , 'upper')
                .convert('ENDERECO'     , 'upper')
                .convert('COMPLEMENTO'  , 'upper')
                .convert('BAIRRO'       , 'upper')
                .convert('MUNICIPIO'    , 'upper')
                .convert('UF'           , 'upper')
                .convert('PRODUTO'      , 'upper')
                .addfield('DATA_CARGA'  , dt.date.today())
            ) 
    # remove a cabeçalho 
    table = etl.data(tbl)
    # gera .csv
    etl.tocsv(table, outfile, delimiter=';')
except IOError:
    print('Arquivo não encontrado')
# carrega a nova base 
try:
    with open(outfile, encoding = "ISO-8859-1") as arq:
     csv_data = csv.reader(arq, delimiter=';')
     for row in csv_data:
         cur.execute('insert into mydesenv.t_tmp_valores(CNPJ, NOME, ENDERECO, COMPLEMENTO, BAIRRO, MUNICIPIO, UF, PRODUTO, VALOR_VENDA, DATA_CADASTRO, DATA_CARGA) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',row[:11])
         mydb.commit()
    #  remove os arquivos mais antigos
    if os.path.exists(outfile):
        os.remove((outfile))
    else:
        print('arquivo não existe !')

except IOError:
    print('Arquivo não encontrado')





