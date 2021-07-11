'''
Create table "agency" and import "agency.txt" from feed path "databasename".
Usage:
    python gtfs_0111_import_agency.py databasename
    
"agency.txt" contains these fields:
    agency_id
    agency_name
    agency_url
    agency_timezone
    
Version: 2021-06-07 ... Version 004
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
    fileName = db_name + "/agency.txt"  # file from feed path "db_name"

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
    sql = "DROP TABLE IF EXISTS agency"
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE IF NOT EXISTS agency
    (  
        agency_id VARCHAR(50) PRIMARY KEY,
        agency_name VARCHAR(255),
        agency_url VARCHAR(255),
        agency_timezone VARCHAR(50)
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
                agency_id_pos = -1
                agency_name_pos = -1
                agency_url_pos = -1
                agency_timezone_pos = -1
                if "agency_id" in headerLineArray:
                    agency_id_pos = headerLineArray.index("agency_id")
                if "agency_name" in headerLineArray:
                    agency_name_pos = headerLineArray.index("agency_name")
                if "agency_url" in headerLineArray:
                    agency_url_pos = headerLineArray.index("agency_url")
                if "agency_timezone" in headerLineArray:
                    agency_timezone_pos = \
                            headerLineArray.index("agency_timezone")
                #print(agency_id_pos, agency_name_pos, agency_url_pos, agency_timezone_pos)  # TEST   
         
            else :
                
                # Read the data of a line into an array
                lineArray = row
                if len(lineArray) >= field_number :
                    agency_id = lineArray[agency_id_pos]        
                    agency_name = lineArray[agency_name_pos]
                    #print(agency_name)   # TEST
                    agency_url = lineArray[agency_url_pos]        
                    agency_timezone = lineArray[agency_timezone_pos]        
                   
                    # Eintrag in MySQL Tabelle
                    sql = '''
                        INSERT INTO agency
                        (
                            agency_id,
                            agency_name,
                            agency_url,
                            agency_timezone
                        )
                        VALUES (%s, %s, %s, %s)
                    '''
                    mycursor.execute(sql, [agency_id,
                                           agency_name,
                                           agency_url,
                                           agency_timezone])

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
