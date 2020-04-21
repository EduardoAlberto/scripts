import mysql.connector
import csv
mydb = mysql.connector.connect(user='root',password='mysql',host='0.0.0.0',database='mydesenv')
cursor = mydb.cursor()
with open('/Users/eduardoaandrad/Dropbox/Desenv/script/csv/carga_teste.csv') as source:
    csv_data = csv.reader(source, delimiter=';')
    next(csv_data) #remove o cabeçalho 
    for row in csv_data:
        cursor.execute('insert into mydesenv.tb_load (num, nm_name, dt_load) values (%s, %s, %s)',row[:27])
        mydb.commit()
cursor.close()

