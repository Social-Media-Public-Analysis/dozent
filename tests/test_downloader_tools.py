import unittest
from os.path import exists
from os import mkdir
from shutil import rmtree
from dozent.downloader_tools import DownloaderTools

from pySmartDL import SmartDL
from pySmartDL.control_thread import ControlThread
from collections import namedtuple
import threading

DownloadProgress = namedtuple("DownloadProgress", "dl_size filesize speed status")


class DownloaderToolsTestCase(unittest.TestCase):
    def tearDown(self) -> None:
        if exists("test_downloader_dir"):
            rmtree("test_downloader_dir")

    def test_make_progress_status(self):

        url = "https://www.google.com/"

        # We want to initialize the SmartDL object without actually starting the download
        downloader_obj = SmartDL(url)
        downloader_obj.post_threadpool_thread = threading.Thread(target=lambda: None)

        control_thread = ControlThread(downloader_obj)
        downloader_obj.control_thread = control_thread

        for progress in [
            DownloadProgress(dl_size=0, filesize=0, speed=0, status="ready"),
            DownloadProgress(dl_size=1024, filesize=1048576, speed=42, status="downloading"),
            DownloadProgress(dl_size=129864, filesize=129865, speed=777, status="paused"),
            DownloadProgress(dl_size=999999, filesize=999999, speed=999, status="finished"),
        ]:
            assert progress.speed < 1000

            # We create faked download progress to test the output
            downloader_obj.shared_var.value = progress.dl_size << 20
            downloader_obj.filesize = progress.filesize << 20
            downloader_obj.status = progress.status
            control_thread.dl_speed = progress.speed
            progress_percentage = 100.0 * progress.dl_size / progress.filesize if progress.filesize else 0

            expected_speed = progress.speed if progress.status != "paused" else 0

            expected_prefix = (
                f"[{progress.status}] {progress.dl_size}Mb/{progress.filesize}Mb "
                f"@{expected_speed} {'B' if expected_speed else 'bytes'}/s"
            )

            expected_suffix = f"[{int(progress_percentage):3.0f}%, {0:3.0f}sec left]"

            actual_progress_percentage, actual_prefix, actual_suffix = DownloaderTools._make_progress_status(downloader_obj)

            self.assertAlmostEqual(progress_percentage, actual_progress_percentage)
            self.assertEqual(expected_prefix, actual_prefix)
            self.assertEqual(expected_suffix, actual_suffix)

    def test_singleton(self):
        try:
            downloader_1 = DownloaderTools()
            downloader_2 = DownloaderTools()
            self.assertTrue(False)
        except RuntimeError:
            self.assertTrue(True)

    def test_download_with_pysmartdl(self):
        mkdir("test_downloader_dir")

        DownloaderTools.download_with_pysmartdl(
            link="http://ipv4.download.thinkbroadband.com/20MB.zip", download_dir="test_downloader_dir", task_id=0
        )

        self.assertTrue(exists("test_downloader_dir/20MB.zip"))


if __name__ == "__main__":
    unittest.main()
