from django.http import HttpRequest
from django.urls import include


def custom_url_dispatcher(request: HttpRequest):
    if request.path.startswith("/auth/api/"):
        from api.urls import urlpatterns as api_urls
        return include(api_urls)(request)
    from config.urls import urlpatterns as main_urls

    return include(main_urls)(request)
