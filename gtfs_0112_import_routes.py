'''
Create table "routes" and import "routes.txt" from feed path "databasename".
Usage:
    python gtfs_0112_import_routes.py databasename
    
"routes.txt" contains these fields:
    route_id,
    agency_id,
    route_short_name,
    route_long_name,
    route_type
    
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
    fileName = db_name + "/routes.txt"  # file from feed path "db_name"

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
    sql = "DROP TABLE IF EXISTS routes"
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE IF NOT EXISTS routes
    (        
        route_id VARCHAR(50) PRIMARY KEY,
        agency_id VARCHAR(50),
        route_short_name VARCHAR(50),
        route_long_name VARCHAR(255),
        route_type INT(2)
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
                route_id_pos = -1
                agency_id_pos = -1
                route_short_name_pos = -1
                route_long_name_pos = -1
                route_type_pos = -1
                if "route_id" in headerLineArray:
                    route_id_pos = headerLineArray.index("route_id")
                if "agency_id" in headerLineArray:
                    agency_id_pos = headerLineArray.index("agency_id")
                if "route_short_name" in headerLineArray:
                    route_short_name_pos = \
                        headerLineArray.index("route_short_name")
                if "route_long_name" in headerLineArray:
                    route_long_name_pos = \
                        headerLineArray.index("route_long_name")
                if "route_type" in headerLineArray:
                    route_type_pos = headerLineArray.index("route_type")
                # print(route_id_pos, agency_id_pos, route_short_name, route_long_name_pos, route_type_pos)  # TEST

            else:

                # Read the data of a line into an array
                lineArray = row
                if len(lineArray) >= field_number:
                    route_id = lineArray[route_id_pos]
                    agency_id = lineArray[agency_id_pos]
                    route_short_name = lineArray[route_short_name_pos]
                    route_long_name = lineArray[route_long_name_pos]
                    route_type = lineArray[route_type_pos]

                    # Eintrag in MySQL Tabelle
                    sql = '''
                        INSERT INTO routes
                        (
                            route_id,
                            agency_id,
                            route_short_name,
                            route_long_name,
                            route_type
                        )
                        VALUES (%s, %s, %s, %s, %s)
                    '''
                    mycursor.execute(sql, [route_id,
                                           agency_id,
                                           route_short_name,
                                           route_long_name,
                                           route_type])

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
