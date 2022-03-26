import sqlite3
connection = sqlite3.connect("Photons.db")
print("Database opened successfully")
cursor = connection.cursor()
#delete
#cursor.execute('''DROP TABLE Photons;''')
connection.execute("create table Photons (photo INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, file TEXT NOT NULL)")
print("Table created successfully")
connection.close()   
