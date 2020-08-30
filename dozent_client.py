import datetime
import json
import multiprocessing
from queue import Queue
from threading import Thread
import time

from dozent.download import download_axel


class DownloadWorker(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            link = self.queue.get()
            try:
                download_axel(link)
            finally:
                self.queue.task_done()


class Dozent:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def download_timeframe(self):
        '''
        Download all tweet archives from self.start_date to self.end_date
        :return: None
        '''

        with open('twitter-archivestream-links.json') as file:

            # Create a queue to communicate with the worker threads
            queue = Queue()

            for x in range(multiprocessing.cpu_count()):
                worker = DownloadWorker(queue)
                # Setting daemon to True will let the main thread exit even though the workers are blocking
                worker.daemon = True
                worker.start()

            data = json.loads(file.read())

            start_index = data.index(next(filter(lambda link: (int(link['month']) == self.start_date.month) and (
                        int(link['year']) == self.start_date.year), data)))
            end_index = data.index(next(filter(
                lambda link: (int(link['month']) == self.end_date.month) and (int(link['year']) == self.end_date.year),
                data)))

            # Put the tasks into the queue
            for dict in data[start_index:end_index]:
                print(f"Queueing tweet download for {dict['month']}-{dict['year']}")
                queue.put(dict['link'])
            queue.join()


current_time = time.time()
d = Dozent(datetime.datetime(2012, 1, 1), datetime.datetime(2012, 5, 1))
d.download_timeframe()
print(f"Download Time: {time.time() - current_time} seconds.")