import unittest
from dozent.preprocess import Preprocess
from os import mkdir
from shutil import rmtree
from pathlib import Path
from tests import CommonTestSetup
import os

CURRENT_FILE_PATH = Path(__file__)
TEST_EXTRACTOR_FILE_PATH = CURRENT_FILE_PATH.parent / 'test_extract_file_path'


class PreprocessTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.data_path, self.path_prefix = CommonTestSetup.set_data_dir_path()
        self.raw_file_path = Path(__file__).parent / 'compressed_test_files/raw'
        self.compressed_files_directory = Path(__file__).parent / 'compressed_test_files/'
        try:
            mkdir(TEST_EXTRACTOR_FILE_PATH)
        except FileExistsError:
            rmtree(TEST_EXTRACTOR_FILE_PATH)
            mkdir(TEST_EXTRACTOR_FILE_PATH)

        try:
            mkdir(self.raw_file_path)
        except FileExistsError:
            rmtree(self.raw_file_path)
            mkdir(self.raw_file_path)

    def tearDown(self) -> None:
        rmtree(TEST_EXTRACTOR_FILE_PATH)
        rmtree(self.raw_file_path)

    def test_extract_directory(self):
        Preprocess.extract_directory(self.compressed_files_directory, self.raw_file_path,
                                     verbose=False)

        self.assertTrue(os.path.isfile(os.path.join(self.raw_file_path, 'test_preprocess_file_1.txt')))
        self.assertTrue(os.path.isfile(os.path.join(self.raw_file_path, 'test_preprocess_file_2.txt')))
        self.assertTrue(os.path.isfile(os.path.join(self.raw_file_path, 'test_preprocess_file_3.txt')))
        self.assertTrue(os.path.isfile(os.path.join(self.raw_file_path, 'test_preprocess_file_4.txt')))
        self.assertTrue(os.path.isfile(os.path.join(self.raw_file_path, 'test_preprocess_file_5.txt')))
        self.assertTrue(os.path.isfile(os.path.join(self.raw_file_path, 'test_preprocess_file_6.txt')))

    def test_store_tweets_to_supported_file_formats(self):
        for output_format in Preprocess._output_formats:
            output_file_format = f'*.{output_format}'
            if output_format in Preprocess._unsupported_formats:
                try:
                    Preprocess.store_tweets_to_file_format(
                        directory_path=self.data_path,
                        destination=TEST_EXTRACTOR_FILE_PATH / output_file_format,
                        suffix='*.json.bz2',
                        recursive=True,
                        output_format=output_format
                    )
                    self.assertFalse(False)
                except (NotImplementedError, ValueError):
                    self.assertTrue(True)
            else:
                file_list = Preprocess.store_tweets_to_file_format(
                    directory_path=self.data_path,
                    destination=TEST_EXTRACTOR_FILE_PATH / output_file_format,
                    suffix='*.json.bz2',
                    recursive=True,
                    output_format=output_format
                )

                file_list = [Path(x) for x in file_list]
                test_file_list = [x for x in TEST_EXTRACTOR_FILE_PATH.glob(f'*.{output_format}')]

                file_list.sort()
                test_file_list.sort()

                self.assertListEqual(file_list, test_file_list)
