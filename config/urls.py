# ruff: noqa
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views import defaults as default_views
from sesame.views import LoginView
from amiribd.articles.editor import views as ck_editor_views
from amiribd.core.admin import earnkraft_site

urlpatterns = [
    # root urls
    path(
        "",
        include(
            "amiribd.liquid.urls",
        ),
    ),
    # posts urls
    path(
        "posts/",
        include(
            "amiribd.posts.urls",
            namespace="posts",
        ),
    ),
    # Django Admin, use {% url 'admin:index' %} 
    # main admin site for super users
    path(settings.ADMIN_URL, admin.site.urls),
    # main admin site for stuff users
    # path(settings.STUFF_ADMIN_URL, include(earnkraft_site.urls)),
    path(settings.STUFF_ADMIN_URL, earnkraft_site.urls, name='stuff_admin'),
    # User management
    path("users/", include("amiribd.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
    # ...
    path("sesame/login/", LoginView.as_view(), name="sesame-login"),
    path(
        "dashboard/",
        include(
            "amiribd.dashboard.urls",
            namespace="dashboard",
        ),
    ),
    path(
        "kyc/dashboard/",
        include(
            "amiribd.dashboard.kyc.urls",
            namespace="kyc",
        ),
    ),
    # path("monee/dashboard/invest/", include("amiribd.invest.urls", namespace="invest")),
    # Htmx actions and related views
    path(
        "htmx/",
        include(
            "amiribd.htmx.urls",
            namespace="htmx",
        ),
    ),
    # path("monee/dashboard/invest/", include("amiribd.invest.urls", namespace="invest")),
    # Htmx actions and related views
    path("settings/", include("amiribd.profilesettings.urls", namespace="settings")),
    # transaction related urls
    path(
        "transactions/", include("amiribd.transactions.urls", namespace="transactions")
    ),
    # mpesa test callbacks
    path(
        "apis/",
        include(
            "amiribd.apis.urls",
            namespace="apis",
        ),
    ),
    path("profiles/", include("amiribd.profiles.urls", namespace="profiles")),
    path(
        "subscriptions/",
        include("amiribd.subscriptions.urls", namespace="subscriptions"),
    ),
    # ckeditor
    # path("ckeditor/", include("ckeditor_uploader.urls")),
    path(
        "ckeditor5/image-upload/",
        ck_editor_views.ck_editor_upload_files,
        name="image_upload",
    ),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("ai/", include("amiribd.ai.urls", namespace="ai")),
    # shops urls
    path("shops/", include("amiribd.shops.urls", namespace="shops")),
    # jobs urls
    path("jobs/", include("amiribd.jobs.urls", namespace="jobs")),

    # payments
    path("payments/", include("amiribd.payments.urls", namespace="payments")),
    # silk interface
    path("silk/", include('silk.urls', namespace="silk")),

    # post ai generation

    path("ai/assistant/", include("assistant.urls", namespace="assistant")),

    # streams for the notifications and other realtime chats
    # path("streams/",include("amiribd.streams.urls", namespace="streams")),
]


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# Admin Site Settings

admin.site.site_title = "Earnkraft Agencies"
admin.site.site_header = "Earnkraft administration"
admin.site.index_title = "Earnkraft Agencies"

