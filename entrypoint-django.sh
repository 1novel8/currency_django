#!/bin/bash

# exit if error
set -e

# Run migrations
echo "Running migrations..."

cd src
python manage.py makemigrations
python manage.py migrate

# Run Django app
echo "Starting Django app..."
python manage.py runserver "$DJANGO_HOST":"$DJANGO_PORT"
