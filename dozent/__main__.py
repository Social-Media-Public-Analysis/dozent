import argparse
import datetime
import time
from pathlib import Path

try:
    from dozent.dozent import Dozent
except ModuleNotFoundError:
    from dozent import Dozent

CURRENT_FILE_PATH = Path(__file__)
DEFAULT_DATA_DIRECTORY = CURRENT_FILE_PATH.parent.parent / "data"

parser = argparse.ArgumentParser(
    description="A powerful downloader to get tweets from twitter for our compute. " "The first step of many"
)
parser.add_argument(
    "-s",
    "--start-date",
    help="The date from where we download. The format must be: YYYY-MM-DD",
    type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d").date(),
)
parser.add_argument(
    "-e",
    "--end-date",
    help="The last day that we download. The format must be: YYYY-MM-DD",
    type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d").date(),
)
parser.add_argument("-t", "--timeit", help="Show total program runtime", default=True)
parser.add_argument(
    "-o",
    "--output-directory",
    help="Output Directory where the file will be stored. " "Defaults to the data/ directory",
    default=DEFAULT_DATA_DIRECTORY,
)
parser.add_argument(
    "-q",
    "--quiet",
    help="Turn off output (except for errors and warnings)",
    action="store_true",
)
parser.add_argument(
    "--dry-run",
    help="Downloads 4 small files for testing purposes (<3 MB total)",
    action="store_true",
)
args = parser.parse_args()
command_line_arguments = vars(args)

if __name__ == "__main__":

    _start_time = time.time()
    verbose = not command_line_arguments["quiet"]
    _dozent_object = Dozent()

    if command_line_arguments["start_date"] and command_line_arguments["end_date"]:
        _dozent_object.download_timeframe(
            start_date=command_line_arguments["start_date"],
            end_date=command_line_arguments["end_date"],
            verbose=verbose,
        )

        if command_line_arguments["timeit"]:
            print(f"Download Time: {datetime.timedelta(seconds=(time.time() - _start_time))}")

    elif command_line_arguments["dry_run"]:
        _dozent_object.download_test(verbose=verbose)

        if command_line_arguments["timeit"]:
            print(f"\nDownload Time: {datetime.timedelta(seconds=(time.time() - _start_time))}")

    else:
        parser.print_help()
