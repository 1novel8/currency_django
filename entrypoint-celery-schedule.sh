#!/bin/sh

# exit if error
set -e

# Run celery schedule
echo "Running celery schedule..."

cd src

pipenv run python -m celery -A config beat --loglevel=info
