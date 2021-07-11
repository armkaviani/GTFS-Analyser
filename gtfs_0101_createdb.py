'''
Creating a new database at the MariaDB DBMS.
The database name is the single program parameter of that Python script.
Usage:
    python gtfs_0101_createdb.py databasename

Version: 2021-06-02 ... Version 003
'''

import mysql.connector
from time import time
import sys
from sys import exit

def main() :
    
    import gtfs_0100_my_db_auth
    db_username = gtfs_0100_my_db_auth.db_username
    db_password = gtfs_0100_my_db_auth.db_password
    db_name = gtfs_0100_my_db_auth.db_name # Test with this databasename

    # Read one program parameter. This ist the database name.
    arguments_number = len(sys.argv) - 1
    if(arguments_number == 1) :
        db_name = sys.argv[1]
    else :
        print ("ERROR: missing parameter 'databasename'.")    
        #exit(1)   # Exit the programm with error code "1"
        
    # Action start
    print("Start creating DB '%s'." % db_name)
    start_time = time()

    mydb = mysql.connector.connect(
        host="localhost",
        user="%s" % db_username,
        password="%s" % db_password
    )

    mycursor = mydb.cursor()
    sql = "DROP DATABASE IF EXISTS %s" % db_name
    print("SQL_1: %s" % sql)
    mycursor.execute(sql)

    mycursor = mydb.cursor()
    sql = "CREATE DATABASE IF NOT EXISTS %s" % db_name
    print("SQL_2: %s" % sql)
    mycursor.execute(sql)
    
    # altering tables requires commit
    mydb.commit()

    # Action finish
    duration = time() - start_time
    print("DB '%s' created after %.2f seconds OK."
          % (db_name, duration))

main()
