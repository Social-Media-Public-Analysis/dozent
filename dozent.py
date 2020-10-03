import datetime
import json
import multiprocessing
import time
from queue import Queue
from threading import Thread
import argparse
from typing import List, Dict, Any

DEFAULT_DIRECTORY = '../data/'
LAST_DAY_OF_SUPPORT = datetime.date(2017, 6, 1)

try:
    from downloader_tools import DownloaderTools
except ModuleNotFoundError:
    from .downloader_tools import DownloaderTools

try:
    from command_line_utils import text_renderer
except ModuleNotFoundError:
    from .command_line_utils import text_renderer


class _DownloadWorker(Thread):

    def __init__(self, queue: Queue):
        Thread.__init__(self)
        self.verbosity = True
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            link = self.queue.get()
            try:
                DownloaderTools.download_pysmartdl(link, verbose=self.verbosity)
            finally:
                self.queue.task_done()

    def set_verbosity(self, verbose: bool = True):
        self.verbosity = verbose


class Dozent:
    def __init__(self, start_date: datetime.date, end_date: datetime.date):
        self.start_date: datetime.date = start_date
        self.end_date: datetime.date = end_date

        with open('twitter-archive-stream-links.json') as file:
            self.date_links: List[Dict[str, str]] = json.loads(file.read())

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

    def get_links_for_days(self) -> List:
        """
        Function to get the links for the given start and end days
        :return: date dictionaries that are within self.start_date and self.end_dates
        """
        links = []

        for date_link in self.date_links:
            date = Dozent._make_date_from_date_link(date_link)
            if self.start_date <= date <= self.end_date:
                links.append(date_link)

        return links

    def download_timeframe(self, verbosity: bool = True):
        """
        Download all tweet archives from self.start_date to self.end_date
        :return: None
        """

        # Create a queue to communicate with the worker threads
        queue = Queue()

        for x in range(multiprocessing.cpu_count()):
            worker = _DownloadWorker(queue)
            worker.set_verbosity(verbose=verbosity)
            # Setting daemon to True will let the main thread exit even though the workers are blocking
            worker.daemon = True
            worker.start()

        for sample_date in self.get_links_for_days():
            print(f"Queueing tweets download for {sample_date['month']}-{sample_date['year']}")
            queue.put(sample_date['link'])

        queue.join()


def main(command_line_arguments: Dict[str, Any]):
    _start_time = time.time()
    verbose = not command_line_arguments['quiet']
    _dozent_object = Dozent(command_line_arguments['start_date'], command_line_arguments['end_date'])

    if _dozent_object.end_date > LAST_DAY_OF_SUPPORT:
        RuntimeError(f'We currently only support until {LAST_DAY_OF_SUPPORT.strftime("%d, %b %Y")}'
                     f'\nWe\'re planning on adding support for it soon.'
                     f'Need that data sooner? Add an issue to out GitHub repo and we\'ll walk you through the process'
                     f'Link to our GitHub '
                     f'Issues: https://github.com/Twitter-Public-Analysis/Twitter-Public-Analysis/issues')

    _dozent_object.download_timeframe(verbosity=verbose)

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
                                                         'Defaults to the data/ directory', default=DEFAULT_DIRECTORY)
    parser.add_argument('-q', '--quiet', help='Turn off output (except for errors and warnings)', action='store_true')
    args = parser.parse_args()
    main(vars(args))
