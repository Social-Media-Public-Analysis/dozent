import sys
import time
import random
from threading import Lock

from pySmartDL import SmartDL

SUFFIXES = ["B", "KB", "MB", "GB", "TB", "PB"]

# Used for tracking and displaying download progress bars
global global_progress_tracker
global_progress_tracker = [[0, 0, 0, 0, 0]]

global global_download_size
global_download_size = 0

global global_final_download_size
global_final_download_size = 0

global global_download_speed
global_download_speed = 0

global global_progress_percentage
global_progress_percentage = 0


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
        """
        Updates download progress for all downloads
        """
        global global_download_size
        updated_size = sum([index[0] for index in global_progress_tracker])

        # Prevents lagging threads from updating with lower values
        if updated_size > global_download_size:
            global_download_size = updated_size

    @staticmethod
    def _get_final_download_size() -> int:
        """
        Retrieves the total download size for all downloads
        :return: total download size in bytes
        """
        global_final_download_size = 0
        for download in global_progress_tracker:
            global_final_download_size += download[1]
        return global_final_download_size

    @staticmethod
    def _update_global_download_speed() -> None:
        """
        Updates global download speed for all downloads
        """
        global global_download_speed

        download_speeds = [int(index[2]) for index in global_progress_tracker]
        global_download_speed = int(sum(download_speeds) / len(download_speeds))

    @staticmethod
    def _update_global_progress_percentage() -> None:
        """
        Updates global progress percentage for all downloads
        """
        global global_progress_percentage

        updated_percentage = [float(index[3]) for index in global_progress_tracker]
        updated_percentage = round(
            float(sum(updated_percentage) / len(updated_percentage) * 100), 2
        )

        # Prevents lagging threads from updating with lower values
        if updated_percentage > global_progress_percentage:
            global_progress_percentage = updated_percentage

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
                cls._update_global_download_speed()
                cls._update_global_progress_percentage()

                sys.stdout.write(f"{global_progress_tracker}\n")

                sys.stdout.flush()
                lock.release()
            # Sleep for a random interval between 250 to 500 milliseconds
            time.sleep((random.random() / 4) + 0.25)
