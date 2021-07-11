'''
Create table for application "all departures from Leipzig Hbf".
Creates table: xtra_departures_leipzig_hbf

Usage:
    python gtfs_0231_create_1_applikation_table_leipzig_hbf.py databasename

Tested with feed "Schienennahverkehr" from gtfs.de.

Version: 2021-06-28 ... Version 001   
    
'''
import mysql.connector
import sys
from sys import exit
from time import time
import gtfs_0100_my_db_auth

db_username = gtfs_0100_my_db_auth.db_username
db_password = gtfs_0100_my_db_auth.db_password
db_name = gtfs_0100_my_db_auth.db_name # Test with this databasename

# Read the program parameter. This is the database name.
arguments_number = len(sys.argv) - 1
if(arguments_number == 1) :
    db_name = sys.argv[1]
else :
    print ("ERROR: missing parameter 'databasename'.")    
    #exit(1)   # Exit the programm with error code "1"
    
# this_stop_name is e.g.'= "Berlin Hbf"' or 'LIKE "Berlin Hbf%"'
this_stop_name = 'LIKE "Leipzig%Hbf%"' 

print("START query on database = %s" % db_name)
start_time = time()

mydb = mysql.connector.connect(
    host = "localhost",
    user = db_username,
    password = db_password,
    database = db_name
)


# Drop the previous sotdated result table, if exists
mycursor = mydb.cursor()
sql = "DROP TABLE IF EXISTS xtra_departures_leipzig_hbf"
mycursor.execute(sql)

# Create new "extra" table: All departures from Leipzig Hbf.
sql = f'''
    CREATE TABLE xtra_departures_leipzig_hbf AS (
        SELECT r.route_short_name,
            s.stop_name,
            t.trip_id,
            x.last_stop_name,
            st.departure_time as departure_time,
            st.departure_time as departure_clock_time, 0 as midnights,
            cd.date as exception_date, cd.exception_type,
            c.*
        FROM routes r
        INNER JOIN trips t ON r.route_id = t.route_id
        INNER JOIN stop_times st ON t.trip_id = st.trip_id
        INNER JOIN stops s ON st.stop_id = s.stop_id
        INNER JOIN xtra_trip_end_names x ON st.trip_id = x.trip_id
        LEFT JOIN calendar_dates cd ON t.service_id = cd.service_id
        LEFT JOIN calendar c ON t.service_id = c.service_id
        WHERE s.stop_name {this_stop_name}
        GROUP BY r.route_short_name, s.stop_name, t.trip_id
        ORDER BY st.departure_time
    );
'''

print(sql)
mycursor.execute(sql)

# altering tables requires commit
mydb.commit()

duration = time() - start_time
print("Query 1 OK ... %.2f seconds" % duration)

# Fix clock times > 23:59:59
start_time = time()
sql = f"""
    UPDATE xtra_departures_leipzig_hbf
    SET midnights = midnights + 1,
        departure_clock_time = ADDTIME(departure_clock_time, "-24:00:00")
    WHERE departure_clock_time >= '24:00:00';
"""

print(sql)
mycursor.execute(sql)
mydb.commit()  # altering tables requires commit

duration = time() - start_time
print("Query 2 OK ... %.2f seconds" % duration)
