import sys
import time
from threading import Lock
import numpy as np

from pySmartDL import SmartDL

SUFFIXES = ["B", "KB", "MB", "GB", "TB", "PB"]

# Used for tracking and displaying download progress bars
global global_progress_tracker
global_progress_tracker = [[0, 0, "0", 0, "0"]]
global global_download_size
global_download_size = 0

global global_final_download_size
global_final_download_size = 0

import random


class DownloaderTools:
    __instance__ = None

    def __init__(self):
        if DownloaderTools.__instance__ is None:
            DownloaderTools.__instance__ = self
        else:
            raise RuntimeError(
                f"Singleton {self.__class__.__name__} class is created more than once!"
            )

    @staticmethod
    def _size(number_of_bytes: int) -> str:
        """
        Converts number of bytes into a human readable format
        :param number_of_bytes: link that needs to be downloaded
        :return: String representing number of bytes in human readable format
        """
        i = 0
        while number_of_bytes >= 1024 and i < len(SUFFIXES) - 1:
            number_of_bytes /= 1024.0
            i += 1
        human_readable_bytes = ("%.2f" % number_of_bytes).rstrip("0").rstrip(".")
        return f"{human_readable_bytes} {SUFFIXES[i]}"

    @staticmethod
    def _get_individual_download_stats(
        downloader_obj: SmartDL,
    ) -> [int, int, str, float, str]:

        download_size = downloader_obj.get_dl_size()
        file_size = downloader_obj.get_final_filesize()
        speed = downloader_obj.get_speed()
        progress_percentage = downloader_obj.get_progress()
        eta = downloader_obj.get_eta()
        return [download_size, file_size, speed, progress_percentage, eta]

    @staticmethod
    def _update_global_download_size() -> None:
        '''
        Updates download progress for all downloads
        '''
        global global_download_size
        global_download_size = sum([index[0]for index in global_progress_tracker])

    @staticmethod
    def _get_final_download_size() -> int:
        '''
        Retrieves the total download size for all downloads
        :return: total download size in bytes
        '''
        global_final_download_size = 0
        for download in global_progress_tracker:
            global_final_download_size += download[1]
        return global_final_download_size

    @classmethod
    def download_with_pysmartdl(
        cls,
        link: str,
        download_dir: str,
        task_id: int,
        number_of_dates: int,
        verbose: str = True,
    ) -> None:
        """
        Downloads file from link using PySmartDL
        :param link: link that needs to be downloaded
        :param download_dir: A relative path to the download directory
        :param task_id: ID of thread
        :verbose: Determines if download status is printed to console
        """
        global global_progress_tracker
        if (len(global_progress_tracker) == 1) and (number_of_dates > 1):
            global_progress_tracker = global_progress_tracker * number_of_dates
        downloader_obj = SmartDL(link, download_dir, progress_bar=False)
        downloader_obj.start(blocking=False)

        global global_final_download_size
        global_final_download_size += downloader_obj.get_final_filesize()

        while not downloader_obj.isFinished():
            if verbose:
                lock = Lock()
                lock.acquire()
                global_progress_tracker[task_id] = cls._get_individual_download_stats(
                    downloader_obj
                )
                cls._update_global_download_size()
                sys.stdout.write(
                    f" {cls._size(global_download_size)} / {cls._size(global_final_download_size)}    \r"
                )
                sys.stdout.flush()
                lock.release()
            # Sleep for a random interval between 0.01 and 0.25 seconds
            time.sleep(random.random() / 4)
