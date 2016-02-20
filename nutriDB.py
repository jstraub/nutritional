import sqlite3

conn = sqlite3.connect("sr28asc.db")
c = conn.cursor()
c.execute('SELECT Long_Desc FROM FOOD_DES WHERE Long_Desc LIKE "Cheese%"')
res = c.fetchall()
print res
conn.close()
