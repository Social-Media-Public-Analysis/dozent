import datetime
import json
import multiprocessing
from pySmartDL import SmartDL
import os
import aria2p

class Dozent:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def download_timeframe(self):
        '''
        Download all tweet archives from self.start_date to self.end_date
        :return: None
        '''

        def download_pysmart(link):
            '''
            Downloads file from link using PySmartDL
            :param link:
            :return: None
            '''
            obj = SmartDL(link, '~/Downloads/')
            obj.start()

        def download_axel(link):
            connections = 2 * multiprocessing.cpu_count()
            os.system(f"axel --verbose --alternate --num-connections={connections} {link}")

        def download_aria2(link):
            connections = 2 * multiprocessing.cpu_count()
            os.system(f"aria2c -x {connections} {link}")

        with open('twitter-archivestream-links.json') as file:
            data = json.loads(file.read())

            start_index = data.index(next(filter(lambda link: (int(link['month']) == self.start_date.month) and (int(link['year']) == self.start_date.year), data)))
            end_index = data.index(next(filter(lambda link: (int(link['month']) == self.end_date.month) and (int(link['year']) == self.end_date.year), data)))

            for dict in data[start_index:end_index]:
                link = dict['link']
                print(f"Downloading all tweets from {dict['month']}-{dict['year']}")
                download_pysmart(link)


d = Dozent(datetime.datetime(2011, 9, 1), datetime.datetime(2017, 7, 1))
d.download_timeframe()