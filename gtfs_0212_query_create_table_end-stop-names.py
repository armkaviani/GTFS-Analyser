'''
Create table end_stop_names - the last stop of every trip.
(This end_stop_names may serve as a long names of the trips.)

Usage:
    python gtfs_0212_query_create_table_end-stop-name.py databasename

Tested with feed "Schienenfernverkehr" from gtfs.de.

Version: 2021-06-28 ... Version 003

Diskussion:
ERROR:
Mit der großen Datenmenge "Nahverkehr" von gtfs.de bringt die erste SQL-Anweisung
diesen Error: "The total number of locks exceeds the lock table size".
FIX:
https://stackoverflow.com/questions/6901108/the-total-number-of-locks-exceeds-the-lock-table-size
Der Standard-Wert von innodb_buffer_pool_size = 8.388.608
 So ändert man ihn:
 SET GLOBAL innodb_buffer_pool_size=268435456;

'''
import mysql.connector
import sys
from sys import exit
from time import time
import gtfs_0100_my_db_auth

db_username = gtfs_0100_my_db_auth.db_username
db_password = gtfs_0100_my_db_auth.db_password
db_name = gtfs_0100_my_db_auth.db_name # Test with this databasename

# Read the program parameters. This is the databasename and the trip_id.
arguments_number = len(sys.argv) - 1
if(arguments_number == 1) :
    db_name = sys.argv[1]
else :
    print ("ERROR: missing parameter: 'databasename'.")    
    #exit(1)   # Exit the programm with error code "1"
    
print("Query on database = %s" % db_name)
start_time = time()

mydb = mysql.connector.connect(
    host = "localhost",
    user = db_username,
    password = db_password,
    database = db_name
)

# Drop the previous sotdated result table, if exists
mycursor = mydb.cursor()
sql = "DROP TABLE IF EXISTS xtra_trip_end_names";
mycursor.execute(sql)

# Prevent error "The total number of locks exceeds the lock table size"
sql = "SET GLOBAL innodb_buffer_pool_size=268435456;"
mycursor.execute(sql)

# Create table of last stop_seq.-number of each trip_id
sql = f'''
    CREATE TEMPORARY TABLE temp_last_stop_sequence AS 
    SELECT t.trip_id AS trip_id,
        MAX(st.stop_sequence) AS last_stop_sequence
    FROM trips t
    INNER JOIN stop_times st ON t.trip_id = st.trip_id
    GROUP BY trip_id
'''

print(sql)
mycursor.execute(sql)

# Create table of last stop_id of each trip_id
sql = f'''
    CREATE TEMPORARY TABLE temp_last_stop_id AS
    SELECT l.trip_id AS trip_id, st.stop_id AS last_stop_id
    FROM stop_times st
    INNER JOIN temp_last_stop_sequence l
        ON (st.trip_id = l.trip_id
            AND st.stop_sequence = l.last_stop_sequence)
'''

print(sql)
mycursor.execute(sql)
##SQL has multiple statements, so we loop the "mycursor.execute(sql)"
#for result in mycursor.execute(sql, multi = True):
#    pass


# altering tables requires commit
mydb.commit()

# Create new "extra" table: the last stop name of every trip
sql = f'''
    CREATE TABLE xtra_trip_end_names AS
    SELECT tlsid.trip_id AS trip_id,
        tlsid.last_stop_id AS last_stop_id,
        s.stop_name AS last_stop_name
    FROM stops s
    INNER JOIN temp_last_stop_id tlsid
    ON s.stop_id = tlsid.last_stop_id
'''

print(sql)
mycursor.execute(sql)


duration = time() - start_time
print("Query OK, %.2f seconds." % duration)
