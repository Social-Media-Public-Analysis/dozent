# Specify the base image
FROM python:3.9.2-slim-buster

# Make sure that the working directory is app
WORKDIR /usr/app

# Never prompts the user for choices on installation/configuration of scripts
ENV DEBIAN_FRONTEND noninteractive

# Install dependencies
COPY ./requirements.txt ./

# Run some commands
RUN set -ex \
    && apt-get update -yqq \
    && apt-get upgrade -yqq \
    && python -m venv dozent-env \
    && python -m pip install -r requirements.txt

# Copy the rest of the files
COPY ./ ./

# Default command
CMD python -m dozent --help
