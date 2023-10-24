#!/bin/sh

# exit if error
set -e

# Run celery worker
echo "Running celery worker..."
cd src

pipenv run python -m celery -A config worker --loglevel=info