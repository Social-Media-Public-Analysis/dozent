import unittest
from collections import namedtuple
from os import mkdir
from os.path import exists
from shutil import rmtree

from dozent.downloader_tools import DownloaderTools

DownloadProgress = namedtuple('DownloadProgress', 'dl_size filesize speed status')


class DownloaderToolsTestCase(unittest.TestCase):

    def tearDown(self) -> None:
        if exists('test_downloader_dir'):
            rmtree('test_downloader_dir')

    def test_singleton(self):
        try:
            downloader_1 = DownloaderTools()
            downloader_2 = DownloaderTools()
            self.assertTrue(False)
        except RuntimeError:
            self.assertTrue(True)

    def test_download_with_pysmartdl(self):
        mkdir('test_downloader_dir')

        DownloaderTools.download_with_pysmartdl(link='http://ipv4.download.thinkbroadband.com/20MB.zip',
                                                download_dir='test_downloader_dir',
                                                task_id=0,
                                                number_of_dates=1,
                                                verbose=False
                                                )

        self.assertTrue(exists('test_downloader_dir/20MB.zip'))

if __name__ == "__main__":
    unittest.main()