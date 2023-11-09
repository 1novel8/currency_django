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

# copy project & entrypointscripts
COPY ./src ./src

RUN python -m pip install --upgrade pip
RUN pip install pipenv
RUN pipenv sync

ADD entrypoint-django.sh ./
ADD entrypoint-celery-worker.sh ./
ADD entrypoint-celery-schedule.sh ./

# Give execute permissions to the entrypoint script
RUN chmod +x ./entrypoint-django.sh
# Give execute permissions to the entrypoint script
RUN chmod +x ./entrypoint-celery-worker.sh
# Give execute permissions to the entrypoint script
RUN chmod +x ./entrypoint-celery-schedule.sh
