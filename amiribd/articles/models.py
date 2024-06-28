from django.db import models
from django.urls import reverse_lazy, reverse
from django_ckeditor_5.fields import CKEditor5Field
from amiribd.users.models import Profile
from django.utils.text import slugify
from django_extensions.db.fields import AutoSlugField
from django.utils import timezone
from datetime import timedelta


def time_diff(duration:str, range:float=1)->timedelta:
    result = None
    if duration=='minutes':
        result = timezone.timedelta(minutes=range)
    elif duration=='hours':
        result = timezone.timedelta(hours=range)
    elif duration=='days':
        result = timezone.timedelta(days=range)
    elif duration=='weeks':
        result = timezone.timedelta(weeks=range)
    else:
        result = timezone.timedelta(days=range)

    return result

class AiToken(models.Model):
    profile = models.OneToOneField(
        Profile,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="aitoken_profile"
    )
    tokens = models.FloatField(default=15.00, help_text="Each article consumes 0.95 tokens. Refresh every 24 hours")
    consumed_tokens = models.IntegerField(default=0.0)

def my_slugify_function(content):
    return content.replace("_", "-").lower()

class TemplateCategory(models.Model):

    title = models.CharField(max_length=100, help_text="Blog, Youtube description", unique=True)
    description = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    icon = models.CharField(default="icon ni ni-spark-fill", max_length=100)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "Template Category"
        verbose_name_plural = "Template Categories"

    @property
    def is_new(self):
        return self.timestamp >= timezone.now() - time_diff('days', 7)
    
    def templates(self):
        return self.category_templates.all()
    @property
    def templates_count(self):
        return self.templates().count()
    

    
    

class Template(models.Model):
    category = models.ForeignKey(TemplateCategory, on_delete=models.CASCADE, related_name="category_templates")
    is_premium = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Template"
        verbose_name_plural = "Templates"

    def __str__(self):
        return self.category.title.title()



class Article(models.Model):
    profile = models.ForeignKey(
        Profile,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    template = models.ForeignKey(
        Template,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="article_template",
    )
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from="title", slugify_function=my_slugify_function)
    content = CKEditor5Field("Text",)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)
    release_date = models.DateTimeField(default=timezone.now, help_text="Time for your post to be visible to audience.")
    

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

