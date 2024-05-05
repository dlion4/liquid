from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "amiribd.users"
    verbose_name = _("Users")

    def ready(self):
        import amiribd.users.signals  # noqa: F401
        return super().ready()
