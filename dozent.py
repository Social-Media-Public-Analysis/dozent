import datetime
import json

from pySmartDL import SmartDL


class Dozent:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def download_timeframe(self):
        '''
        Download all tweet archives from self.start_date to self.end_date
        :return: None
        '''

        def download(link):
            '''
            Downloads file from link
            :param link:
            :return: None
            '''
            obj = SmartDL(link, '~/Downloads/')
            obj.start()

        with open('links.json') as file:
            data = json.loads(file.read())
            start_index = next((i for i, item in enumerate(data) if (
                        int(item['month']) == self.start_date.month and int(item['year']) == self.start_date.year)),
                               None)
            end_index = next((i for i, item in enumerate(data) if
                              (int(item['month']) == self.end_date.month and int(item['year']) == self.end_date.year)),
                             None)
            for dict in data[start_index:end_index]:
                link = dict.get('link')
                print(f"Downloading all tweets from {dict.get('month')}-{dict.get('year')}")
                download(link)


d = Dozent(datetime.datetime(2011, 9, 1), datetime.datetime(2017, 6, 1))
d.download_timeframe()