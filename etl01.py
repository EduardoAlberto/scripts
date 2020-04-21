# teste de carga no banco
import mysql.connector
conn = mysql.connector.connect(user='root', 
                               password='mysql',
                               host='0.0.0.0',
                               database='mydesenv')

# abre o cursor
cur = conn.cursor()

# query sql
sql = (" insert into mydesenv.tb_load(id, nm_name, dt_load) values(%s, %s, %s) ")
data = (1, 'Eduardo','2020-03-23')
cur.execute(sql, data)
conn.commit()
conn.close()  