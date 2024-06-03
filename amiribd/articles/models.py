from django.db import models
from django.urls import reverse_lazy, reverse
from django_ckeditor_5.fields import CKEditor5Field
from amiribd.users.models import Profile
from django.utils.text import slugify
from django_extensions.db.fields import AutoSlugField


def my_slugify_function(content):
    return content.replace("_", "-").lower()


class Article(models.Model):
    profile = models.ForeignKey(
        Profile,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from="title", slugify_function=my_slugify_function)
    content = CKEditor5Field("Text", config_name="default", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "dashboard:articles:article-detail",
            kwargs={
                "slug": self.slug,
                "tm__year": self.created_at.year,
                "tm__month": self.created_at.month,
                "tm__day": self.created_at.day,
            },
        )

    def get_update_url(self):
        return reverse(
            "dashboard:articles:article-detail-edit",
            kwargs={
                "slug": self.slug,
                "tm__year": self.created_at.year,
                "tm__month": self.created_at.month,
                "tm__day": self.created_at.day,
            },
        )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
