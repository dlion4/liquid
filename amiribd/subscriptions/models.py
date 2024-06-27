from django.db import models
from amiribd.users.models import Profile
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Issue(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    files = models.FileField(upload_to="issues/%Y/%m/%d/", blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _('Issue')
        verbose_name_plural = _('Issues')
