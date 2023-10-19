#!/bin/sh

# exit if error
set -e

# Run celery worker
echo "Running migrations..."

cd src

pipenv run python -m celery -A config worker --loglevel=info