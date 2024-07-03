from django.utils.deprecation import MiddlewareMixin
from amiribd.tokens.models import Secret

import os

class LoadSecretsMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        secrets = Secret.objects.prefetch_related("source").filter(is_active=True)
        for secret in secrets:
            os.environ[secret.name] = secret.value
        
    def __call__(self, request):
        response = self.get_response(request)
        return response
    
