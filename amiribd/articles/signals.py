from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import AiToken
from amiribd.users.models import Profile


@receiver(post_save, sender=Profile)
def assign_each_profile_ai_tokens_on_signup(sender, instance,created, **kwargs):
    if created:AiToken.objects.create(profile=instance)
    else: pass


