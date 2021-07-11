'''
Create table "calendar" and import "calendar.txt" from feed path "databasename".
Usage:
    python gtfs_0117_import_calendardates.py databasename
    
"calendar.txt" contains these fields:
    service_id
    monday
    tuesday
    wednesday
    thursday
    friday
    saturday
    sunday
    start_date
    end_date

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
    fileName = db_name + "/calendar.txt"  # file from feed path "db_name"

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
    sql = "DROP TABLE IF EXISTS calendar"
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE IF NOT EXISTS calendar
    (
        service_id VARCHAR(50) PRIMARY KEY,
        monday TINYINT(1),
        tuesday TINYINT(1),
        wednesday TINYINT(1),
        thursday TINYINT(1),
        friday TINYINT(1),
        saturday TINYINT(1),
        sunday TINYINT(1),
        start_date DATE,
        end_date DATE
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
                if "monday" in headerLineArray:
                    monday_pos = headerLineArray.index("monday")
                if "tuesday" in headerLineArray:
                    tuesday_pos = headerLineArray.index("tuesday")
                if "wednesday" in headerLineArray:
                    wednesday_pos = headerLineArray.index("wednesday")
                if "thursday" in headerLineArray:
                    thursday_pos = headerLineArray.index("thursday")
                if "friday" in headerLineArray:
                    friday_pos = headerLineArray.index("friday")
                if "saturday" in headerLineArray:
                    saturday_pos = headerLineArray.index("saturday")
                if "sunday" in headerLineArray:
                    sunday_pos = headerLineArray.index("sunday")                  
                if "start_date" in headerLineArray:
                    start_date_pos = headerLineArray.index("start_date")
                if "end_date" in headerLineArray:
                    end_date_pos = headerLineArray.index("end_date")
            else :
                
                # Read the data of a line into an array
                lineArray = row
                if len(lineArray) >= field_number :
                    service_id = lineArray[service_id_pos]        
                    monday = lineArray[monday_pos]
                    tuesday = lineArray[tuesday_pos]
                    wednesday = lineArray[wednesday_pos]
                    thursday = lineArray[thursday_pos]
                    friday = lineArray[friday_pos]
                    saturday = lineArray[saturday_pos]
                    sunday = lineArray[sunday_pos]
                    start_date = lineArray[start_date_pos]
                    end_date = lineArray[end_date_pos]

                    # Eintrag in MySQL Tabelle
                    sql = '''
                        INSERT INTO calendar
                        (
                            service_id,
                            monday,
                            tuesday,
                            wednesday,
                            thursday,
                            friday,
                            saturday,
                            sunday,
                            start_date,
                            end_date
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    '''
                    mycursor.execute(sql, [service_id,
                                           monday,
                                           tuesday,
                                           wednesday,
                                           thursday,
                                           friday,
                                           saturday,
                                           sunday,
                                           start_date,
                                           end_date])

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
