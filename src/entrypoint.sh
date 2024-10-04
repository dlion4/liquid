#!/bin/bash
set -e

# Activate the virtual environment
source /app/.venv/bin/activate
# Collect static files

# Run the server
uvicorn src:app --reload --host 0.0.0.0 --port 8001

# Run the server
exec "$@"