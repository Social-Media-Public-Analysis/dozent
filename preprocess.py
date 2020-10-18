import os
import tarfile
import time
import zipfile
from datetime import timedelta
from morpheus.data_loading import DataLoading
from pathlib import Path
from typing import Union, List


class Preprocess:
    _output_formats = ['csv', 'json', 'parquet', 'sql']
    _supported_formats = ['csv', 'json']
    _unsupported_formats = ['parquet', 'sql']

    def __init__(self):
        os.chdir('..')
        if os.path.isdir("raw"):
            pass
        else:
            os.mkdir('raw')

    @staticmethod
    def _untar_file(file_path: Union[str, Path], destination: Union[str, Path]):
        """
        Untars a single tar file into target directory
        :return: None
        """
        file_path = tarfile.open(file_path)
        file_path.extract(destination)

    @staticmethod
    def _unzip_file(file_path: Union[str, Path], destination: Union[str, Path]):
        """
        Unzips a single zip file into target directory
        :return: None
        """
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(destination)

    @staticmethod
    def extract_directory(directory_path: Union[str, Path], destination: Union[str, Path], verbose: bool = True):
        """
        Extracts all files in a directory into target directory
        :param directory_path: path of the directory
        :param destination: where the files will be stored
        :param verbose: show output?
        :return: None
        """

        files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
        for file in files:
            file_extension = file.split('.')[:-1]

            if file_extension == 'tar':
                if verbose:
                    print(f"\nUntaring: {file}")
                Preprocess._untar_file(f"{directory_path}/{file}", destination)
            elif file_extension == 'zip':
                if verbose:
                    print(f"\nUnzipping: {file}")
                Preprocess._unzip_file(f"{directory_path}/{file}", destination)
            else:
                RuntimeError(f"File extension {file_extension} not recognized.")
        if verbose:
            print(f"\nSuccessfully extracted all files in {directory_path} to {destination}")

    @staticmethod
    def store_tweets_to_file_format(directory_path: Union[str, Path], destination: Union[str, Path],
                                    suffix: str = '*.json*',
                                    recursive: bool = True,
                                    output_format='csv') -> List[str]:
        """
        Extracting all tweets and storing them as csv.
        This function recursively searches the `directory_path` for files that match the given `suffix`

        :param directory_path: path of the directory where the data is stored.
        :param suffix: suffix: suffix to search for files with
        :param destination: where the output needs to be stored
        :param recursive: recursively search for files?
        :param output_format: the format that the data should be stored in.
                              While the possible values are:  ['csv', 'json', 'parquet', 'sql'], we currently test for
                              only ['csv', 'json']
        :return: returns the list of all of the output files
        """
        if output_format not in Preprocess._supported_formats:
            raise ValueError(f'The given format: {output_format} is not in {Preprocess._supported_formats}')

        files_list = DataLoading.get_files_list(pathname=directory_path, suffix=suffix, recursive=recursive)
        data = DataLoading.get_twitter_data_from_file_list(file_lst=files_list, remove_deleted_tweets=True)
        data = data.to_dataframe()

        if output_format == 'csv':
            return data.to_csv(destination)

        elif output_format == 'json':
            return data.to_json(destination)

        elif output_format == 'parquet':  # skip_tests
            raise NotImplementedError('Parquet has not been yet supported because of the added dependency of '
                                      'fastparque/pyarrow, which we might look into later'
                                      'If you would like this feature, please make an issue here: '
                                      'https://github.com/Twitter-Public-Analysis/Twitter-Public-Analysis/issues')

        elif output_format == 'sql':  # skip_tests
            raise NotImplementedError('SQL has not been yet implemented. '
                                      'If you would like this feature, please make an issue here: '
                                      'https://github.com/Twitter-Public-Analysis/Twitter-Public-Analysis/issues')

        else:
            raise ValueError(f'The given format: {output_format} is not recognized')


if __name__ == "__main__":
    pass
