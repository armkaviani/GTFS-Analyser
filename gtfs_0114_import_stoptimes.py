'''
Create table "stop_times" and import "stop_times.txt" from feed path "databasename".
Usage:
    python gtfs_0114_import_stoptimes.py databasename
    
"stop_times.txt" contains these fields:
    trip_id
    arrival_time
    departure_time
    stop_id
    stop_sequence

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
    fileName = db_name + "/stop_times.txt"  # file from feed path "db_name"

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
    sql = "DROP TABLE IF EXISTS stop_times"
    mycursor.execute(sql)

    # mycursor = mydb.cursor()
    sql = '''
    CREATE TABLE IF NOT EXISTS stop_times
    (
        trip_id VARCHAR(50) NOT NULL,
        arrival_time TIME NOT NULL,
        departure_time TIME NOT NULL,
        stop_id VARCHAR(50) NOT NULL,
        stop_sequence INT UNSIGNED
    )
    '''
    mycursor.execute(sql)

    # REMARK: Having an index in the table slows the "INSERT INTO" down.
    #        Better: adding the index after all "INSERT INTO".

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
                arrival_time_pos = -1
                departure_time_pos = -1
                stop_id_pos = -1
                stop_sequence_pos = -1
                if "trip_id" in headerLineArray:
                    trip_id_pos = headerLineArray.index("trip_id")
                if "arrival_time" in headerLineArray:
                    arrival_time_pos = headerLineArray.index("arrival_time")
                if "departure_time" in headerLineArray:
                    departure_time_pos = headerLineArray.index("departure_time")
                if "stop_id" in headerLineArray:
                    stop_id_pos = headerLineArray.index("stop_id")
                if "stop_sequence" in headerLineArray:
                    stop_sequence_pos = headerLineArray.index("stop_sequence")
            else:

                # Read the data of a line into an array
                lineArray = row
                if len(lineArray) >= field_number:
                    trip_id = lineArray[trip_id_pos]
                    arrival_time = lineArray[arrival_time_pos]
                    departure_time = lineArray[departure_time_pos]
                    stop_id = lineArray[stop_id_pos]
                    stop_sequence = lineArray[stop_sequence_pos]

                    # Eintrag in MySQL Tabelle
                    sql = '''
                        INSERT INTO stop_times
                        (
                            trip_id,
                            arrival_time,
                            departure_time,
                            stop_id,
                            stop_sequence
                        )
                        VALUES (%s, %s, %s, %s, %s)
                    '''
                    mycursor.execute(sql, [trip_id,
                                           arrival_time,
                                           departure_time,
                                           stop_id,
                                           stop_sequence])
                    n = n + 1

                    # Progress-feedback every 10.000 lines
                    # m = m + 1
                    # if m >= 10000 :
                    #    m = 0
                    #    print("  Progress: %s" % n)

    # Altering tables requires commit. It is faster 
    #   doing this only one time, at the very end.
    mydb.commit()

    # Create index
    sql = '''
    CREATE INDEX idx_trip_id
    ON stop_times (trip_id);
    
    CREATE INDEX idx_stop_id
    ON stop_times (stop_id);
    '''
    # SQL has multiple statements, so we loop the "mycursor.execute(sql)"
    for result in mycursor.execute(sql, multi=True):
        pass

    duration = time() - start_time
    print("Import OK ... %s rows in %.2f seconds" % (n, duration))


main()
