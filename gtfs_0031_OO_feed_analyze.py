"""
Analyse der Text-Dateien in einem entpackten GTFS Feed

Input: Das Verzeichnis mit den Text-Dateien eines entpackten GTFS-Feeds
    gtfs_feed (relativ zum Python-Programm)

Version: 2021-05-06 ... Version 008

"""

from time import time
import os
from pathlib import Path
import sys
from sys import exit


class FeedAnalyzer:

    # Constructor
    def __init__(self, unzip_path):
        self.unzip_path = unzip_path

        self.files = os.listdir(self.unzip_path)
        print("This GTFS dataset has got %d tables."
              % len(self.files))
        print("===================================")

    def directory_content(self):
        ''' Gets a list (array) of the filenames of self.unzipPath
        returns: fullFileNamesList
        '''
        files = os.listdir(self.unzip_path)

        full_file_names_list = []
        for _file in files:
            full_path_name = os.path.join(self.unzip_path, _file)
            full_file_names_list.append(full_path_name)

        return full_file_names_list

    def report_file_writer(self, report_filename):
        # Open report file, write the report
        with open(report_filename, 'w', encoding="utf-8") as f:
            f.write("gtfs-feed: %s\n" % self.unzip_path)
            f.write("==========\n")
            # Jede GTFS Tabelle lesen, Daten ermitteln, in Report schreiben
            objFileAnalyzer = FileAnalyzer()
            for _file in self.directory_content():

                # Objekt der Klasse File_Analyzer herstellen, Analyse starten                
                objFileAnalyzer.set_path(_file)
                objFileAnalyzer.line_analyze()

                f.write("table: %s\n" % str(objFileAnalyzer.table_name))
                f.write("lines: %s\n" % str(objFileAnalyzer.dataline_number))

                for field_name in objFileAnalyzer.fields_array:
                    field_name = field_name.strip()
                    if field_name != "":
                        f.write("field: %s\n" % field_name)
                f.write("----------\n")


class FileAnalyzer:

    ## There is no Constructor
    # def __init__(...) : ...

    def set_path(self, _file_path):
        self.file_path = _file_path

    def line_analyze(self):
        ''' Gets the data line number of the file self.file_path
            (without header line)
            sets class value:
                self.table_name ... Name of the table (from filename)
                self.dataline_number ... number of lines without first line                        
                self.fields_array ... Array of fieldnames of the table
        returns: nothing
        '''
        # print("TEST Counting lines in %s" % self.file_path)

        # get the pure filename without the path
        pure_filename = os.path.split(self.file_path)[1]
        self.table_name = pure_filename.split(".")[0]

        # line-count
        lines_number = sum(1 for line in open(self.file_path, 'r+',
                                              encoding="utf-8-sig"))
        self.dataline_number = lines_number - 1  # without table header

        print("%i data lines in table:" % self.dataline_number)
        print("%s" % self.table_name)
        print("----------")

        # Read the first line of the text file, containing the fieldnames
        # (encoding "utf-8-sig" skips BOM)
        with open(self.file_path, "r", encoding="utf-8-sig") as file:
            line = file.readline()  # Read the first line
        # print("TEST: First line of the text file %s" % line)  # Test

        line = line.replace('"', '')  # removes " in "service_id" etc.
        self.fields_array = line.split(",")

        for fieldname in self.fields_array:
            print("%s" % fieldname)  # Test


def main():
    #### Values
    unzip_path = "gtfs_feed"

    #### Action Start
    print("Start analyzing.")
    start_time = time()

    # if exists, use program parameter as unzip_path value
    arguments_number = len(sys.argv) - 1
    if arguments_number == 1:
        unzip_path = sys.argv[1]

    feed_analyzer_object = FeedAnalyzer(unzip_path)

    # create report filename, write report into file 
    report_filename = "report_%s.txt" % unzip_path
    feed_analyzer_object.report_file_writer(report_filename)

    #### Action Finish
    duration = time() - start_time
    print("Report %s ready after %.2f seconds"
          % (report_filename, duration))


if __name__ == "__main__":
    main()
