# Dozent

Dozent is a powerful downloader that is used to collect large amounts of Twitter data from the internet archive.

It is built on top of [PySmartDL](https://pypi.org/project/pySmartDL/) and multithreading, similar to how traditional download accelerators like [axel](https://linux.die.net/man/1/axel), [aria2c](https://linux.die.net/man/1/aria2c) and [aws s3](https://docs.aws.amazon.com/cli/latest/userguide/cli-services-s3-commands.html) work, ensuring that the biggest bottlenecks are your network and your hardware.

The data that is downloaded is already heavily compressed to reduce download times and save local storage. When uncompressed, the data can easily add up to several terabytes depending on the timeframe of data being collected. Fortunately, you do not have to decompress the data to analyze it! We are working on a separate big data tool named [Murphy](https://github.com/Social-Media-Public-Analysis/murpheus) that uses Dask to analyze the data without needing to decompress it.

If you have any ideas on how to improve Dozent, please open an issue [here](https://github.com/Twitter-Public-Analysis/Twitter-Public-Analysis/issues) and tell us how!

## Installation

Before installing, ensure that the version of python that you're using is python>=3.6. We intend to support all of the latest releases of as they come out

### Installing with pip

Installing with pip is as easy as:

```bash
pip install dozent
```

### Installing with Docker

In keeping with our goal for keeping everything we distribute as lightweight as possible, we include a docker image that would ensure that this process is as painless as possible without having to worry about python versions and so on.

While "installing" isn't something that we can do with docker, we felt it best to include a some helpful links to help new comers install docker. 

You can find the link to the installation [here](https://docs.docker.com/get-docker/). If you chose to go this route, we suggest jumping down to the `Run Dozent as a Docker Container` section after installing docker. 

## Usage

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

### Downloading with Dozent after installing with pip

Downloading all tweets from 12th of May 2020 to 15th of May 2020

```bash
$ python -m dozent -s 2020-05-12 -e 2020-05-15

Queueing tweets download for 05-2020
Queueing tweets download for 05-2020
Queueing tweets download for 05-2020
Queueing tweets download for 05-2020
https://archive.org/download/archiveteam-twitter-stream-2020-05/twitter_stream_2020_05_13.tar [downloading] 16 Mb / 2498 Mb @ 1.6 MB/s [------------------] [0%, 32 minutes, 31 seconds left]
```

### Downloading with Dozent after installing Docker

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
$ docker run -it socialmediapublicanalysis/dozent:latest python -m dozent -s 2020-05-12 -e 2020-05-15
```

# About the Data

- Only collects Tweets in the English language
- Tweets are stored in JSON format
- Each day is a compressed file roughly 2.5 GB large or ~ 32 GB uncompressed
- Each tweet has accompanying metadata about the tweet and user

# Sample Data

Interested in seeing what the data that Dozent collects looks like?

Check it out!

https://dozent-tests.s3.amazonaws.com/sample_data.json
