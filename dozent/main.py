import argparse
import datetime
import json
import multiprocessing
import os
import time
from pathlib import Path
from queue import Queue
from threading import Thread
from typing import List, Dict, Any

from dozent.downloader_tools import DownloaderTools
from dozent.progress_tracker import ProgressTracker

CURRENT_FILE_PATH = Path(__file__)
DEFAULT_DATA_DIRECTORY = CURRENT_FILE_PATH.parent.parent / 'data'
TWITTER_ARCHIVE_STREAM_LINKS_PATH = CURRENT_FILE_PATH.parent / 'twitter-archive-stream-links.json'

FIRST_DAY_OF_SUPPORT = datetime.date(2017, 6, 1)
LAST_DAY_OF_SUPPORT = datetime.date(2020, 6, 30)

class _DownloadWorker(Thread):  # skip_tests

    def __init__(self, queue: Queue, download_dir: Path, tracker: ProgressTracker = None):
        Thread.__init__(self)
        self.queue = queue
        self.download_dir = download_dir
        self.tracker = tracker

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            link = self.queue.get()
            try:
                DownloaderTools.download_with_pysmartdl(link, str(self.download_dir), tracker=self.tracker)
            finally:
                self.queue.task_done()


class Dozent:
    # TODO: Move start_date and end_date as optional arguments
    __instance__ = None

    def __init__(self):
        if Dozent.__instance__ is None:
            Dozent.__instance__ = self
            with open(TWITTER_ARCHIVE_STREAM_LINKS_PATH) as file:
                self.date_links: List[Dict[str, str]] = json.loads(file.read())

        else:
            raise RuntimeError(f"Singleton {self.__class__.__name__} class is created more than once!")

    @staticmethod
    def _make_date_from_date_link(date_link: Dict[str, str]) -> datetime.date:
        """
        Function to make a date given the date link. For months that don't have individual dates (date = 'NaN'), we
        assume that it's the first.
        :param date_link: date dictionary from `data/test_sample_files.json`. This is used to convert to the date
        :return: date object for the associated month
        """
        day = int(date_link['day']) if date_link['day'] != 'NaN' else 1
        month = int(date_link['month'])
        year = int(date_link['year'])

        return datetime.date(year=year, month=month, day=day)

    def get_links_for_days(self, start_date: datetime.date, end_date: datetime.date) -> List:
        """
        Function to get the links for the given start and end days
        :return: date dictionaries that are within self.start_date and self.end_dates
        """
        links = []

        if not FIRST_DAY_OF_SUPPORT >= start_date:
            RuntimeError(f'We currently only support the range {FIRST_DAY_OF_SUPPORT.strftime("%d, %b %Y")}, '
                         f'{LAST_DAY_OF_SUPPORT.strftime("%d, %b %Y")}'
                         f'\nWe\'re planning on adding support for it soon.'
                         f'Need that data sooner? Add an issue to out GitHub repo and we\'ll '
                         f'walk you through the process'
                         f'Link to our GitHub '
                         f'Issues: https://github.com/Twitter-Public-Analysis/Twitter-Public-Analysis/issues')

        elif not end_date <= end_date:
            RuntimeError(f'We currently only support the range {FIRST_DAY_OF_SUPPORT.strftime("%d, %b %Y")}, '
                         f'{LAST_DAY_OF_SUPPORT.strftime("%d, %b %Y")}'
                         f'\nWe\'re planning on adding support for it soon.'
                         f'Need that data sooner? Add an issue to out GitHub repo and we\'ll '
                         f'walk you through the process'
                         f'Link to our GitHub '
                         f'Issues: https://github.com/Twitter-Public-Analysis/Twitter-Public-Analysis/issues')

        for date_link in self.date_links:
            date = Dozent._make_date_from_date_link(date_link)
            if start_date <= date <= end_date:
                links.append(date_link)

        return links

    def download_timeframe(self, start_date: datetime.date, end_date: datetime.date, verbose: bool = True,
                           download_dir: Path = DEFAULT_DATA_DIRECTORY):
        """
        Download all tweet archives from self.start_date to self.end_date
        :return: None
        """

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
            # worker.set_verbosity(verbose=verbosity)
            # Setting daemon to True will let the main thread exit even though the workers are blocking
            worker.daemon = True
            worker.start()

        for sample_date in self.get_links_for_days(start_date=start_date, end_date=end_date):
            print(f"Queueing tweets download for {sample_date['month']}-{sample_date['year']}")
            queue.put(sample_date['link'])

        queue.join()
        tracker.join()


def main(command_line_arguments: Dict[str, Any]):  # skip_tests
    _start_time = time.time()
    verbose = not command_line_arguments['quiet']
    _dozent_object = Dozent()

    _dozent_object.download_timeframe(start_date=command_line_arguments['start_date'],
                                      end_date=command_line_arguments['end_date'],
                                      verbose=verbose)

    if command_line_arguments['timeit']:
        print(f"Download Time: {datetime.timedelta(seconds=(time.time() - _start_time))}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A powerful downloader to get tweets from twitter for our compute. '
                                                 'The first step of many')
    parser.add_argument('-s', '--start-date', help="The date from where we download. The format must be: YYYY-MM-DD",
                        required=True, type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d').date())
    parser.add_argument('-e', '--end-date', help="The last day that we download. The format must be: YYYY-MM-DD",
                        required=True, type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d').date())
    parser.add_argument('-t', '--timeit', help='Show total program runtime', default=True)
    parser.add_argument('-o', '--output-directory', help='Output Directory where the file will be stored. '
                                                         'Defaults to the data/ directory',
                        default=DEFAULT_DATA_DIRECTORY)
    parser.add_argument('-q', '--quiet', help='Turn off output (except for errors and warnings)', action='store_true')
    args = parser.parse_args()
    main(vars(args))
