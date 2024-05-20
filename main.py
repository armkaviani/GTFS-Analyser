'''
Applikation: Download und Unzip eines GTFS-Feeds
Usage: python main.py
                      https://feedurl/feed.zip unzippath
    
Version: 2021-05-06 ... Version 003 
'''
import sys
from time import time
from utilities import GTFSFeedUnzipper
from utilities import GTFSFeedDownloader
import argparse


def gtfsAnalyzer():
    UrlFeed = "https://download.gtfs.de/germany/fv_free/latest.zip"
    FilePath = "GTFSFeeds"

    TempZipFile = "TempZipFile.zip"

    parser = argparse.ArgumentParser()
    parser.add_argument('-u',
                        action='store',
                        dest='UrlFeed',
                        default="",
                        required=False,
                        help='Set url_feed Manager')

    parser.add_argument('-p',
                        action='store',
                        dest='FilePath',
                        default="",
                        required=False,
                        help='Set PathFile Manager')

    parser.add_argument('--version', action='version', version='1.0.0')
    results = parser.parse_args()

    if results.UrlFeed != "":
        UrlFeed = results.UrlFeed

    if results.FilePath != "":
        FilePath = results.FilePath

    print("Download from: %s." % UrlFeed)
    print("Unzip into: %s." % FilePath)

    print("Start action.")
    start_time = time()

    FeedDownloaderObj = GTFSFeedDownloader.FeedDownloader(UrlFeed, TempZipFile)
    FeedDownloaderObj.Downloader()

    duration = time() - start_time
    print("Download finished after %.2f seconds." % duration)

    FeedUnzipperObj = GTFSFeedUnzipper.FeedUnzipper(FilePath, TempZipFile)
    FeedUnzipperObj.Unzipper()

    duration = time() - start_time

    #### Action Finish
    print("Everything finished after %.2f seconds." % duration)


if __name__ == "__main__":
    gtfsAnalyzer()
