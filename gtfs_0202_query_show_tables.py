'''
SHOW TABLES - Abfrage

Gets all tablenames of a database.
Usage:
    python gtfs_0202_query_show_tables.py databasename

Version: 2021-06-05 ... Version 001
'''

import mysql.connector
import sys
from sys import exit
from time import time
import gtfs_0100_my_db_auth

db_username = gtfs_0100_my_db_auth.db_username
db_password = gtfs_0100_my_db_auth.db_password
db_name = gtfs_0100_my_db_auth.db_name  # Test with this databasename

# Read one program parameter. This is the database name.
arguments_number = len(sys.argv) - 1
if arguments_number == 1:
    db_name = sys.argv[1]
else:
    print("ERROR: missing parameter 'databasename'.")
    # exit(1)   # Exit the programm with error code "1"

print("Query on database = %s" % db_name)
start_time = time()

mydb = mysql.connector.connect(
    host="localhost",
    user=db_username,
    password=db_password,
    database=db_name
)

mycursor = mydb.cursor()
sql = "SHOW TABLES"
mycursor.execute(sql)

myresult = mycursor.fetchall()

for x in myresult:
    print(x)

duration = time() - start_time
print("Query OK, %.2f seconds." % duration)
