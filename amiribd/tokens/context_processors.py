from amiribd.tokens.models import Secret
import os

def load_secrets(request):
    secrets = Secret.objects.prefetch_related("source").filter(is_active=True)
    for secret in secrets:
        os.environ[secret.name] = secret.value
    return {}
