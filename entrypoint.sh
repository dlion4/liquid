#!/bin/bash
set -e

# Activate the virtual environment
source /app/.venv/bin/activate

# Collect static files
python manage.py collectstatic --noinput

# Run the server
python manage.py runserver 0.0.0.0:8000
python manage.py runserver 0.0.0.0:8090
python manage.py runserver 0.0.0.0:8091

# Run the server
exec "$@"