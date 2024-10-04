from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from amiribd.users.models import Profile
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="title")
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        Profile, verbose_name=_(""), on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "posts:post_detail",
            kwargs={
                "slug": self.slug,
                "year": self.date_posted.year,
                "month": self.date_posted.month,
                "day": self.date_posted.day,
            },
        )
