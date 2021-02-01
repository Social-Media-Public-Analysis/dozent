import io
import sys
from typing import Tuple
from pathlib import Path

CURRENT_FILE_PATH = Path(__file__)


class CommonTestSetup:
    @staticmethod
    def set_data_dir_path() -> Tuple[Path, Path]:
        data_path = CURRENT_FILE_PATH.parent.parent / f"tests/test_data"
        path_prefix = CURRENT_FILE_PATH.parent.parent
        return data_path, path_prefix

    @staticmethod
    def get_sample_files_list():
        data_path, _ = CommonTestSetup.set_data_dir_path()
        return data_path.glob("*.json.bz2")


# Suppress printing to console while running tests
sys.stdout = io.StringIO()

if __name__ == "__main__":
    pass
