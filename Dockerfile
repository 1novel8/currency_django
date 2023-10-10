FROM python:3.11.4

# set work directory
WORKDIR trading_django

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY Pipfile Pipfile.lock ./

# copy project & entrypointscript
COPY ./src ./src
COPY entrypoint-django.sh /entrypoint-django.sh

# Give execute permissions to the entrypoint script
RUN chmod +x /entrypoint-django.sh
