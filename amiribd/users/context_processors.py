from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings

def get_site_protocol(request):
    return "https" if request.is_secure() else "http"



def allauth_settings(request):
    """Expose some settings from django-allauth in templates."""
    return {
        "ACCOUNT_ALLOW_REGISTRATION": settings.ACCOUNT_ALLOW_REGISTRATION,
    }