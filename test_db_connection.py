'''
Test Connection with MySQL
'''
import mysql.connector
mydb = mysql.connector.connect(
 host="localhost",
 user="root",
 password=""
)
print(mydb)
