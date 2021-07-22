import click

from aria2c_downloader import download_with_aria2c


@click.command()
@click.option('--start-date',
              help='What is the start date? (YYYY-MM-DD)',
              prompt='What is the start date? (YYYY-MM-DD)')
@click.option('--end-date',
              help='What is the end date? (YYYY-MM-DD)',
              prompt='What is the end date? (YYYY-MM-DD)')
def download_all_days_between(start_date: str, end_date: str):
    download_with_aria2c(start_date=start_date, end_date=end_date)


if __name__ == '__main__':
    download_all_days_between()
