"""
WSGI config for nirania_trading project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from utils.tracing_setup import setup_tracing
from opentelemetry.instrumentation.django import DjangoInstrumentor

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nirania_trading.settings")

application = get_wsgi_application()


setup_tracing("nirania_trading")
DjangoInstrumentor().instrument()
