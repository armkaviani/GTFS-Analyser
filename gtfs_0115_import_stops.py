'''
Create table "stops" and import "stops.txt" from feed path "databasename".
Usage:
    python gtfs_0115_import_stops.py databasename
    
"stop_times.txt" contains these fields:
    stop_id
    stop_name
    stop_lat
    stop_lon

Version: 2021-06-07 ... Version 004
'''

import mysql.connector
import csv
from time import time
import sys
from sys import exit
import gtfs_0100_my_db_auth


def main():
    import gtfs_0100_my_db_auth
    db_username = gtfs_0100_my_db_auth.db_username
    db_password = gtfs_0100_my_db_auth.db_password
    db_name = gtfs_0100_my_db_auth.db_name  # Test with this databasename

    # Read one program parameter. This is the feed path AND database name.
    arguments_number = len(sys.argv) - 1
    if arguments_number == 1:
        db_name = sys.argv[1]
    else:
        print("ERROR: missing parameter 'databasename == feedpath'.")
        # exit(1)   # Exit the programm with error code "1"

    #### Values
    fileName = db_name + "/stops.txt"  # file from feed path "db_name"

    print("Import from %s START" % fileName)
    start_time = time()

    #### Connect with the database
    mydb = mysql.connector.connect(
        host="localhost",
        user="%s" % db_username,
        password="%s" % db_password,
        database="%s" % db_name
    )

    #### Create the table again
    # Wenn es eine alte Tabelle gibt, diese Tabelle löschen
    mycursor = mydb.cursor()
    sql = "DROP TABLE IF EXISTS stops"
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE IF NOT EXISTS stops
    (       
        stop_id VARCHAR(50) PRIMARY KEY,
        stop_name VARCHAR(255),
        stop_lat DECIMAL(9,6),
        stop_lon DECIMAL(9,6)
    )
    '''
    mycursor.execute(sql)

    #### Read the text file line by line, import each line
    n = m = 0  # n is the line counter
    firstLine = True
    with open(fileName, "r", encoding="utf-8-sig") as file:  # "utf-8-sig" removes BOM

        reader = csv.reader(file)
        for row in reader:
            # print("TEST row=" + str(row))  # TEST

            if firstLine == True:
                firstLine = False
                # Read the first line - the table header
                headerLineArray = row
                # print("TEST: Header-Array = " + str(headerLineArray))
                field_number = len(headerLineArray)

                # Find the position of all the fields of the table
                stop_id_pos = -1
                stop_name_pos = -1
                stop_lat_pos = -1
                stop_lon_pos = -1
                if "stop_id" in headerLineArray:
                    stop_id_pos = headerLineArray.index("stop_id")
                if "stop_name" in headerLineArray:
                    stop_name_pos = headerLineArray.index("stop_name")
                if "stop_lat" in headerLineArray:
                    stop_lat_pos = headerLineArray.index("stop_lat")
                if "stop_lon" in headerLineArray:
                    stop_lon_pos = headerLineArray.index("stop_lon")
            else:

                # Read the data of a line into an array
                lineArray = row
                if len(lineArray) >= field_number:
                    stop_id = lineArray[stop_id_pos]
                    stop_name = lineArray[stop_name_pos]
                    stop_lat = lineArray[stop_lat_pos]
                    stop_lon = lineArray[stop_lon_pos]

                    # Eintrag in MySQL Tabelle
                    sql = '''
                        INSERT INTO stops
                        (
                            stop_id,
                            stop_name,
                            stop_lat,
                            stop_lon
                        )
                        VALUES (%s, %s, %s, %s)
                    '''
                    mycursor.execute(sql, [stop_id,
                                           stop_name,
                                           stop_lat,
                                           stop_lon])

                    n = n + 1

                    # Progress-feedback every 10.000 lines
                    # m = m + 1
                    # if m >= 10000 :
                    #    m = 0
                    #    print("  Progress: %s" % n)

    # Altering tables requires commit. It is faster 
    #   doing this only one time, at the very end.
    mydb.commit()

    duration = time() - start_time
    print("Import OK ... %s rows in %.2f seconds" % (n, duration))


main()
