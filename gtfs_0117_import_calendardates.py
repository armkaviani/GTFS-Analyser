'''
Create table "calendar_dates" and import "calendar_dates.txt" from feed path "databasename".
Usage:
    python gtfs_0117_import_calendardates.py databasename
    
"calendar_dates.txt" contains these fields:
    service_id
    exception_type
    date

Version: 2021-07-06 ... Version 004
'''

import mysql.connector
import csv
from time import time
import sys
from sys import exit
import gtfs_0100_my_db_auth

def main() :
    
    import gtfs_0100_my_db_auth
    db_username = gtfs_0100_my_db_auth.db_username
    db_password = gtfs_0100_my_db_auth.db_password
    db_name = gtfs_0100_my_db_auth.db_name # Test with this databasename

    # Read one program parameter. This is the feed path AND database name.
    arguments_number = len(sys.argv) - 1
    if(arguments_number == 1) :
        db_name = sys.argv[1]
    else :
        print ("ERROR: missing parameter 'databasename == feedpath'.")    
        #exit(1)   # Exit the programm with error code "1"        
        
    #### Values
    fileName = db_name + "/calendar_dates.txt"  # file from feed path "db_name"

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
    sql = "DROP TABLE IF EXISTS calendar_dates"
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE IF NOT EXISTS calendar_dates
    (
        service_id VARCHAR(50),
        exception_type TINYINT(2) NOT NULL,
        date DATE NOT NULL,
        PRIMARY KEY(service_id, date)
    )
    '''
    mycursor.execute(sql)

    #### Read the text file line by line, import each line
    n = m = 0   # n is the line counter
    firstLine = True
    with open(fileName, "r", encoding="utf-8-sig") as file :  # "utf-8-sig" removes BOM
        
        reader = csv.reader(file)
        for row in reader:
            #print("TEST row=" + str(row))  # TEST
        
            if firstLine == True :
                firstLine = False
                # Read the first line - the table header
                headerLineArray = row
                #print("TEST: Header-Array = " + str(headerLineArray))
                field_number = len(headerLineArray) 
                
                # Find the position of all the fields of the table
                service_id_pos = -1
                exception_type_pos = -1
                date_pos = -1
                if "service_id" in headerLineArray:
                    service_id_pos = headerLineArray.index("service_id")
                if "exception_type" in headerLineArray:
                    exception_type_pos = headerLineArray.index("exception_type")
                if "date" in headerLineArray:
                    date_pos = headerLineArray.index("date")
            else :
                
                # Read the data of a line into an array
                lineArray = row
                if len(lineArray) >= field_number :
                    service_id = lineArray[service_id_pos]        
                    exception_type = lineArray[exception_type_pos]
                    date = lineArray[date_pos]        
                    
                    # Eintrag in MySQL Tabelle
                    sql = '''
                        INSERT INTO calendar_dates
                        (
                            service_id,
                            exception_type,
                            date
                        )
                        VALUES (%s, %s, %s)
                    '''
                    mycursor.execute(sql, [service_id,
                                           exception_type,
                                           date])

                    n = n + 1

                    # Progress-feedback every 10.000 lines
                    #m = m + 1 
                    #if m >= 10000 :
                    #    m = 0
                    #    print("  Progress: %s" % n)
                
    
    # Altering tables requires commit. It is faster 
    #   doing this only one time, at the very end.
    mydb.commit() 

    duration = time() - start_time
    print("Import OK ... %s rows in %.2f seconds" % (n, duration))

main()
