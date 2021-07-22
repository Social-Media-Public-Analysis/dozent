import os
from links_parser import get_links

LINKS_FILE_NAME = 'links.txt'


def _run_bash_command(command):
    os.system(command)


def remove_links_file():
    os.remove(LINKS_FILE_NAME)


def is_aria2c_installed():
    pass


def _make_links_file_for_aria2(start_date: str, end_date: str):
    links = get_links(start_date=start_date, end_date=end_date)

    with open(LINKS_FILE_NAME, 'w') as links_file_handle:
        links_file_handle.write('\n'.join(links))


def download_with_aria2c(
        start_date: str,
        end_date: str
):
    _make_links_file_for_aria2(start_date=start_date, end_date=end_date)

    command = f"aria2c -i {LINKS_FILE_NAME} -x 16 -j 16"

    _run_bash_command(command)
    remove_links_file()


if __name__ == "__main__":
    download_with_aria2c('2019-06-02', '2019-06-04')
