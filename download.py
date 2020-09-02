import multiprocessing
import os

from pySmartDL import SmartDL


def download_pysmartdl(link):
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
