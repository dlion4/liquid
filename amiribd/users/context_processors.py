from django.contrib.sites.shortcuts import get_current_site


def get_site_protocol(request):
    return "https" if request.is_secure() else "http"



