import os
from django.core.management.base import BaseCommand
from uvicorn import Config, Server

class Command(BaseCommand):
    help = 'Starts the ASGI server with Uvicorn'

    def handle(self, *args, **options):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
        config = Config(
            'config.asgi:application',
            host='127.0.0.1', 
            port=8000, 
            log_level='debug', 
            reload=True, 
            reload_dirs=['./services/apis/']
        )
        server = Server(config)
        server.run()
