from django.apps import AppConfig

from utils.tracing_setup import setup_tracing
from opentelemetry.instrumentation.django import DjangoInstrumentor


class UnivestConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "univest"

    def ready(self):
        setup_tracing("univest")
        DjangoInstrumentor().instrument()
