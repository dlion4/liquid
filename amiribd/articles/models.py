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
    color = models.CharField(max_length=100, choices=(
        ("primary", "primary"),
        ("secondary", "secondary"),
        ("danger", "danger"),
        ("info", "info"),
        ("warning", "warning"),
        ("success", "success"),
    ), default="primary")

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
    
    def get_article_posts(self):
        # Access articles through related templates
        return Article.objects.filter(template__category=self)

    

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
    summary = models.TextField(blank=True)
    content = CKEditor5Field("Content",)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)
    release_date = models.DateTimeField(default=timezone.now, help_text="Time for your post to be visible to audience.")
    views = models.IntegerField(default=0)
    archived = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    reads = models.IntegerField(default=0)
    editorsPick = models.BooleanField(default=False)
    sponsored = models.BooleanField(default=False)
    recommeded = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.title
    
    @property
    def trending(self):
        return self.is_trending()
    
    @property
    def popular(self):
        return self.is_popular()

    def is_trending(self)->bool:
        return timezone.now() - timedelta(days=3) >= self.created_at and self.views > 1000
    
    def is_popular(self)->bool:
        return self.views >= 1000


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

class YtSummarizer(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    video_url = models.URLField(max_length=255) # the online needed url
    timestamp = models.DateTimeField(auto_now_add=True)
    summary = models.TextField(blank=True)
    audio_file = models.URLField(max_length=2000, blank=True, null=True)
    is_processed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "YtSummarizer"
        verbose_name_plural = "YtSummarizers"
    
    def __str__(self):
        return f"Summarizer for {self.video_url}"
