FROM python:3.11.4

# set work directory
WORKDIR trading_django

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install -y curl

# install dependencies
COPY Pipfile Pipfile.lock ./

# copy project & entrypointscript
COPY ./src ./src
# COPY entrypoint-django.sh ./
ADD entrypoint-django.sh ./

RUN python -m pip install --upgrade pip
RUN pip install pipenv
RUN pipenv sync

# Give execute permissions to the entrypoint script
RUN chmod 777 ./entrypoint-django.sh
