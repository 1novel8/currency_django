FROM python:3.11.4-slim

# set work directory
WORKDIR trading_django/src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install -y curl

# install dependencies
RUN python -m pip install --upgrade pip
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv lock
RUN pipenv install --dev --system --deploy

# copy project
COPY ./src .