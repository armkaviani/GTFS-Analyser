from time import time
import wget
import os


class FeedDownloader:
    def __init__(self, UrlFeed, ZipFileName):
        self.UrlFeed = UrlFeed
        self.ZipFileName = ZipFileName

    def Downloader(self):
        if os.path.exists(self.ZipFileName):
            os.remove(self.ZipFileName)

        wget.download(self.UrlFeed, self.ZipFileName)

