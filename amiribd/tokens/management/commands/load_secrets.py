import os

from django.core.management.base import BaseCommand

from amiribd.tokens.models import Secret


class Command(BaseCommand):
    help = "Load secret keys into environment variables"

    def handle(self, *args, **kwargs):
        secrets = Secret.objects.filter(is_active=True).prefetch_related("source")
        for secret in secrets:
            os.environ[secret.name] = secret.value
            self.stdout.write(
                self.style.SUCCESS(f"Successfully loaded secret: {secret.name}"))
