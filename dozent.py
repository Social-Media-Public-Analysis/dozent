import datetime
import json
import multiprocessing
import os
import time
from queue import Queue
from threading import Thread
from typing import List

try:
    from downloader_tools import DownloaderTools, ProgressTracker
except ModuleNotFoundError:
    from .downloader_tools import DownloaderTools, ProgressTracker


class _DownloadWorker(Thread):

    def __init__(self, queue: Queue, download_dir: str, tracker: ProgressTracker = None):
        Thread.__init__(self)
        self.queue = queue
        self.download_dir = download_dir
        self.tracker = tracker

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            link = self.queue.get()
            try:
                DownloaderTools.download_pysmartdl(link, self.download_dir, tracker=self.tracker)
            finally:
                self.queue.task_done()


class Dozent:

    @staticmethod
    def get_archives_in_date_interval(start_date: datetime.datetime,
                                      end_date: datetime.datetime, file_path: str = None) -> List[str]:
        """
        Parse out the download links for archives in a given date interval.

        :param start_date: Beginning date of range to filter results.
        :param end_date: End date of range to filter results.
        :param file_path: The path to a json file containing the archive link data, defaults to None.
                          If None is provided, "__file__/twitter-archive-stream-links.json" will be used

        :return: The list of url links.

        :raises ValueError: Raised when the end_date exceeds the maximum date of: June 1, 2017.
        """

        if end_date > datetime.datetime(2017, 6, 1):
            raise ValueError(f'Specified end_date is out of range: {end_date} (>{datetime.datetime(2017, 6, 1)})')

        if file_path is None:
            file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'twitter-archive-stream-links.json')

        with open(file_path) as file:
            data = json.loads(file.read())

        start_index = data.index(
            next(filter(lambda link: (int(link['month']) == start_date.month) and
                                     (int(link['year']) == start_date.year), data)))
        end_index = data.index(
            next(filter(lambda link: (int(link['month']) == end_date.month) and
                                     (int(link['year']) == end_date.year), data)))

        return [sample_date['link'] for sample_date in data[start_index:end_index]]

    @staticmethod
    def download_timeframe(start_date: datetime.datetime,
                           end_date: datetime.datetime,
                           verbose: bool = True,
                           download_dir: str = './data'):
        """
        Download all tweet archives from start_date to end_date
        :param verbose: Show verbose output, defaults to True
        :param download_dir: A relative path to the download directory, defaults to './data'
        :return: None
        """

        links = Dozent.get_archive_links_in_date_interval(start_date, end_date)

        # Create a queue to communicate with the worker threads
        queue = Queue()
        if verbose:
            tracker = ProgressTracker()
            tracker.daemon = True
            tracker.start()
        else:
            tracker = None

        os.makedirs(download_dir, exist_ok=True)

        for x in range(multiprocessing.cpu_count()):
            worker = _DownloadWorker(queue, download_dir, tracker=tracker)
            # Setting daemon to True will let the main thread exit even though the workers are blocking
            worker.daemon = True
            worker.start()

        # Put the tasks into the queue
        for link in links:
            queue.put(link)

        queue.join()
        tracker.join()


if __name__ == "__main__":
    from catch_thread_exceptions import install as _catch_thread_exceptions
    _catch_thread_exceptions()

    _start_time = time.time()
    Dozent.download_timeframe(datetime.datetime(2011, 9, 1), datetime.datetime(2016, 10, 1))
    print(f"Download Time: {datetime.timedelta(seconds=(time.time() - _start_time))}")
