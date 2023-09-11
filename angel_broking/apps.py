from django.apps import AppConfig

from utils.tracing_setup import setup_tracing


class AngelBrokingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "angel_broking"

    def ready(self):
        setup_tracing("angel_broking")
