import zipfile
from pathlib import Path
import shutil
import os


class FeedUnzipper:
    def __init__(self, UnzipPath, ZipFileName):
        """

        :param UnzipPath:       Path to directory to save unzipped data
        :param ZipFileName:     Path to zip file
        """
        self.UnzipPath = UnzipPath
        self.ZipFileName = ZipFileName

    def Unzipper(self):
        """
        Unzip the ZIP file 'zip_file_name' into a fresh created path 'unzip_path' returns: nothing

        """
        with zipfile.ZipFile(self.ZipFileName, 'r') as ExtractFile:
            try:
                shutil.rmtree(self.UnzipPath)
            except OSError as e:
                print("INFO: %s --> Creating a new path: %s."
                      % (e.strerror, self.UnzipPath))

            # Unpack the zip data
            Path(self.UnzipPath).mkdir(parents=True, exist_ok=True)
            ExtractFile.extractall(self.UnzipPath)
