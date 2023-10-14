#!/bin/bash

# exit if error
set -e

# Run migrations
echo "Running migrations..."

cd src

pipenv run python manage.py makemigrations
pipenv run python manage.py migrate

# Run Django app
echo "Starting Django app..."
pipenv run python manage.py runserver "$DJANGO_HOST":"$DJANGO_PORT"
