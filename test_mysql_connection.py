# pip install mysql-connector

from mysql.connector import connect

cnx = connect(
	host='localhost',
	database='movies',
	user='root',
	password='root', 
	port=3306
)

print("Successfully connected to database.")