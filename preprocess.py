import os
import tarfile
import time
import zipfile
from datetime import timedelta


class Preprocess:
    def __init__(self):
        os.chdir('..')
        if os.path.isdir("raw"):
            pass
        else:
            os.mkdir('raw')

    @staticmethod
    def _untar_file(file_path: str, dest: str):
        """
        Untars a single tar file into target directory
        :return: None
        """
        file_path = tarfile.open(file_path)
        file_path.extract(dest)

    @staticmethod
    def _unzip_file(file_path: str, dest: str):
        """
        Unzips a single zip file into target directory
        :return: None
        """
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(dest)

    @staticmethod
    def extract_directory(directory_path: str, destination: str, verbose: bool = True):
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
            print(f"\nSucessfully extracted all files in {directory_path} to {destination}")


if __name__ == "__main__":
    _start_time = time.time()
    Preprocess.extract_directory('dozent/data', 'preprocess/raw')
    print(f"\nElasped Time: {timedelta(seconds=(time.time() - _start_time))}")
