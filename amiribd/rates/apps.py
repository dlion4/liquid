from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class RatesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "amiribd.rates"
    verbose_name = _("rates")
