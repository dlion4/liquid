from django.db import models

from amiribd.users.models import Profile


class AIHistory(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="profile_ai_history")
    title = models.CharField(max_length=1000)
    question = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "History"
        verbose_name_plural = "Histories"