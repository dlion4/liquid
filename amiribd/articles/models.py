import contextlib
import threading
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.db import transaction
from django.urls import reverse
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
from django_extensions.db.fields import AutoSlugField

from amiribd.articles.mixins import ImmutableFieldsMixin
from amiribd.invest.models import Account
from amiribd.transactions.models import Transaction
from amiribd.users.models import Profile

POPULAR_VIEW_COUNT = 1000


def time_diff(duration:str, range:float=1.0)->timedelta:  # noqa: A002
    result = None
    if duration=="minutes":
        result = timezone.timedelta(minutes=range)
    elif duration=="hours":
        result = timezone.timedelta(hours=range)
    elif duration=="days":
        result = timezone.timedelta(days=range)
    elif duration=="weeks":
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
        related_name="aitoken_profile",
    )
    tokens = models.FloatField(
        default=15.00,
        help_text="Each article consumes 0.95 tokens. Refresh every 24 hours")
    consumed_tokens = models.IntegerField(default=0.0)

    def __str__(self):
        return str(self.tokens)

def my_slugify_function(content):
    return content.replace("_", "-").lower()

class TemplateCategory(models.Model):

    title = models.CharField(
        max_length=100, help_text="Blog, Youtube description", unique=True)
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
    cover = models.FileField(upload_to="template/category", blank=True, null=True)

    class Meta:
        verbose_name = "Template Category"
        verbose_name_plural = "Template Categories"

    def __str__(self):
        return self.title

    @property
    def is_new(self):
        return self.timestamp >= timezone.now() - time_diff("days", 7)

    def templates(self):
        return self.category_templates.all()
    @property
    def templates_count(self):
        return self.templates().count()

    def get_article_posts(self):
        return Article.objects.filter(template__category=self)


class Template(models.Model):
    category = models.ForeignKey(
        TemplateCategory, on_delete=models.CASCADE, related_name="category_templates")
    is_premium = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Template"
        verbose_name_plural = "Templates"

    def __str__(self):
        return self.category.title.title()


class Article(ImmutableFieldsMixin, models.Model):
    immutable_fields = ["revenue"]
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
    content = CKEditor5Field("Content")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)
    release_date = models.DateTimeField(
        default=timezone.now, help_text="Time for your post to be visible to audience.")
    views = models.IntegerField(default=0)
    cover = models.FileField(upload_to="template/category", blank=True, null=True)
    archived = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    reads = models.IntegerField(default=0)
    editorsPick = models.BooleanField(default=False)  # noqa: N815
    sponsored = models.BooleanField(default=False)
    recommeded = models.BooleanField(default=False)
    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        revenue = self.revenue
        with transaction.atomic(), contextlib.suppress(Account.DoesNotExist):
            account = Account.objects.get(pool__profile=self.profile)
            threading.Thread(
                target=self.handle_transaction_model,
                args=(
                    self.profile,
                    account,
                    revenue,
                ),
            ).start()
            account.balance += revenue
            account.save()
            super().save(*args, **kwargs)

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

    def handle_transaction_model(self, profile, account, amount):
        Transaction.objects.create(
            profile=profile,
            account=account,
            type="DEPOSIT",
            amount=amount,
            verified=True,
            is_payment_success=True,
            source="Article Revenue",
            currency="KES",
            country="Kenya",
        )

    @property
    def trending(self):
        return bool(self.is_trending())

    @property
    def popular(self):
        return self.is_popular()

    def is_trending(self)->bool:
        return (
            timezone.now() - timedelta(days=3) >= (self.created_at)
        ) and self.is_popular()

    def is_popular(self)->bool:
        return self.views >= POPULAR_VIEW_COUNT

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


def youtube_audio_file_path(instance, filename):
    return f"audio/{instance.profile.user.username}/yt/{filename}"

class YtSummarizer(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True)
    video_url = models.URLField(max_length=255) # the online needed url
    timestamp = models.DateTimeField(auto_now_add=True)
    summary = models.TextField(blank=True)
    transcript_file = models.URLField(blank=True)
    audio_url = models.URLField(max_length=300, blank=True)
    is_processed = models.BooleanField(default=False)
    duration = models.IntegerField(default=0, help_text="in seconds")
    size = models.IntegerField(default=0, help_text="megabytes")
    video_transcript = models.TextField(blank=True)
    is_verified = models.BooleanField(default=True)


    class Meta:
        verbose_name = "YtSummarizer"
        verbose_name_plural = "YtSummarizers"

    def __str__(self):
        return f"Summarizer for {self.video_url}"
