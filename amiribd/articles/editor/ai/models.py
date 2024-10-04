from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import AutoSlugField

from amiribd.articles.models import my_slugify_function
from amiribd.users.models import Profile


class AIHistory(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.DO_NOTHING, blank=True, null=True,
        related_name="profile_ai_history")
    title = models.CharField(max_length=1000)
    slug = AutoSlugField(populate_from="title", slugify_function=my_slugify_function)
    question = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "History"
        verbose_name_plural = "Histories"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "dashboard:articles:editor:new-article-ai-edit",
            kwargs={
                "pk": self.pk,
                "slug": self.slug,
            })
