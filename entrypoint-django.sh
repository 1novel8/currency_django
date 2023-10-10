#!/bin/bash

# exit if error
set -e

# Install curl for healthcheck
echo "Installing curl..."
apt-get update
apt-get install -y curl

# Install dependencies
echo "Installing dependencies..."
python -m pip install --upgrade pip
pip install pipenv
pipenv lock
pipenv install --dev --system --deploy

# Run migrations
echo "Running migrations..."

cd src
python manage.py makemigrations
python manage.py migrate

# Run Django app
echo "Starting Django app..."
python manage.py runserver "$DJANGO_HOST":"$DJANGO_PORT"
