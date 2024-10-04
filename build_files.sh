#!/bin/bash
set -e
# Activate the virtual environment
source /app/.venv/bin/activate

# makemigrations
python manage.py makemigrations
# migrate the migrations
python manage.py migrate



# Run the server
exec "$@"