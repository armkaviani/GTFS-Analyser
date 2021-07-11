'''
Modul: Download of a ZIP file from a GTFS feed

If the script runs allone:
  The feed to be downloaded is:
    https://download.gtfs.de/germany/fv_free/latest.zip
  The filename of the download is: tmp_latest_gtfs.zip 

Version: 2021-04-03 ... Version 002
'''

from time import time
import wget
import os

class Downer:
    def download(self, feed_url, zip_file_name):

        self.feed_url = feed_url
        self.zip_file_name = zip_file_name

        ## Mit dem Modul wget genügt eine Anweisung zum Download 
        #wget.download(feedUrl, 'feedDownloaded.zip')

        # See: https://stackabuse.com/download-files-with-python/
        # -> With the requests module, you can also easily retrieve relevant meta-data about
        #    your request, including the status code, headers and much more. 
        # -> Das request-Modul ist auch im Buch vpm Al Sweigert "Routineaufgaben ..." vorgestellt

        #r = requests.get(feedUrl)
        ## Retrieve HTTP meta-data
        #print(r.status_code)
        #print(r.headers['content-type'])
        #print(r.encoding)
        #print(r.content)

        ## Das Modul urllib.request ist simple und genügt, um einfach nur die Datei (egal was) runterzuladen
        ## ... Wow: Ich musste dieses Modul in Thonny nicht importieren. Download überschreibt alte Datei.
        ##     Aber Note: This urllib.request.urlretrieve is considered a "legacy interface" seit Python 3.3
        #urllib.request.urlretrieve(feedUrl, 'download.zip')

        # Erlebnisse mit wget: Wenn es die Datei mit dem Namen feedDownloaded.zip
        # schon gibt, wird sie nicht überschrieben. Sondern: Es wird eine
        # neue Version gespeichert: feedDownloaded(1).zip, feedDownloaded(2).zip
        if os.path.exists(self.zip_file_name):
          os.remove(self.zip_file_name)   # Ein Download mit wget überschreibt die alte Datei nicht
        wget.download(self.feed_url, self.zip_file_name)

def main():
    #### Values
    feed_url = "https://download.gtfs.de/germany/fv_free/latest.zip"
    download_file_name = "tmp_latest_gtfs.zip"

    #### Action Start
    print("Start download GTFS feed from %s" %feed_url)
    start_time = time()
    
    gtfs_zip_file_object = Downer()
    gtfs_zip_file_object.download(feed_url, download_file_name)

    #### Action Finish
    duration = time() - start_time
    print("Download finished after %.2f seconds" %duration)

if __name__ == "__main__" :
    main()