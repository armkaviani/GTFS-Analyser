'''
Applikation: Download und Unzip eines GTFS-Feeds
Usage: python gtfs_app_download_unzip.py
                      https://feedurl/feed.zip unzippath
    
Version: 2021-05-06 ... Version 003 
'''
import sys
from time import time
from gtfs_book_modules import gtfs_book_feed_download
from gtfs_book_modules import gtfs_book_feed_unzip

def main():
    #### Default Values
    feed_url = "https://download.gtfs.de/germany/fv_free/latest.zip"
    unzip_path = "gtfs_feed_01"
    tmp_zip_file_name = "tmp_latest_gtfs.zip"

    #### Action Start
    arguments_number = len(sys.argv) - 1
    if(arguments_number < 2) :
        print("Usage: python %s feed_url unzip_path" %sys.argv[0])
        print("WARNING: 2 arguments expected, found only %s." %arguments_number)
        print("         Using standard feed_url and unzip_path.")
    else :
        feed_url = sys.argv[1]
        unzip_path = sys.argv[2]
    
    print("Download from: %s." %feed_url)
    print("Unzip into: %s." %unzip_path)
    
    print("Start action.")
    start_time = time()

    downloaderObj = gtfs_book_feed_download.Downer()
    downloaderObj.download(feed_url, tmp_zip_file_name)
    
    duration = time() - start_time
    print("Download finished after %.2f seconds." %duration) 

    unzipperObject = gtfs_book_feed_unzip.Unzip()
    unzipperObject.unzipper(unzip_path, tmp_zip_file_name)

    duration = time() - start_time
    
    #### Action Finish
    print("Everything finished after %.2f seconds." %duration)

main()
   