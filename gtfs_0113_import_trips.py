'''
Create table "trips" and import "trips.txt" from feed path "databasename".
Usage:
    python gtfs_0113_import_routes.py databasename
    
"trips.txt" contains these fields:
    trip_id
    route_id
    service_id
    direction_id    (although not optional)

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
    fileName = db_name + "/trips.txt"  # file from feed path "db_name"

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
    sql = "DROP TABLE IF EXISTS trips"
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE IF NOT EXISTS trips
    (              
        trip_id VARCHAR(50) PRIMARY KEY,
        route_id VARCHAR(50),
        service_id VARCHAR(50),
        direction_id TINYINT(1),
        INDEX (route_id)
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
                trip_id_pos = -1
                route_id_pos = -1
                service_id_pos = -1
                direction_id_pos = -1
                if "trip_id" in headerLineArray:
                    trip_id_pos = headerLineArray.index("trip_id")
                if "route_id" in headerLineArray:
                    route_id_pos = headerLineArray.index("route_id")
                if "service_id" in headerLineArray:
                    service_id_pos = headerLineArray.index("service_id")
                if "direction_id" in headerLineArray:
                    direction_id_pos = \
                        headerLineArray.index("direction_id")
            else:

                # Read the data of a line into an array
                lineArray = row
                if len(lineArray) >= field_number:
                    trip_id = lineArray[trip_id_pos]
                    route_id = lineArray[route_id_pos]
                    service_id = lineArray[service_id_pos]
                    direction_id = lineArray[direction_id_pos]

                    # Eintrag in MySQL Tabelle
                    sql = '''
                        INSERT INTO trips
                        (
                            trip_id,
                            route_id,
                            service_id,
                            direction_id
                        )
                        VALUES (%s, %s, %s, %s)
                    '''
                    mycursor.execute(sql, [trip_id,
                                           route_id,
                                           service_id,
                                           direction_id])

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
