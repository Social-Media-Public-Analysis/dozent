import time
import sys
from typing import Tuple
from threading import Lock
from pySmartDL import SmartDL
# Used for tracking and displaying download progress bars
global global_progress_tracker
global_progress_tracker = [(0, 0, "0", 0, "0")]
global global_download_size
global_download_size = 0
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
    def _get_individual_download_stats(
            downloader_obj: SmartDL,
    ) -> Tuple[int, int, str, float, str]:
        download_size = downloader_obj.get_dl_size() >> 20
        file_size = downloader_obj.get_final_filesize() >> 20
        speed = downloader_obj.get_speed()
        progress_percentage = downloader_obj.get_progress()
        eta = downloader_obj.get_eta()
        return download_size, file_size, speed, progress_percentage, eta
    @staticmethod
    def _update_global_download_size() -> int:
        global global_download_size
        for download in global_progress_tracker:
            global_download_size += download[0]
    @staticmethod
    def _get_final_download_size() -> int:
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
    ):
        """
        Downloads file from link using PySmartDL
        :param link: link that needs to be downloaded
        :param download_dir: A relative path to the download directory
        """
        global global_progress_tracker
        if (len(global_progress_tracker) == 1) and (number_of_dates > 1):
            global_progress_tracker = global_progress_tracker * number_of_dates
        downloader_obj = SmartDL(link, download_dir, progress_bar=False)
        downloader_obj.start(blocking=False)
        while not downloader_obj.isFinished():
            if verbose:
                lock = Lock()
                lock.acquire()
                global_progress_tracker[task_id] = cls._get_individual_download_stats(
                    downloader_obj
                )
                cls._update_global_download_size()
                sys.stdout.write(f"{global_download_size} \r")
                sys.stdout.flush()
                lock.release()
            # Sleep for a random interval between 0.01 and 0.25 seconds
            time.sleep(.25)
