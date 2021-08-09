import wget
import os


class FeedDownloader:
    def __init__(self, UrlFeed, ZipFileName):
        """

        :param UrlFeed:         Url of gtfs feeds
        :param ZipFileName:     The name of zip file to save data from url to it
        """
        self.UrlFeed = UrlFeed
        self.ZipFileName = ZipFileName

    def Downloader(self):
        if os.path.exists(self.ZipFileName):
            os.remove(self.ZipFileName)

        wget.download(self.UrlFeed, self.ZipFileName)
