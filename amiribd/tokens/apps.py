
from django.apps import AppConfig


class TokensConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "amiribd.tokens"

    def ready(self) -> None:
        super().ready()
