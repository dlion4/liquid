import os
from urllib.parse import urljoin

from django.conf import settings
from django.core.files.storage import FileSystemStorage


class CKEditorFileStorage(FileSystemStorage):
    """Custom storage for django_ckeditor_5 images."""

    def __init__(self, *args, **kwargs):
        kwargs["location"] = os.path.join(settings.MEDIA_ROOT, "django_ckeditor_5")  # noqa: PTH118
        kwargs["base_url"] = urljoin(settings.MEDIA_URL, "django_ckeditor_5/")
        super().__init__(*args, **kwargs)
