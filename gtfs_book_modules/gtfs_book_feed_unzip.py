'''
Modul: Unzip of a ZIP file of a GTFS-Feed.

If the script runs allone:
  The ZIP file tmp_latest_gtfs.zip will be unzipped into folder
  gtfs_feed (relatively to script folder)

Version: 2021-04-03 ... Version 002
'''

from time import time
import zipfile
from pathlib import Path
import shutil

class Unzip:
    def unzipper(self, unzip_path, zip_file_name) :
        ''' Unzip the ZIP file 'zip_file_name'
            into a fresh created path 'unzip_path'
            returns: nothing
        '''
        self.zip_file_name = zip_file_name
        self.unzip_path = unzip_path
        
        with zipfile.ZipFile(self.zip_file_name, 'r') as extract_File:
            
            # Lösche das bestehende Unterverzeichnis mit den alten Daten
            try :
                shutil.rmtree(self.unzip_path)
            except OSError as e:
                # Wenn das Unterverzeichnis nicht gelöscht werden konnte, hat es evtl. nicht existiert.
                print("INFO: %s --> Creating a new path: %s."
                      %(e.strerror, self.unzip_path))
                
            # Entpacke die ZIP-Datei
            Path(self.unzip_path).mkdir(parents=True, exist_ok=True)
            extract_File.extractall(self.unzip_path)

def main():
    #### Values
    gtfsFeedFileName = "tmp_latest_gtfs.zip"
    unzip_path = "gtfs_feed"
        
    #### Action Start
    print("Start unzip.")
    start_time = time()

    unzip_object = Unzip()
    unzip_object.unzipper(unzip_path, gtfsFeedFileName)
    
    #### Action Finish
    duration = time() - start_time
    print("Unzip finished after %.2f seconds." %duration)

if __name__ == "__main__" :
    main()

   