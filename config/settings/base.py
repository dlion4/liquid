# ruff: noqa: ERA001, E501
"""Base settings to build other settings files upon."""

import os
from pathlib import Path
import resend
import environ
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

from .unfold import DJANGO_UNFOLD_SIDEBAR_NAVIGATION

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

load_dotenv()

# amiribd/
APPS_DIR = BASE_DIR / "amiribd"

env = environ.Env()

# READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=True)
READ_DOT_ENV_FILE = True
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(BASE_DIR / ".env"))

# resend.api_key = env.str("RESEND_EMAIL_SERVICE_API_KEY")

ALLOWED_HOSTS = env.list(
    "DJANGO_ALLOWED_HOSTS", default=["127.0.0.1", "localhost"])
# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "UTC"
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-us"
# https://docs.djangoproject.com/en/dev/ref/settings/#languages
# from django.utils.translation import gettext_lazy as _
# LANGUAGES = [
#     ('en', _('English')),
#     ('fr-fr', _('French')),
#     ('pt-br', _('Portuguese')),
# ]
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [str(BASE_DIR / "locale")]

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    "default": env.db("DATABASE_URL"),
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-DEFAULT_AUTO_FIELD
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"
ROOT_API_URLCONF = "api.urls"
# INVEST,ENT UR;LS
# ------------------------------------------------------------------------------
FIRST_INVESTMENT_URL = "dashboard:invest:invest"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [

    "unfold",  # before django.contrib.admin
    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.forms",  # optional, if special form elements are needed
    "unfold.contrib.inlines",  # optional, if special inlines are needed
    "unfold.contrib.import_export",  # optional, if django-import-export package is used
    "unfold.contrib.guardian",  # optional, if django-guardian package is used
    "unfold.contrib.simple_history",  # optional, if django-simple-history package is used

    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",  # Handy template tags
    "django.contrib.admin",
    "django.forms",
]
THIRD_PARTY_APPS = [
    "crispy_forms",
    "crispy_bootstrap5",
    "django_htmx",
    "after_response",
    "nested_inline",
    # "django.contrib.gis",
    "rest_framework",  # utilities for rest apis
    "rest_framework.authtoken",  # token authentication
    "django_filters",  # for filtering rest endpoints
    "easyaudit",  # for recording all the user events
    # "django_apscheduler",  # backup and other task scheduling
    # "dbbackup",  # django-dbbackup
    # "ckeditor",  # https://pypi.org/project/django-ckeditor/#installation
    "django_ckeditor_5",
    "ckeditor_uploader",  # https://pypi.org/project/django-ckeditor-uploader/#installation
    "widget_tweaks",

    "django_celery_beat",
    # for monitoring application healths
    "silk",
    "django_extensions",
    
    'allauth',
    'allauth.account',

    # Optional -- requires install using `django-allauth[socialaccount]`.
    'allauth.socialaccount',
    # ... include the providers you want to enable:
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.google',
    
    #  ... html minification tools
    "htmlmin",
]


# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': env.str("GOOGLE_OAUTH_CLIENT_ID"),
            'secret': env.str("GOOGLE_OAUTH_CLIENT_SECRET"),
        },
        'SCOPE': ['email', 'profile'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'INIT_PARAMS': {'login_hint': 'email'},
        'FIELDS': [
            'id', 'email', 'name', 'first_name', 'last_name',
            'username', 'picture', 'account_type'],
        'EXCHANGE_TOKEN': True,
        "METHOD": "oauth2",
        'LOCALE_FUNC': 'django_localflavor_br.i18n.locale_name_to_python',
        "VERIFIED_EMAIL": True,
        'EMAIL_AUTHENTICATION': True,
    },
    'github': {
        'APP': {
            'client_id': env.str("GITHUB_OAUTH_CLIENT_ID"),
            'secret': env.str("GITHUB_OAUTH_CLIENT_SECRET"),
        },
        'SCOPE': [
            'user',
            'repo',
            'read:org',
        ],
    }
}


# django-allauth
# ------------------------------------------------------------------------------
# https://docs.allauth.org/en/latest/socialaccount/configuration.html
SOCIALACCOUNT_ADAPTER = "amiribd.users.adapters.SocialAccountAdapter"
# Disable automatic redirect to signup when user exists
ACCOUNT_ALLOW_REGISTRATION=env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
SOCIALACCOUNT_AUTO_SIGNUP=True
SOCIALACCOUNT_LOGIN_ON_GET=True
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT=True
SOCIALACCOUNT_EMAIL_VERIFICATION = False
SOCIALACCOUNT_ONLY =True
ACCOUNT_EMAIL_VERIFICATION = "none"  # or "none"

LOCAL_APPS = [
    "amiribd.users",
    # Your stuff: custom apps go here
    "amiribd.liquid",
    # posts
    "amiribd.posts",
    # dashboard
    "amiribd.dashboard",
    # investors
    "amiribd.invest",
    # money
    "amiribd.transactions",
    # profiles
    "amiribd.profiles",
    # tokens
    "amiribd.tokens",
    "amiribd.profilesettings",
    "amiribd.payments",
    # subscriptions
    "amiribd.subscriptions",
    # streams
    "amiribd.streams",
    # articles
    "amiribd.articles",
    "amiribd.schemes",
    # shops for sales of items fro the members
    "amiribd.shops",
    # jobs
    "amiribd.jobs",
    # conversion rates
    "amiribd.rates",
    # apis
    "amiribd.apis",
    # application for running and registering adverts for display in other
    # appwebsites will deponed on the apis app for external websites to access the adverst registered by the users of our
    # platforms
    "amiribd.adverts",
    # market apps fro the different packages
    "amiribd.markets",
    # core apps
    "amiribd.core",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# BACKUP FOLDER AD SETTINGS
# ------------------------------------------------------------------------------
# DB_BACKUP_FOLDER = str(BASE_DIR / "db_backup")
# DBBACKUP_STORAGE = "django.core.files.storage.FileSystemStorage"
# DBBACKUP_STORAGE_OPTIONS = {"location": DB_BACKUP_FOLDER}

# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
MIGRATION_MODULES = {"sites": "amiribd.contrib.sites.migrations"}

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "users.backends.TokenAuthenticationBackend",
    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "users.User"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "home"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = "users:login"
SIGNUP_URL = "users:signup"
# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    # Add the account middleware:
    "allauth.account.middleware.AccountMiddleware",
    # ...
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    # caching
    # "django.middleware.cache.UpdateCacheMiddleware",
    # "htmlmin.middleware.HtmlMinifyMiddleware",
    # other middleware classes
    # "django.middleware.cache.FetchFromCacheMiddleware",
    # "htmlmin.middleware.MarkRequestMiddleware",
    # to check authentication status
    "amiribd.users.middleware.AuthenticationStateCheckMiddleware",
    "amiribd.users.middleware.BasicAuthMiddleware",  # for the silk popup authentication
    "amiribd.users.middleware.CustomXFrameOptionsMiddleware",  # x frame option
    "amiribd.users.middleware.ContentSecurityPolicyMiddleware",  # x frame option
    # custom load secret variables
    "amiribd.tokens.middleware.load_secrets.LoadSecretsMiddleware",
    # account status middleware
    "amiribd.dashboard.middleware.AccountStatusMiddleware",
    "silk.middleware.SilkyMiddleware",
    "easyaudit.middleware.easyaudit.EasyAuditMiddleware",
]

# CACHE_MIDDLEWARE_ALIAS = "default"  # The cache alias to use for storage.
# CACHE_MIDDLEWARE_SECONDS = (60 * 60)

# HTML_MINIFY = True
# EXCLUDE_FROM_MINIFYING = ("^admin/",)
# KEEP_COMMENTS_ON_MINIFYING = True
CONSERVATIVE_WHITESPACE_ON_MINIFYING = False

COMPRESS_ENABLED = True
COMPRESS_CSS_HASHING_METHOD = "content"

JWT_ISSUER = env.str("JWT_ISSUER", "")
JWT_AUDIENCE = env.str("JWT_AUDIENCE", "")

# HTML_MINIFY = True
# KEEP_COMMENTS_ON_MINIFYING = True
# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(BASE_DIR / "staticfiles")
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [str(APPS_DIR / "static")]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "media/"
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR / "media")

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#dirs
        "DIRS": [str(APPS_DIR / "templates")],
        # https://docs.djangoproject.com/en/dev/ref/settings/#app-dirs
        "APP_DIRS": True,
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                # liquid app processor
                "amiribd.liquid.context_processors.liquid_site_data",
                "amiribd.invest.context_processors.withdrawal_form_action",
                "amiribd.htmx.context_processors.display_add_plan_form",
                "amiribd.payments.context_processors.payment_context_data",

                # secret template processor from. the secrets
                "amiribd.tokens.context_processors.load_secrets",
                "amiribd.transactions.context_processors.deposit_form_action",
                "amiribd.users.context_processors.allauth_settings",
                # `allauth` needs this from django
                "django.template.context_processors.request",
            ],
        },
    },
]

# https://docs.djangoproject.com/en/dev/ref/settings/#form-renderer
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(APPS_DIR / "fixtures"),)

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
# CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
# X_FRAME_OPTIONS = "DENY"

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5


# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"
# STUFF ADMIN
# ------------------------------------------------------------------------------
STUFF_ADMIN_URL="earnkraft/"
# ------------------------------------------------------------------------------
# Django CLIENT Dashboard URL
DASHBOARD_URL = env.str("DJANGO_DASHBOARD_URL", default="dashboard:home")
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""kwasa""", "support@earnkraft.com")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
# https://cookiecutter-django.readthedocs.io/en/latest/settings.html#other-environment-settings

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "users": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}

# django-compressor
# ------------------------------------------------------------------------------
# https://django-compressor.readthedocs.io/en/latest/quickstart/#installation
INSTALLED_APPS += ["compressor"]
STATICFILES_FINDERS += ["compressor.finders.CompressorFinder"]

# Your stuff...
# ------------------------------------------------------------------------------

# authentication
LOGIN_BY_CODE_ENABLED = True

# SESAME CONFIGURATIONS
# SESAME_MAX_AGE = 300  # 300 seconds = 5 minutes


# MAINTENANCE MODE

MAINTENANCE_MODE = False


# NINJA API

NINJA_API_ENABLED = True

# DJANGO RESTFRAMWORK SETEUP
# -------------------------------------------------------

# Django Rest Framework
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": int(os.getenv("DJANGO_PAGINATION_LIMIT", str(10))),
    "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%S%z",
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
}


# SESSION_COOKIE_DOMAIN = ".localhost"


CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}

# ckeditor
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = "uploads/"


# Define a list of allowed plugins
CKEDITOR_ALLOWED_PLUGINS = [
    "Bold",
    "Italic",
    "Underline",
    "List",
    "Autoformat",
    "Mention",
]

# Simulate the builtinPlugins as a list of dictionaries
CKEDITOR_BUILTIN_PLUGINS = [
    {"pluginName": "Bold"},
    {"pluginName": "Italic"},
    {"pluginName": "Underline"},
    {"pluginName": "List"},
    {"pluginName": "Autoformat"},
    {"pluginName": "Mention"},
    {"pluginName": "OtherPlugin"},
]


# Filter the plugins
CKEDITOR_FILTERED_PLUGINS = [
    plugin["pluginName"]
    for plugin in CKEDITOR_BUILTIN_PLUGINS
    if plugin["pluginName"] in CKEDITOR_ALLOWED_PLUGINS
]


CKEDITOR_5_CONFIGS = {
    "default": {
        # https://ckeditor.com/docs/ckeditor5/latest/features/toolbar/toolbar.html#extended-toolbar-configuration-format
        "toolbar": {
            "items": [
                "aiCommands",
                "aiAssistant",
                "|",
                "ckbox",
                # "uploadImage",
                "|",
                "exportPDF",
                "exportWord",
                "|",
                "comment",
                "trackChanges",
                "revisionHistory",
                "|",
                "findAndReplace",
                "selectAll",
                "formatPainter",
                "|",
                "undo",
                "redo",
                # "-",
                "|",
                "bold",
                "italic",
                "strikethrough",
                "underline",
                "removeFormat",
                "|",
                "bulletedList",
                "numberedList",
                "multiLevelList",
                "todoList",
                "|",
                "outdent",
                "indent",
                "|",
                "alignment",
                "|",
                "subscript",
                "superscript",
                "-",
                "heading",
                "|",
                "fontSize",
                "fontFamily",
                "fontColor",
                "fontBackgroundColor",
                "highlight",
                "|",
                "link",
                "blockQuote",
                "insertTable",
                "mediaEmbed",
                "tableOfContents",
                "insertTemplate",
                "|",
                "specialCharacters",
                "horizontalLine",
                "pageBreak",
            ],
            "shouldNotGroupWhenFull": True,
        },
        # Changing the language of the interface requires loading the language file using the <script> tag.
        # "language": "e",
        "list": {"properties": {"styles": True, "startIndex": True, "reversed": True}},
        # https://ckeditor.com/docs/ckeditor5/latest/features/headings.html#configuration
        "heading": {
            "options": [
                {
                    "model": "paragraph",
                    "title": "Paragraph",
                    "class": "ck-heading_paragraph",
                },
                {
                    "model": "heading1",
                    "view": "h1",
                    "title": "Heading 1",
                    "class": "ck-heading_heading1",
                },
                {
                    "model": "heading2",
                    "view": "h2",
                    "title": "Heading 2",
                    "class": "ck-heading_heading2",
                },
                {
                    "model": "heading3",
                    "view": "h3",
                    "title": "Heading 3",
                    "class": "ck-heading_heading3",
                },
                {
                    "model": "heading4",
                    "view": "h4",
                    "title": "Heading 4",
                    "class": "ck-heading_heading4",
                },
                {
                    "model": "heading5",
                    "view": "h5",
                    "title": "Heading 5",
                    "class": "ck-heading_heading5",
                },
                {
                    "model": "heading6",
                    "view": "h6",
                    "title": "Heading 6",
                    "class": "ck-heading_heading6",
                },
            ],
        },
        # https://ckeditor.com/docs/ckeditor5/latest/features/font.html#configuring-the-font-family-feature
        "fontFamily": {
            "options": [
                "default, Roboto, Poppins",
                "Arial, Helvetica, sans-serif",
                "Courier New, Courier, monospace",
                "Georgia, serif",
                "Lucida Sans Unicode, Lucida Grande, sans-serif",
                "Tahoma, Geneva, sans-serif",
                "Times New Roman, Times, serif",
                "Trebuchet MS, Helvetica, sans-serif",
                "Verdana, Geneva, sans-serif",
            ],
            "supportAllValues": True,
        },
        # https://ckeditor.com/docs/ckeditor5/latest/features/font.html#configuring-the-font-size-feature
        "fontSize": {
            "options": [
                10,
                12,
                14,
                "default",
                18,
                20,
                22,
                24,
                26,
                28,
                30,
                48,
                50,
            ],
            "supportAllValues": True,
        },
        # Be careful with the setting below. It instructs CKEditor to accept ALL HTML markup.
        # https://ckeditor.com/docs/ckeditor5/latest/features/general-html-support.html#enabling-all-html-features
        "htmlSupport": {
            "allow": [
                {"name": "/.*/", "attributes": True, "classes": True, "styles": True},
            ],
        },
        # Be careful with enabling previews
        # https://ckeditor.com/docs/ckeditor5/latest/features/html-embed.html#content-previews
        "htmlEmbed": {"showPreviews": True},
        # https://ckeditor.com/docs/ckeditor5/latest/features/mentions.html#configuration
        "mention": {
            "feeds": [
                {
                    "marker": "@",
                    "feed": [
                        "@apple",
                        "@bears",
                        "@brownie",
                        "@cake",
                        "@cake",
                        "@candy",
                        "@canes",
                        "@chocolate",
                        "@cookie",
                        "@cotton",
                        "@cream",
                        "@cupcake",
                        "@danish",
                        "@donut",
                        "@dragée",
                        "@fruitcake",
                        "@gingerbread",
                        "@gummi",
                        "@ice",
                        "@jelly-o",
                        "@liquorice",
                        "@macaroon",
                        "@marzipan",
                        "@oat",
                        "@pie",
                        "@plum",
                        "@pudding",
                        "@sesame",
                        "@snaps",
                        "@soufflé",
                        "@sugar",
                        "@sweet",
                        "@topping",
                        "@wafer",
                    ],
                    "minimumCharacters": 1,
                },
            ],
        },
        "template": {
            "definitions": [
                {
                    "title": "The title of the template",
                    "description": "A longer description of the template",
                    "data": "<p>Data inserted into the content</p>",
                },
                {
                    "title": "Annual financial report",
                    "description": "A report that spells out the company's financial condition.",
                    "data": "",
                },
            ],
        },
        # https://ckeditor.com/docs/ckeditor5/latest/features/editor-placeholder.html#using-the-editor-configuration
        "placeholder": "Welcome to Liquid 5!",
        # Used by real-time collaboration
        "cloudServices": {
            # Be careful - do not use the development token endpoint on production systems!
            "tokenUrl": "https://110069.cke-cs.com/token/dev/QFSgjaKo9ZSzY6iuKSMwomhekcA4bCbrYKOp?limit=10",
            "webSocketUrl": "wss://110069.cke-cs.com/ws",
            "uploadUrl": "https://110069.cke-cs.com/easyimage/upload/",
        },
        # "collaboration": {
        #     # Modify the channelId to simulate editing different documents
        #     # https://ckeditor.com/docs/ckeditor5/latest/features/collaboration/real-time-collaboration/real-time-collaboration-integration.html#the-channelid-configuration-property
        #     "channelId": "document-id-8"
        # },
        # https://ckeditor.com/docs/ckeditor5/latest/features/collaboration/annotations/annotations-custom-configuration.html#sidebar-configuration
        "sidebar": {"container": "document.querySelector('#sidebar')"},
        "documentOutline": {"container": "document.querySelector('#outline')"},
        # https://ckeditor.com/docs/ckeditor5/latest/features/collaboration/real-time-collaboration/users-in-real-time-collaboration.html#users-presence-list
        "presenceList": {
            "container": "document.querySelector('#presence-list-container')",
        },
        # Add configuration for the comments editor if the Comments plugin is added.
        # https://ckeditor.com/docs/ckeditor5/latest/features/collaboration/annotations/annotations-custom-configuration.html#comment-editor-configuration
        "comments": {
            "editorConfig": {
                "extraPlugins": CKEDITOR_FILTERED_PLUGINS,
                # Combine mentions + Webhooks to notify users about new comments
                # https://ckeditor.com/docs/cs/latest/guides/webhooks/events.html
                "mention": {
                    "feeds": [
                        {
                            "marker": "@",
                            "feed": [
                                "@Baby Doe",
                                "@Joe Doe",
                                "@Jane Doe",
                                "@Jane Roe",
                                "@Richard Roe",
                            ],
                            "minimumCharacters": 1,
                        },
                    ],
                },
            },
        },
        # Do not include revision history configuration if you do not want to integrate it.
        # Remember to remove the 'revisionHistory' button from the toolbar in such a case.
        # "revisionHistory": {
        #     "editorContainer": "document.querySelector('#editor-container')",
        #     "viewerContainer": "document.querySelector('#revision-viewer-container')",
        #     "viewerEditorElement": "document.querySelector('#revision-viewer-editor')",
        #     "viewerSidebarContainer": "document.querySelector('#revision-viewer-sidebar')"
        # },
        # https://ckeditor.com/docs/ckeditor5/latest/features/images/image-upload/ckbox.html
        "ckbox": {
            # Be careful - do not use the development token endpoint on production systems!
            "tokenUrl": "https://110069.cke-cs.com/token/dev/QFSgjaKo9ZSzY6iuKSMwomhekcA4bCbrYKOp?limit=10",
        },
        "ai": {
            # AI Assistant feature configuration.
            # https://ckeditor.com/docs/ckeditor5/latest/features/ai-assistant.html
            "aiAssistant": {"contentAreaCssClass": "formatted"},
            # Configure one of the supported AI integration: OpenAI, Azure OpenAI, Amazon Bedrock
            # https://ckeditor.com/docs/ckeditor5/latest/features/ai-assistant/ai-assistant-integration.html#integration
            "openAI": {
                "apiUrl": "https://url.to.your.application/ai",
            },
        },
        "style": {
            "definitions": [
                {
                    "name": "Article category",
                    "element": "h3",
                    "classes": ["category"],
                },
                {"name": "Info box", "element": "p", "classes": ["info-box"]},
            ],
        },
        # License key is required only by the Pagination plugin and non-realtime Comments/Track changes.
        "licenseKey": "WVJOOHVieTNyaEVQTk9zbGFaR2RKdHhsRHlESUpKdHhsUkRlbmg1MVZRUTlvaXBaMnJTTXhvQ2xIeTh4bmc9PS1NakF5TkRBMk1Uaz0=",
        "removePlugins": [
            # Before enabling Pagination plugin, make sure to provide proper configuration and add relevant buttons to the toolbar
            # https://ckeditor.com/docs/ckeditor5/latest/features/pagination/pagination.html
            "Pagination",
            # Intentionally disabled, file uploads are handled by CKBox
            "Base64UploadAdapter",
            # Intentionally disabled, file uploads are handled by CKBox
            "CKFinder",
            # Intentionally disabled, file uploads are handled by CKBox
            "EasyImage",
            # Requires additional license key
            "WProofreader",
            # Incompatible with real-time collaboration
            "SourceEditing",
            # Careful, with the Math type plugin CKEditor will not load when loading this sample
            # from a local file system (file://) - load this site via HTTP server if you enable MathType
            "MathType",
            # If you would like to adjust enabled collaboration features:
            # 'RealTimeCollaborativeComments',
            # / 'RealTimeCollaborativeTrackChanges',
            # 'RealTimeCollaborativeRevisionHistory',
            # 'PresenceList',
            # 'Comments',
            # 'TrackChanges',
            # 'TrackChangesData',
            # 'RevisionHistory',
        ],
    },
}


CKEDITOR_5_FILE_STORAGE = "config.settings.storage.CKEditorFileStorage"

CK_EDITOR_5_UPLOAD_FILE_VIEW_NAME = "image_upload"

CORS_ALLOW_ALL_ORIGINS = False  # Change this based on your needs

# Allow specific origins
CORS_ALLOWED_ORIGINS = [
    "https://auth.earnkraft.com",
    "https://dashboard.earnkraft.com",
    "https://app.earnkraft.com",
]

# Allow sending cookies and credentials with CORS requests
CORS_ALLOW_CREDENTIALS = True

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = [
    "https://auth.earnkraft.com",
    "https://dashboard.earnkraft.com",
    "https://app.earnkraft.com",
]

# Allowed HTTP methods for CORS
CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]

# X-Frame-Options (consider using SAMEORIGIN)
X_FRAME_OPTIONS = "SAMEORIGIN"  # or handle it differently

UNFOLD = {
    "SITE_SYMBOL": "speed",
    "SHOW_VIEW_ON_SITE": True, # show/hide "View on site" button, default: True
    "ENVIRONMENT": "core.environment_callback",
    "DASHBOARD_CALLBACK": "core.dashboard_callback", # show/hide "View on site" button, default: True
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "en": "🇬🇧",
                "fr": "🇫🇷",
                "nl": "🇧🇪",
            },
        },
    },
    "SIDEBAR": {
        "show_search": True,  # Search in applications and models names
        "show_all_applications": True,  # Dropdown with all applications and models
        "navigation": DJANGO_UNFOLD_SIDEBAR_NAVIGATION,
    },

    "TABS": [
        {
            "models": [
                "articles.article",
            ],
            "items": [
                {
                    "title": _("Article"),
                    "link": reverse_lazy("earnkraft:articles_article_changelist"),
                    "permission": lambda request: request.user.is_staff,
                },
            ],
        },
    ],
}


# GOOGLE GEMINI API  SETTINGS

GOOGLE_GEMINI_API_KEY = env.str("GOOGLE_GEMINI_API_KEY", default="")

ZERO_BOUNCE_EMAIL_VALIDATION_PROJECT_TOKEN=env.str("ZERO_BOUNCE_EMAIL_VALIDATION_PROJECT_TOKEN",  default="")



