from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Profile
from django.contrib.auth.models import User
