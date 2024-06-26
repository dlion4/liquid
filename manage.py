#!/usr/bin/env python
# ruff: noqa
import os
import sys
from pathlib import Path
import subprocess
import threading
import asyncio
import uvicorn

def run_django():
    subprocess.call(['python', 'manage.py', 'runserver', '127.0.0.1:8000'])

def run_uvicorn():
    subprocess.call(['uvicorn', 'services.apis.views:app', '--reload', '--host', '127.0.0.1', '--port', '8001'])

async def main():
    config = uvicorn.Config("main:app", port=5000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

    try:
        from django.core.management import execute_from_command_line

    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )

        raise

    # This allows easy placement of apps within the interior
    # amiribd directory.
    current_path = Path(__file__).parent.resolve()
    sys.path.append(str(current_path / "amiribd"))
    # sys.path.append(str(current_path / "services"))
    
    execute_from_command_line(sys.argv)
