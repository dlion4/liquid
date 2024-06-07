# ruff: noqa: ERA001, E501
"""Base settings to build other settings files upon."""

from pathlib import Path
from dotenv import load_dotenv
import environ

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
DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
# https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-DEFAULT_AUTO_FIELD
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"
# INVEST,ENT UR;LS
# ------------------------------------------------------------------------------
FIRST_INVESTMENT_URL = "dashboard:invest:invest"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
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
    "allauth",
    "allauth.account",
    "allauth.mfa",
    "allauth.socialaccount",
    "django_htmx",
    "after_response",
    "nested_inline",
    # "django.contrib.gis",
    "rest_framework",  # utilities for rest apis
    "rest_framework.authtoken",  # token authentication
    "django_filters",  # for filtering rest endpoints
    "easyaudit",  # for recordign all the user events
    "django_apscheduler",  # backup and othe rtask scheduling
    "dbbackup",  # django-dbbackup
    # "ckeditor",  # https://pypi.org/project/django-ckeditor/#installation
    "django_ckeditor_5",
    "ckeditor_uploader",  # https://pypi.org/project/django-ckeditor-uploader/#installation
    "widget_tweaks",

]
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
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# BACKUP FOLDER AD SETTINGS
# ------------------------------------------------------------------------------
DB_BACKUP_FOLDER = str(BASE_DIR / "db_backup")
DBBACKUP_STORAGE = "django.core.files.storage.FileSystemStorage"
DBBACKUP_STORAGE_OPTIONS = {"location": DB_BACKUP_FOLDER}

# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
MIGRATION_MODULES = {"sites": "amiribd.contrib.sites.migrations"}

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "users.backends.TokenAuthenticationBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
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
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    # cahcing
    # "django.middleware.cache.UpdateCacheMiddleware",
    # "django.middleware.common.CommonMiddleware",
    # "django.middleware.cache.FetchFromCacheMiddleware",
    # account status middleware
    "amiribd.dashboard.middleware.AccountStatusMiddleware",
    "easyaudit.middleware.easyaudit.EasyAuditMiddleware",
]

# CACHE_MIDDLEWARE_ALIAS = "default"  # The cache alias to use for storage.
# CACHE_MIDDLEWARE_SECONDS = (
#     60 * 60 * 60
# )  # The number of seconds each page should be cached.


COMPRESS_ENABLED = True
COMPRESS_CSS_HASHING_METHOD = "content"

HTML_MINIFY = True
KEEP_COMMENTS_ON_MINIFYING = True
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
                "amiribd.users.context_processors.allauth_settings",
                # liquid app processor
                "amiribd.liquid.context_processors.liquid_site_data",
                "amiribd.invest.context_processors.withdrawal_form_action",
                "amiribd.htmx.context_processors.display_add_plan_form",
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
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"

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
# ------------------------------------------------------------------------------
# Django CLIENT Dashboard URL
DASHBOARD_URL = env.str("DJANGO_DASHBOARD_URL", default="dashboard:home")
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""kwasa""", "support@earnkraft.com")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
# https://cookiecutter-django.readthedocs.io/en/latest/settings.html#other-environment-settings
# Force the `admin` sign in process to go through the `django-allauth` workflow
DJANGO_ADMIN_FORCE_ALLAUTH = env.bool("DJANGO_ADMIN_FORCE_ALLAUTH", default=False)

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


# django-allauth
# ------------------------------------------------------------------------------
ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_AUTHENTICATION_METHOD = "email"
# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_EMAIL_REQUIRED = True
# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_USERNAME_REQUIRED = False
# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_ADAPTER = "amiribd.users.adapters.AccountAdapter"
# https://docs.allauth.org/en/latest/account/forms.html
ACCOUNT_FORMS = {"signup": "amiribd.users.forms.UserSignupForm"}
# https://docs.allauth.org/en/latest/socialaccount/configuration.html
SOCIALACCOUNT_ADAPTER = "amiribd.users.adapters.SocialAccountAdapter"
# https://docs.allauth.org/en/latest/socialaccount/configuration.html
SOCIALACCOUNT_FORMS = {"signup": "amiribd.users.forms.UserSocialSignupForm"}
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


# MENTENANCE MODE

MAINTENANCE_MODE = False


import platform
import environ
import os

# NINJA API

NINJA_API_ENABLED = True

# DJANGO RESTFRAMWORK SETEUP
# -------------------------------------------------------

# Django Rest Framework
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": int(os.getenv("DJANGO_PAGINATION_LIMIT", 10)),
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


# cskeditor
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
            ]
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
                {"name": "/.*/", "attributes": True, "classes": True, "styles": True}
            ]
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
                }
            ]
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
            ]
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
            "container": "document.querySelector('#presence-list-container')"
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
                        }
                    ]
                },
            }
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
            "tokenUrl": "https://110069.cke-cs.com/token/dev/QFSgjaKo9ZSzY6iuKSMwomhekcA4bCbrYKOp?limit=10"
        },
        "ai": {
            # AI Assistant feature configuration.
            # https://ckeditor.com/docs/ckeditor5/latest/features/ai-assistant.html
            "aiAssistant": {"contentAreaCssClass": "formatted"},
            # Configure one of the supported AI integration: OpenAI, Azure OpenAI, Amazon Bedrock
            # https://ckeditor.com/docs/ckeditor5/latest/features/ai-assistant/ai-assistant-integration.html#integration
            "openAI": {
                # apiUrl: 'https://url.to.your.application/ai'
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
            ]
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
            # Careful, with the Mathtype plugin CKEditor will not load when loading this sample
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


