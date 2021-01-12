# Dozent

Dozent is a powerful downloader that is used to collect large amounts of Twitter data from the internet archive.

It is built on top of [PySmartDL](https://pypi.org/project/pySmartDL/) and multithreading, similar to how traditional download accelerators like [axel](https://linux.die.net/man/1/axel), [aria2c](https://linux.die.net/man/1/aria2c) and [aws s3](https://docs.aws.amazon.com/cli/latest/userguide/cli-services-s3-commands.html) work, ensuring that the biggest bottlenecks are your network and your hardware.

The data that is downloaded is already heavily compresseed to reduce download times and save local storage. When uncompressed, the data can easily add up to several petabytes depending on the timeframe of data being collected. Fortunetly, you do not have to decompress the data to analyze it! We are working on a seperate big data tool named [Murpheus](https://github.com/Social-Media-Public-Analysis/murpheus) that uses [Dask](https://dask.org/) to analyze the data without needing to decompress it.

If you have any ideas on how to improve Dozent, please open an issue [here](https://github.com/Twitter-Public-Analysis/Twitter-Public-Analysis/issues) and tell us how!

## Getting Started

To get started, just follow the `Getting Started` part of our main ReadMe (Linked [here](https://github.com/Twitter-Public-Analysis/Twitter-Public-Analysis/blob/master/README.md#getting-started)) 

## Usage

Please ensure that Dozent is ran with a Python version greater or equal to 3.6 as any versions lower than 3.6 are incompatible.

Here's the `help` command:

```bash
$ python -m dozent --help

usage: __main__.py [-h] -s START_DATE -e END_DATE [-t TIMEIT]
                 [-o OUTPUT_DIRECTORY] [-q]

A powerful downloader to get tweets from twitter for our compute. The first
step of many

optional arguments:
  -h, --help            show this help message and exit
  -s START_DATE, --start-date START_DATE
                        The date from where we download. The format must be:
                        YYYY-MM-DD
  -e END_DATE, --end-date END_DATE
                        The last day that we download. The format must be:
                        YYYY-MM-DD
  -t TIMEIT, --timeit TIMEIT
                        Show total program runtime
  -o OUTPUT_DIRECTORY, --output-directory OUTPUT_DIRECTORY
                        Output Directory where the file will be stored.
                        Defaults to the data/ directory
  -q, --quiet           Turn off output (except for errors and warnings)

```

## Example

Here's an example of how the project works:

The general workflow that we envision is that the user downloads the files for the days that they're interested in, preprocessing for the specifics that you'll looking for, and running more complex algorithms on top of that. 

Here is the command for downloading all tweets from March 12th, 2020 to March 15th, 2020. Please be sure to use a Python version greater or equal to 3.6

```bash
$ python -m dozent -s 2020-05-12 -e 2020-05-15

Queueing tweets download for 05-2020
Queueing tweets download for 05-2020
Queueing tweets download for 05-2020
Queueing tweets download for 05-2020
https://archive.org/download/archiveteam-twitter-stream-2020-05/twitter_stream_2020_05_13.tar [downloading] 16 Mb / 2498 Mb @ 1.6 MB/s [------------------] [0%, 32 minutes, 31 seconds left]
```
## Run Dozent as a Docker Container

Pull the latest Dozent image from Docker Hub
```bash
$ docker pull socialmediapublicanalysis/dozent:latest
```

Get help
```bash
$ docker run -it socialmediapublicanalysis/dozent:latest
```
or
```bash
$ docker run -it socialmediapublicanalysis/dozent:latest -h
```

Download all tweets from March 12th, 2020 to March 15th, 2020
```bash
$ docker run -it socialmediapublicanalysis/dozent:latest python3.6 -m dozent -s 2020-05-12 -e 2020-05-15
```
