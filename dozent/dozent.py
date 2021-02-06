import datetime
import json
import os
from pathlib import Path
from queue import Queue
from threading import Thread
from typing import List, Dict

try:
    from dozent.downloader_tools import DownloaderTools
except ModuleNotFoundError:
    from downloader_tools import DownloaderTools

CURRENT_FILE_PATH = Path(__file__)
DEFAULT_DATA_DIRECTORY = CURRENT_FILE_PATH.parent.parent / "data"
TWITTER_ARCHIVE_STREAM_LINKS_PATH = (
    CURRENT_FILE_PATH.parent / "twitter-archive-stream-links.json"
)

FIRST_DAY_OF_SUPPORT = datetime.date(2017, 6, 1)
LAST_DAY_OF_SUPPORT = datetime.date(2020, 6, 30)


class _DownloadWorker(Thread):  # skip_tests
    def __init__(
        self,
        queue: Queue,
        download_dir: Path,
        task_id: int,
        number_of_dates: int,
        verbose: bool,
    ):
        Thread.__init__(self)
        self.queue = queue
        self.download_dir = download_dir
        self.task_id = task_id
        self.number_of_dates = number_of_dates
        self.verbose = verbose

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            link = self.queue.get()
            try:
                DownloaderTools.download_with_pysmartdl(
                    link=link,
                    download_dir=str(self.download_dir),
                    task_id=self.task_id,
                    number_of_dates=self.number_of_dates,
                    verbose=self.verbose,
                )
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
            raise RuntimeError('Multiple classes detected, this class might not be thread safe')

    @staticmethod
    def _make_date_from_date_link(date_link: Dict[str, str]) -> datetime.date:
        """
        Function to make a date given the date link. For months that don't have individual dates (date = 'NaN'), we
        assume that it's the first.
        :param date_link: date dictionary from `data/test_sample_files.json`. This is used to convert to the date
        :return: date object for the associated month
        """
        day = int(date_link["day"]) if date_link["day"] != "NaN" else 1
        month = int(date_link["month"])
        year = int(date_link["year"])

        return datetime.date(year=year, month=month, day=day)

    def get_links_for_days(
        self, start_date: datetime.date, end_date: datetime.date
    ) -> List:
        """
        Function to get the links for the given start and end days
        :return: date dictionaries that are within self.start_date and self.end_dates
        """
        links = []

        if not FIRST_DAY_OF_SUPPORT >= start_date:
            RuntimeError(
                f'We currently only support the range {FIRST_DAY_OF_SUPPORT.strftime("%d, %b %Y")}, '
                f'{LAST_DAY_OF_SUPPORT.strftime("%d, %b %Y")}'
                f"\nWe're planning on adding support for it soon."
                f"Need that data sooner? Add an issue to out GitHub repo and we'll "
                f"walk you through the process"
                f"Link to our GitHub "
                f"Issues: https://github.com/Twitter-Public-Analysis/Twitter-Public-Analysis/issues"
            )

        elif not end_date <= end_date:
            RuntimeError(
                f'We currently only support the range {FIRST_DAY_OF_SUPPORT.strftime("%d, %b %Y")}, '
                f'{LAST_DAY_OF_SUPPORT.strftime("%d, %b %Y")}'
                f"\nWe're planning on adding support for it soon."
                f"Need that data sooner? Add an issue to out GitHub repo and we'll "
                f"walk you through the process"
                f"Link to our GitHub "
                f"Issues: https://github.com/Twitter-Public-Analysis/Twitter-Public-Analysis/issues"
            )

        for date_link in self.date_links:
            date = Dozent._make_date_from_date_link(date_link)
            if start_date <= date <= end_date:
                links.append(date_link)

        return links

    def download_timeframe(
        self,
        start_date: datetime.date,
        end_date: datetime.date,
        verbose: bool = True,
        download_dir: Path = DEFAULT_DATA_DIRECTORY,
    ):  # skip_tests
        """
        Download all tweet archives from self.start_date to self.end_date
        :return: None
        """

        # Create a queue to communicate with the worker threads
        queue = Queue()

        os.makedirs(download_dir, exist_ok=True)

        number_of_dates = (end_date - start_date).days + 1

        task_id = 0

        for x in range(number_of_dates):
            worker = _DownloadWorker(
                queue=queue,
                download_dir=download_dir,
                task_id=task_id,
                number_of_dates=number_of_dates,
                verbose=verbose,
            )
            task_id += 1
            # Setting daemon to True will let the main thread exit even though the workers are blocking
            worker.daemon = True
            worker.start()

        for sample_date in self.get_links_for_days(
            start_date=start_date, end_date=end_date
        ):
            print(
                f"Queueing tweets download for {sample_date['day']}-{sample_date['month']}-{sample_date['year']}"
            )
            queue.put(sample_date["link"])

        print("")
        queue.join()

    def download_test(
        self, verbose: bool = True, download_dir: Path = DEFAULT_DATA_DIRECTORY
    ):  # skip_tests
        """
        Downloads four small test files from S3 for testing purposes
        """

        # Stores download links for sample data
        test_download_links = [
            "https://dozent-tests.s3.amazonaws.com/test_500K.txt",
            "https://dozent-tests.s3.amazonaws.com/test_550K.txt",
            "https://dozent-tests.s3.amazonaws.com/test_600K.txt",
            "https://dozent-tests.s3.amazonaws.com/test_650K.txt",
        ]

        # Create a queue to communicate with the worker threads
        queue = Queue()

        os.makedirs(download_dir, exist_ok=True)

        task_id = 0

        number_of_links = len(test_download_links)

        for x in range(number_of_links):
            worker = _DownloadWorker(
                queue=queue,
                download_dir=download_dir,
                task_id=task_id,
                number_of_dates=number_of_links,
                verbose=verbose,
            )

            task_id += 1
            # Setting daemon to True will let the main thread exit even though the workers are blocking
            worker.daemon = True
            worker.start()

        for link in test_download_links:
            print(f"Queueing Link {link}")
            queue.put(link)

        print("")
        queue.join()
