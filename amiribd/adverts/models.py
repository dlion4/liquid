from django.db import models
from amiribd.markets.models import Package
from utils.upload_urls import advertizement_design_upload_url

class AdCategory(models.Model):
    title = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.title
    


class Advert(models.Model):
    category = models.ForeignKey(AdCategory, on_delete=models.DO_NOTHING, related_name="advert_category")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    design = models.FileField(upload_to=advertizement_design_upload_url, blank=True, null=True)
    website_url = models.URLField(max_length=1000, blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["category", "title"], name="unique_category_title_fields"
            )
        ]
    def __str__(self):
        return self.title
    