from django.apps import AppConfig


class StreamsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "amiribd.streams"

    def ready(self) -> None:
        import amiribd.streams.signals

