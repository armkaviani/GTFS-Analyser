'''
Create table for application "all departures from Leipzig Hbf".
Creates table: xtra_departures_days_leipzig_hbf

Usage:
    gtfs_0232_create_3_applikation_table_leipzig_hbf.py databasename

Tested with feed "Schienennahverkehr" from gtfs.de.

Version: 2021-06-29 ... Version 002   

'''
import mysql.connector
import sys
from sys import exit
from time import time
import datetime
import gtfs_0100_my_db_auth

db_username = gtfs_0100_my_db_auth.db_username
db_password = gtfs_0100_my_db_auth.db_password
db_name = gtfs_0100_my_db_auth.db_name  # Test with this databasename

# Read the program parameter. This is the database name.
arguments_number = len(sys.argv) - 1
if arguments_number == 1:
    db_name = sys.argv[1]
else:
    print("ERROR: missing parameter 'databasename'.")
    # exit(1)   # Exit the programm with error code "1"

# this_date ... e.g. today date
# ===> TODO: Parameterübenrahme "date" und Berechnung Wochentag, Yesterday etc. programmieren!
today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
yesterday = today - datetime.timedelta(days=1)

today_date = str(today)
tomorrow_date = str(tomorrow)
yesterday_date = str(yesterday)

today_wd = today.strftime('%A').lower()
tomorrow_wd = tomorrow.strftime('%A').lower()
yesterday_wd = yesterday.strftime('%A').lower()

# TEST DATA
# yesterday_date = "2021-06-10"
# today_date = "2021-06-11"
# tomorrow_date = "2021-06-12"

# yesterday_wd = "thursday"
# today_wd = "friday"
# tomorrow_wd = "saturday"

print("START query on database = %s" % db_name)
start_time = time()

mydb = mysql.connector.connect(
    host="localhost",
    user=db_username,
    password=db_password,
    database=db_name
)

# Drop the previous outdated result table, if exists
mycursor = mydb.cursor()
sql = "DROP TABLE IF EXISTS xtra_departures_days_leipzig_hbf"
mycursor.execute(sql)

# Create new "extra" table: All departures from Leipzig Hbf today.
sql = f"""
    CREATE TABLE xtra_departures_days_leipzig_hbf AS (
        SELECT DATE('{today_date}') as day, x.*
        FROM xtra_departures_leipzig_hbf x
        WHERE midnights = 0 AND
            (
                ('{today_date}' >= x.start_date
                    AND '{today_date}' <= x.end_date
                    AND x.{today_wd} = 1)
                OR ('{today_date}' = x.exception_date
                    AND x.exception_type = 1)
                OR (x.exception_date IS NULL
                    AND x.monday IS NULL)
            )
            OR midnights = 1 AND
            (
                ('{yesterday_date}' >= x.start_date
                    AND '{yesterday_date}' <= x.end_date
                    AND x.{yesterday_wd} = 1)
                OR ('{yesterday_date}' = x.exception_date
                    AND x.exception_type = 1)
                OR (x.exception_date IS NULL
                    AND x.monday IS NULL)
            )
        ORDER BY x.departure_clock_time
    );
"""

print(sql)
mycursor.execute(sql)

# altering tables requires commit
mydb.commit()

duration = time() - start_time
print("Query 1 OK ... %.2f seconds" % duration)

# Append new "extra" table: All departures from Leipzig Hbf tomorrow.
start_time = time()
sql = f"""
    INSERT INTO xtra_departures_days_leipzig_hbf
        SELECT DATE('{tomorrow_date}') as day, x.*
        FROM xtra_departures_leipzig_hbf x
        WHERE midnights = 0 AND
            (
                ('{tomorrow_date}' >= x.start_date
                    AND '{tomorrow_date}' <= x.end_date
                    AND x.{tomorrow_wd} = 1)
                OR ('{tomorrow_date}' = x.exception_date
                    AND x.exception_type = 1)
                OR (x.exception_date IS NULL
                    AND x.monday IS NULL)
            )
            OR midnights = 1 AND
            (
                ('{today_date}' >= x.start_date
                    AND '{today_date}' <= x.end_date
                    AND x.{today_wd} = 1)
                OR ('{yesterday_date}' = x.exception_date
                    AND x.exception_type = 1)
                OR (x.exception_date IS NULL
                    AND x.monday IS NULL)
            )
        ORDER BY x.departure_clock_time
"""

print(sql)
mycursor.execute(sql)

# altering tables requires commit
mydb.commit()

duration = time() - start_time
print("Query 2 OK ... %.2f seconds" % duration)
