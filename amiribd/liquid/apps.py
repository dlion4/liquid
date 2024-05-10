from django.apps import AppConfig


class LiquidConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "amiribd.liquid"

    def ready(self) -> None:

        from .schedular import schedular

        schedular.main()
