#!/bin/bash
set -e

# Activate the virtual environment
source /app/.venv/bin/activate

# Collect static files
python manage.py collectstatic --noinput

# Run the server
exec "$@"