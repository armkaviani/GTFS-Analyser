'''
Zusammenfassung eines Feed-Reports

Input: Der Name einer Report-Datei. Der Inhalt hat diese Form:

gtfs-feed: feedname
==========
table: agency
lines: 47
field: agency_id
field: agency_name
field: agency_url
field: agency_timezone
field: agency_lang
----------
table: calendar
lines: 624
... usw.

Output: Datei "report_short_feedname.tab"
        mit diesem Inhalt (Tabulator getrennt):
feed    feedname
agency  47
stops   23M
routes  175k
... usw. 

Version: 2021-05-06 ... Version 005

'''

from time import time
import os
from pathlib import Path
import sys
from sys import exit

class ReportAnalyzer :
    
    ## Constructor
    #def __init__(self, report_filename) :
    #    self.report_filename = report_filename

    def process(self, report_input) :
        
        # prepare some values and data structures
        tables = [
            "agency", "stops", "routes", "trips", "stop_times",
            "calendar", "calendar_dates", "fare_attributes",
            "fare_rules", "shapes", "frequencies", "transfers",
            "feed_info", "translations", "attributions", "levels",
            "pathways"
            ]
        
        table_size_dict = {}   # create a new dictionary

        # read values from input file
        gtfs_feed = ""
        lines = 0
        table = ""        
        with open(report_input, encoding="utf-8-sig") as inputf:
            for line in inputf:
                line = line.strip()
                if line.startswith("gtfs-feed:") :
                    gtfs_feed = line[11:]
                if line.startswith("lines:") :
                    lines = line[7:]
                if line.startswith("table:") :
                    table = line[7:]       
                if line.startswith("------") :
                    #print("%s , %s , %s" %(gtfs_feed, lines, table))
                    
                    table_size_dict[table] = lines
                    lines = 0
                    table = ""
        
        # write output file
        report_output = "report_short_%s.tab" % gtfs_feed
        with open(report_output, 'w', encoding="utf-8") as outputf:
            outputf.write("feed\t%s\n" %gtfs_feed)
            for t in tables :
                if t in table_size_dict :
                    n = self.short_number_of(table_size_dict[t])
                    outputf.write("%s\t%s\n" %(t, n))
                else :
                    outputf.write("%s\t%s\n" %(t, "---"))
                    
    def short_number_of(self, int_number) :
        n = int(int_number)
        if(n >= 1000000000) :
            return str(round(n/1000000000)) + "G"
        elif(n >= 1000000) :
            return str(round(n/1000000)) + "M"
        elif(n >= 1000) :
            return str(round(n/1000)) + "k"
        else :
            return n
    
def main() :
    #### Values
    report_input_filename = "gtfs-feed-report_test.txt"
        
    #### Action Start
    print("Start analyzing.")
    start_time = time()
    
    # if exists, use program parameter as report_filename value
    arguments_number = len(sys.argv) - 1
    if(arguments_number == 1) :
        report_input_filename = sys.argv[1]
    
    report_analyzer_object = ReportAnalyzer()
    report_analyzer_object.process(report_input_filename)
    
    #### Action Finish
    duration = time() - start_time
    print("Report %s ready after %.2f seconds"
          %(report_input_filename, duration))

if __name__ == "__main__" :
    main()
