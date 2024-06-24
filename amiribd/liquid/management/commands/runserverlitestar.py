import os
from django.core.management.base import BaseCommand
from uvicorn import Config, Server

class Command(BaseCommand):
    help = 'Starts the ASGI server with Uvicorn'

    def handle(self, *args, **options):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
        config = Config('config.asgi:application', host='localhost', port=8000, log_level='info', reload=True)
        server = Server(config)
        server.run()
