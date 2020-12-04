import multiprocessing
import os
import time
from typing import Tuple

from pySmartDL import SmartDL

try:
    from dozent.progress_tracker import ProgressTracker
except ModuleNotFoundError:
    from .progress_tracker import ProgressTracker


class DownloaderTools:
    __instance__ = None

    def __init__(self):
        if DownloaderTools.__instance__ is None:
            DownloaderTools.__instance__ = self

        else:
            raise RuntimeError(f"Singleton {self.__class__.__name__} class is created more than once!")

    @staticmethod
    def _make_progress_status(downloader_obj: SmartDL) -> Tuple[float, str, str]:
        """Function to make progress bar

        :param downloader_obj: SmartDL object that's currently downloading a file
        :return: the progress percentage in [0,100] and a string prefix/suffix to be output before/after a progress bar.
        """

        status = downloader_obj.get_status()
        filesize = downloader_obj.get_final_filesize() >> 20

        try:
            dl_size = downloader_obj.get_dl_size() >> 20
            speed = downloader_obj.get_speed(human=True)
            eta = downloader_obj.get_eta(human=True)
            progress_percentage = 100.0 * downloader_obj.get_progress()

            eta = eta.split(',')[0]
            eta_parts = eta.split(' ')
            eta_unit = eta_parts[1][:3]
            if eta_unit == 'hou':
                eta_unit = 'hrs'
            eta = f"{float(eta_parts[0]):3.0f}{eta_unit}"

        except AttributeError:
            dl_size = 0
            speed = ''
            eta = ''
            progress_percentage = 0

        prefix = f"[{status}] {dl_size}Mb/{filesize}Mb {f'@{speed}' if speed else ''}"
        suffix = f"[{int(progress_percentage):3.0f}%{f', {eta} left' if eta else ''}]"

        return progress_percentage, prefix, suffix

    @classmethod
    def download_with_pysmartdl(cls, link: str, download_dir: str, tracker: ProgressTracker = None):
        """
        Downloads file from link using PySmartDL

        :param link: link that needs to be downloaded
        :param download_dir: A relative path to the download directory
        :param tracker: Used to track progress, defaults to None
        """

        downloader_obj = SmartDL(link, download_dir, progress_bar=False)

        task_id = None
        if tracker:
            task_id = tracker.register_task(link, lambda: DownloaderTools._make_progress_status(downloader_obj))

        downloader_obj.start(blocking=False)

        while not downloader_obj.isFinished():
            if task_id is not None:
                tracker.update(task_id)
            time.sleep(.25)

    @classmethod
    def download_with_axel(cls, link: str):  # skip_tests: Only possible on Ubuntu and depreciated
        """Downloads file from link using axel

        :param link: link that needs to be downloaded
        :return: None
        """
        os.system(f"axel --verbose --alternate --num-connections={cls._connections_count} {link}")

    @classmethod
    def download_with_aria2(cls, link: str):  # skip_tests: Only possible on Ubuntu and depreciated
        """
        Downloads file from link using aria2
        :param link: link that needs to be downloaded
        """
        os.system(f"aria2c -x {cls._connections_count} {link}")

    _connections_count = 2 * multiprocessing.cpu_count()

    _downloaders = {
        'pySmartDL': download_with_pysmartdl.__func__,
        'Axel': download_with_axel.__func__,
        'aria2': download_with_aria2.__func__
    }
