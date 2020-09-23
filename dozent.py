import datetime
import json
import multiprocessing
import time
from queue import Queue
from threading import Thread

try:
    from downloader_tools import DownloaderTools
except ModuleNotFoundError:
    from .downloader_tools import DownloaderTools


class _DownloadWorker(Thread):

    def __init__(self, queue: Queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            link = self.queue.get()
            try:
                DownloaderTools.download_pysmartdl(link)
            finally:
                self.queue.task_done()


class Dozent:
    def __init__(self, start_date: datetime.datetime, end_date: datetime.datetime):
        self.start_date = start_date
        self.end_date = end_date

    def download_timeframe(self):
        '''
        Download all tweet archives from self.start_date to self.end_date
        :return: None
        '''

        with open('twitter-archivestream-links.json') as file:
            data = json.loads(file.read())

        # Create a queue to communicate with the worker threads
        queue = Queue()

        for x in range(multiprocessing.cpu_count()):
            worker = _DownloadWorker(queue)
            # Setting daemon to True will let the main thread exit even though the workers are blocking
            worker.daemon = True
            worker.start()

        start_index = data.index(
            next(filter(lambda link: (int(link['month']) == self.start_date.month) and
                                     (int(link['year']) == self.start_date.year), data)))
        end_index = data.index(
            next(filter(lambda link: (int(link['month']) == self.end_date.month) and
                                     (int(link['year']) == self.end_date.year), data)))

        # Put the tasks into the queue
        for sample_date in data[start_index:end_index]:
            print(f"Queueing tweet download for {sample_date['month']}-{sample_date['year']}")
            queue.put(sample_date['link'])

        queue.join()


if __name__ == "__main__":
    _start_time = time.time()
    _dozent_object = Dozent(datetime.datetime(2011, 9, 1), datetime.datetime(2016, 10, 1))
    if _dozent_object.end_date > datetime.datetime(2017, 6, 1):
        RuntimeError('Not implemented')
    _dozent_object.download_timeframe()
    print(f"Download Time: {datetime.timedelta(seconds=(time.time() - _start_time))}")
