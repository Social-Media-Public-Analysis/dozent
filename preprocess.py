import os
import shutil
import tarfile
import zipfile
import tqdm

from morpheus.data_loading import DataLoading


class Preprocess:
    __instance__ = None
    __output_formats = ['csv', 'json', 'parquet', 'sql']

    def __init__(self):
        if Preprocess.__instance__ is None:
            Preprocess.__instance__ = self
        else:
            raise RuntimeError(f"Singleton {self.__class__.__name__} class is created more than once!")

    @staticmethod
    def __untar_file(file_path: str, destination: str, verbose: bool):
        """
        Untars a single tar file into target directory
        :return: None
        """
        if verbose:
            print(f"Extracting {file_path}")
        tar_file = tarfile.open(file_path)
        try:
            tar_file.extractall(destination)
        except:
            tar_file.close()
        tar_file.close()

    @staticmethod
    def __unzip_file(file_path: str, destination: str, verbose: bool):
        """
        Unzips a single zip file into target directory
        :return: None
        """
        if verbose:
            print(f"Extracting {file_path}")
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            try:
                zip_ref.extractall(destination)
            except:
                zip_ref.close()
            zip_ref.close()

    @staticmethod
    def extract_directory(directory_path: str, destination: str, verbose: bool = True, delete_archive: bool = False):
        """
        Extracts all files in a directory into target directory
        :param directory_path: path of the directory
        :param destination: where the files will be stored
        :param verbose: show output?
        :return: None
        """

        if os.path.isdir(destination):
            pass
        else:
            os.mkdir(destination)

        files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
        for file in files:
            file_extension = file[-3:]
            if file_extension == 'tar':
                if verbose:
                    print(f"\nUntaring: {file}")
                Preprocess.__untar_file(f"{directory_path}{file}", destination, verbose)
            elif file_extension == 'zip':
                if verbose:
                    print(f"\nUnzipping: {file}")
                Preprocess.__unzip_file(f"{directory_path}{file}", destination, verbose)
            else:
                raise RuntimeError(f"File extension .{file_extension} not recognized.")
        if verbose:
            print(f"\nSuccessfully extracted all files in {directory_path} to {destination}")

        if delete_archive:
            shutil.rmtree(directory_path)

    @staticmethod
    def store_tweets_to_file_format(directory_path: str, destination: str, suffix: str = '*.json*',
                                    recursive: bool = True,
                                    output_format='csv'):
        """
        Extracting all tweets and storing them as csv.
        This function recursively searches the `directory_path` for files that match the given `suffix`

        :param directory_path: path of the directory where the data is stored.
        :param suffix: suffix: suffix to search for files with
        :param destination: where the output needs to be stored
        :param recursive: recursively search for files?
        :param output_format: the format that the data should be stored in.
                              Possible values are:  ['csv', 'json', 'parquet', 'sql']
        :return:
        """

        if output_format not in Preprocess.__output_formats:
            raise ValueError(f'The given format: {output_format} is not in {Preprocess.__output_formats}')

        files_list = DataLoading.get_files_list(pathname=directory_path, suffix=suffix, recursive=recursive)
        data = DataLoading.get_twitter_data_from_file_list(file_lst=files_list)
        data = data.to_dataframe()

        if output_format == 'csv':
            data.to_csv(destination)

        elif output_format == 'json':
            data.to_json(destination)

        elif output_format == 'parquet':
            data.to_parquet(destination)

        elif output_format == 'sql':
            raise NotImplementedError('SQL has not been yet implemented. '
                                      'If you would like this feature, please make an issue here: '
                                      'https://github.com/Twitter-Public-Analysis/Twitter-Public-Analysis/issues')

        else:
            raise ValueError(f'The given format: {output_format} is not recognized')
