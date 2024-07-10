from django.apps import AppConfig
from django.core.management import call_command
import os
class TokensConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "amiribd.tokens"

    def ready(self) -> None:
        super().ready()
        # call_command("load_secrets")
