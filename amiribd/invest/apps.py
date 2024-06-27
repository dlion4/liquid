from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class InvestConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "amiribd.invest"
    verbose_name = _("invests")
