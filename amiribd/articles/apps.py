from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ArticlesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "amiribd.articles"
    verbose_name = _("Articles")

    def ready(self) -> None:
        import amiribd.articles.signals  # noqa: F401
        return super().ready()


