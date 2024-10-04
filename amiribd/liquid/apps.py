from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class LiquidConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "amiribd.liquid"

    verbose_name = _("Liquid")

    def ready(self) -> None:

        from .schedular import schedular

        schedular.main()
