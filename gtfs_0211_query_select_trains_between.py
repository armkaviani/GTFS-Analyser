'''
Getting all trips at a given stop between two times, sorted by departure time.

Usage:
    python gtfs_0211_query_select_trains_between.py databasename

Tested with feed "Schienenfernverkehr" from gtfs.de.

Version: 2021-06-19 ... Version 002   
    
Diskussion:    
Für einen Haltepunkt: Alle Fahrten (trips) zwischen 20:00 und 21:00 Uhr,
nach der Ankunftszeit sortiert. Man beachte die Schreibweise der Uhrzeit!
(Die Tabellen calendar und calendar_dates werden in diesem Beispiel nicht verwendet.)

Diskussion:
Man beachte die Schreibweise der Uhrzeit '21:00:00.000'.
Auch hier findet man Zeiten nach 24:00 Uhr. Das sind Fahrten, die
am Tag zuvor begonnen haben.

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
this_stop_name = 'LIKE "Berlin Hbf%"' 

# two pair of times – the second pair is for trains over midnight
min_time_string = '00:30:00.000'
max_time_string = '01:30:00.000'
min_time2_string = '24:30:00.000'  # min_time_string + 24h
max_time2_string = '25:30:00.000'  # max_time_string + 24h
    
print("Query on database = %s" % db_name)
start_time = time()

mydb = mysql.connector.connect(
    host = "localhost",
    user = db_username,
    password = db_password,
    database = db_name
)

mycursor = mydb.cursor()

sql = f"""
    SELECT r.route_short_name, s.stop_name, t.trip_id,
        TIME_FORMAT(st.departure_time, '%H:%i')
    FROM routes r
    INNER JOIN trips t ON r.route_id = t.route_id
    INNER JOIN stop_times st ON t.trip_id = st.trip_id
    INNER JOIN stops s ON st.stop_id = s.stop_id
    WHERE s.stop_name {this_stop_name}
        AND (st.departure_time >= '{min_time_string}'
        AND st.departure_time < '{max_time_string}'
        OR st.departure_time >= '{min_time2_string}'
        AND st.departure_time < '{max_time2_string}')
    GROUP BY r.route_short_name, s.stop_name, t.trip_id
    ORDER BY st.departure_time
"""

print(sql)
mycursor.execute(sql)
myresult = mycursor.fetchall()
#print("%s lines in myresult" % len(myresult)) #TEST

for x in myresult:
    print(x)

duration = time() - start_time
print("Query OK, %.2f seconds." % duration)
