# ruff: noqa
"""
WSGI config for amiribd project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""

import os
import sys
from pathlib import Path

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from starlette.requests import Request

from channels.security.websocket import AllowedHostsOriginValidator

# This allows easy placement of apps within the interior
# amiribd directory.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(BASE_DIR / "amiribd"))

# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
# os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.production"
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
from starlette.types import ASGIApp, Receive, Scope, Send

# This application object is used by any WSGI server configured to use this
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
django_asgi_application = get_asgi_application()

from amiribd.streams import routing




application = ProtocolTypeRouter(
    {
        "http": django_asgi_application,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns))
        ),
    }
)

