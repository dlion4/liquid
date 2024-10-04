from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


def get_site_protocol(request):
    protocol = "http"
    if request.is_secure():
        protocol = "https"
    return protocol



def allauth_settings(request):
    """Expose some settings from django-allauth in templates."""
    return {
        "ACCOUNT_ALLOW_REGISTRATION": settings.ACCOUNT_ALLOW_REGISTRATION,
        "website_base_url":f"{get_site_protocol(request)}://{get_current_site(request).domain}",
    }

