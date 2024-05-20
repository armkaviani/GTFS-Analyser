'''
SHOW DATABASES

Gets all database names of the MariaDB.
Usage:
    python gtfs_0201_query_databases.py
    
Version: 2021-06-19 ... Version 002
'''

import mysql.connector
from time import time
import gtfs_0100_my_db_auth

db_username = gtfs_0100_my_db_auth.db_username
db_password = gtfs_0100_my_db_auth.db_password

start_time = time()

mydb = mysql.connector.connect(
    host="localhost",
    user=db_username,
    password=db_password
)

mycursor = mydb.cursor()
sql = "SHOW DATABASES"
print(sql)
mycursor.execute(sql)

myresult = mycursor.fetchall()

for x in myresult:
    print(x)
    # print(type(x))   #TEST

duration = time() - start_time
print("Query OK, %.2f seconds." % duration)
