import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO contacts (firstName,lastName,email,phone) VALUES (?,?,?,?)", (Hamisa,Musa,hamisamusam@gmail.com,0783922470))
cur.execute("INSERT INTO contacts (firstName,lastName,email,phone) VALUES (?,?,?,?)", ('Mahisa','Isa','mahisaisa@gmail.com','078395855'))


connection.commit()
connection.close()